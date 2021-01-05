# -*- coding: utf-8 -*- 
# @Time : 2020/11/19 17:11 
# @Author : 王西亚 
# @File : job_dm_inbound_qi_monitor.py
from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_dm_inbound_qi_monitor(CTimeJob):
    def execute(self) -> str:
        inbound_qi_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select 
                dm2_storage_inbound.dsiid as query_ib_id
              , dm2_storage.dstid as query_storage_id
              , dm2_storage.dsttitle as query_storage_title
              , dm2_storage.dsttype as query_storage_type
              , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
              , dm2_storage_inbound.dsidirectory as query_ib_relation_dir
              , dm2_storage_inbound.dsidirectoryid as query_ib_relation_dir_id
              , dm2_storage_inbound.dsibatchno as query_ib_batchno
              , dm2_storage.dstotheroption as query_storage_option
              , dm2_storage_inbound.dsiotheroption as query_ib_option
            from dm2_storage_inbound 
              left join dm2_storage on dm2_storage.dstid = dm2_storage_inbound.dsistorageid 
            where dm2_storage_inbound.dsistatus = {0}
            '''.format(self.IB_Status_QI_Processing)
        )
        if inbound_qi_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有需要检查的入库质检任务！')

        abnormal_job_retry_times = settings.application.xpath_one(
            self.Path_Setting_MetaData_InBound_Parser_MetaData_Retry_Times,
            self.Default_Abnormal_Job_Retry_Times
        )

        for data_index in range(inbound_qi_list.size()):
            ds_ib_id = inbound_qi_list.value_by_name(data_index, 'query_ib_id', '')
            ds_storage_id = inbound_qi_list.value_by_name(data_index, 'query_storage_id', '')
            ds_storage_title = inbound_qi_list.value_by_name(data_index, 'query_storage_title', '')
            ds_storage_type = inbound_qi_list.value_by_name(data_index, 'query_storage_type', self.Storage_Type_Mix)
            ds_storage_root_dir = inbound_qi_list.value_by_name(data_index, 'query_rootpath', '')
            ds_ib_directory_name = inbound_qi_list.value_by_name(data_index, 'query_ib_relation_dir', '')
            ds_ib_directory_id = inbound_qi_list.value_by_name(data_index, 'query_ib_relation_dir_id', '')
            # 需要时再开启
            ds_storage_option = CUtils.any_2_str(inbound_qi_list.value_by_name(data_index, 'query_storage_option', ''))
            ds_ib_option = CUtils.any_2_str(inbound_qi_list.value_by_name(data_index, 'query_ib_option', ''))

            CLogger().debug(
                '正在检查存储[{0}]下的目录[{1}]质检进度...'.format(
                    ds_storage_title,
                    ds_ib_directory_name
                )
            )

            try:
                # 检查目录扫描进度
                dir_record_total_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_directory
                    where dsd_ib_id = :ib_id
                    ''',
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )
                dir_record_finished_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_directory
                    where dsd_ib_id = :ib_id
                      and dsdscanstatus = {0}
                      and dsdscandirstatus = {0}
                      and dsdscanfilestatus = {0}
                    '''.format(self.ProcStatus_Finished),
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )
                if dir_record_total_count == 0:
                    self.update_inbound_qi_result(
                        ds_ib_id,
                        CResult.merge_result(
                            self.Failure,
                            '存储[{0}]下的目录[{1}]未找到对应的质检任务, 请检查异常情况! '.format(
                                ds_storage_title,
                                CFile.join_file(ds_storage_root_dir, ds_ib_directory_name)
                            )
                        )
                    )
                    continue

                if dir_record_total_count != dir_record_finished_count:
                    CLogger().debug(
                        '存储[{0}]下的目录[{1}]质检任务正在进行, 目录还未扫描完毕! '.format(
                            ds_storage_title,
                            CFile.join_file(ds_storage_root_dir, ds_ib_directory_name)
                        )
                    )
                    continue

                # 检查文件扫描进度
                file_record_total_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_file
                    where dsf_ib_id = :ib_id
                    ''',
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )
                file_record_finished_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_file
                    where dsf_ib_id = :ib_id
                      and dsfscanstatus = {0}
                    '''.format(self.ProcStatus_Finished),
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )

                if file_record_total_count != file_record_finished_count:
                    CLogger().debug(
                        '存储[{0}]下的目录[{1}]质检任务正在进行, 文件还未扫描完毕! '.format(
                            ds_storage_title,
                            CFile.join_file(ds_storage_root_dir, ds_ib_directory_name)
                        )
                    )
                    continue

                # 检查对象识别进度
                obj_record_total_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dso_ib_id = :ib_id
                    ''',
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )
                obj_record_correct_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dso_ib_id = :ib_id
                        and dsometadataparsestatus = {0}
                        and dsodetailparsestatus = {0}
                        and dsotagsparsestatus = {0} 
                        and dso_da_status = {0}
                    '''.format(self.ProcStatus_Finished),
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )
                obj_record_error_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dso_ib_id = :ib_id
                        and dsometadataparsestatus <> {0}
                        and dso_metadataparser_retry = {1}
                    '''.format(self.ProcStatus_Finished, abnormal_job_retry_times),
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )

                if obj_record_total_count != obj_record_correct_count + obj_record_error_count:
                    CLogger().debug(
                        '存储[{0}]下的目录[{1}]质检任务正在进行, 识别的数据还未分析处理完毕, 已经识别数据[{2}]个, 成功质检[{3}]个, 失败[{4}]个, 请稍后...'.format(
                            ds_storage_title,
                            CFile.join_file(ds_storage_root_dir, ds_ib_directory_name),
                            obj_record_total_count,
                            obj_record_correct_count,
                            obj_record_error_count
                        )
                    )
                    continue

                self.update_inbound_qi_result(
                    ds_ib_id,
                    CResult.merge_result(
                        self.Success,
                        '存储[{0}]下的目录[{1}]质检任务已经完成, 共识别数据[{2}]个, 成功质检[{3}]个, 失败[{4}]个, 请检查! '.format(
                            ds_storage_title,
                            CFile.join_file(ds_storage_root_dir, ds_ib_directory_name),
                            obj_record_total_count,
                            obj_record_correct_count,
                            obj_record_error_count
                        )
                    ),
                    ds_storage_type,
                    ds_storage_option,
                    ds_ib_option
                )

            except Exception as error:
                self.update_inbound_qi_result(
                    ds_ib_id,
                    CResult.merge_result(
                        self.Failure,
                        '存储[{0}]下的目录[{1}]质检任务检查过程出现异常情况, 详细错误信息为: [{2}]'.format(
                            ds_storage_title,
                            CFile.join_file(ds_storage_root_dir, ds_ib_directory_name),
                            error.__str__()
                        )
                    )
                )
                continue

        return CResult.merge_result(self.Success, '本次入库质检任务成功结束！')

    def update_inbound_qi_result(self, notify_id, result, storage_type='mix', storage_option=None, ib_option=None):
        CLogger().debug(CResult.result_message(result))
        if CResult.result_success(result):
            if CUtils.equal_ignore_case(storage_type, self.Storage_Type_InBound):
                switch_inbound_after_qi_immediately_status = CUtils.equal_ignore_case(
                    settings.application.xpath_one(
                        self.path_switch(
                            self.Path_Setting_MetaData_QI_Switch,
                            self.Switch_Inbound_After_QI_Immediately_Of_IB_Storage
                        ),
                        self.Name_ON
                    ),
                    self.Name_ON
                )
            else:
                switch_inbound_after_qi_immediately_status = CUtils.equal_ignore_case(
                    settings.application.xpath_one(
                        self.path_switch(
                            self.Path_Setting_MetaData_QI_Switch,
                            self.Switch_Inbound_After_QI_Immediately_Of_MIX_Storage
                        ),
                        self.Name_OFF
                    ),
                    self.Name_ON
                )

            if switch_inbound_after_qi_immediately_status:
                next_status = self.IB_Status_IB_InQueue
            else:
                next_status = self.IB_Status_QI_Finished

            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsiStatus = {0}, dsiprocmemo = :notify_message
                where dsiid = :notify_id   
                '''.format(next_status),
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsiprocmemo = :notify_message
                where dsiid = :notify_id   
                ''',
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound_qi_monitor('', '').execute()
