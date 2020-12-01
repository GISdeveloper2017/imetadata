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
              , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
              , dm2_storage_inbound.dsidirectory as query_ib_relation_dir
              , dm2_storage_inbound.dsidirectoryid as query_ib_relation_dir_id
              , dm2_storage_inbound.dsibatchno as query_ib_batchno
              , dm2_storage_inbound.dsiotheroption as query_ib_option
            from dm2_storage_inbound 
              left join dm2_storage on dm2_storage.dstid = dm2_storage_inbound.dsistorageid 
            where dm2_storage_inbound.dsistatus in ({0}, {1})
            '''.format(self.IB_Status_QI_Processing, self.IB_Status_QI_Error)
        )
        if inbound_qi_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有需要检查的入库质检任务！')

        for data_index in range(inbound_qi_list.size()):
            ds_ib_id = inbound_qi_list.value_by_name(data_index, 'query_ib_id', '')
            ds_storage_id = inbound_qi_list.value_by_name(data_index, 'query_storage_id', '')
            ds_storage_title = inbound_qi_list.value_by_name(data_index, 'query_storage_title', '')
            ds_storage_root_dir = inbound_qi_list.value_by_name(data_index, 'query_rootpath', '')
            ds_ib_directory_name = inbound_qi_list.value_by_name(data_index, 'query_ib_relation_dir', '')
            ds_ib_directory_id = inbound_qi_list.value_by_name(data_index, 'query_ib_relation_dir_id', '')
            # 需要时再开启
            # ds_ib_option = CUtils.any_2_str(inbound_qi_list.value_by_name(data_index, 'query_ib_option', ''))

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
                    where dsdstorageid = :storage_id
                      and  ((dsdid = :directory_id) or (position(:SubDirectory in dsddirectory) = 1))
                    ''',
                    {
                        'directory_id': ds_ib_directory_id,
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                )
                dir_record_finished_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_directory
                    where dsdstorageid = :storage_id
                      and  ((dsdid = :directory_id) or (position(:SubDirectory in dsddirectory) = 1))
                      and dsdscanstatus = {0}
                      and dsdscandirstatus = {0}
                      and dsdscanfilestatus = {0}
                    '''.format(self.ProcStatus_Finished),
                    {
                        'directory_id': ds_ib_directory_id,
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
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
                            ds_ib_directory_name
                        )
                    )
                    continue

                # 检查文件扫描进度
                file_record_total_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_file
                    where dsfstorageid = :storage_id
                      and position(:SubDirectory in dsffilerelationname) = 1
                    ''',
                    {
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                )
                file_record_finished_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_file
                    where dsfstorageid = :storage_id
                      and position(:SubDirectory in dsffilerelationname) = 1
                      and dsfscanstatus = {0}
                    '''.format(self.ProcStatus_Finished),
                    {
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                )

                if file_record_total_count != file_record_finished_count:
                    CLogger().debug(
                        '存储[{0}]下的目录[{1}]质检任务正在进行, 文件还未扫描完毕! '.format(
                            ds_storage_title,
                            ds_ib_directory_name
                        )
                    )
                    continue

                # 检查对象识别进度
                obj_record_total_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dsoid in (
                      select dsd_object_id
                      from dm2_storage_directory
                      where dsdstorageid = :storage_id
                          and  ((dsdid = :directory_id) or (position(:SubDirectory in dsddirectory) = 1))
                    )
                    ''',
                    {
                        'directory_id': ds_ib_directory_id,
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dsoid in (
                      select dsf_object_id
                      from dm2_storage_file
                      where dsfstorageid = :storage_id
                        and position(:SubDirectory in dsffilerelationname) = 1
                    )
                    ''',
                    {
                        'directory_id': ds_ib_directory_id,
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                )
                obj_record_finished_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dsoid in (
                      select dsd_object_id
                      from dm2_storage_directory
                      where dsdstorageid = :storage_id
                          and  ((dsdid = :directory_id) or (position(:SubDirectory in dsddirectory) = 1))
                    )   and dsometadataparsestatus = {0}
                        and dsodetailparsestatus = {0}
                        and dsotagsparsestatus = {0} 
                    '''.format(self.ProcStatus_Finished),
                    {
                        'directory_id': ds_ib_directory_id,
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    '''
                    select count(*)
                    from dm2_storage_object
                    where dsoid in (
                      select dsf_object_id
                      from dm2_storage_file
                      where dsfstorageid = :storage_id
                        and position(:SubDirectory in dsffilerelationname) = 1
                    )   and dsometadataparsestatus = {0}
                        and dsodetailparsestatus = {0}
                        and dsotagsparsestatus = {0} 
                    '''.format(self.ProcStatus_Finished),
                    {
                        'directory_id': ds_ib_directory_id,
                        'storage_id': ds_storage_id,
                        'SubDirectory': CFile.join_file(ds_ib_directory_name, '')
                    },
                    0
                )

                if obj_record_total_count != obj_record_finished_count:
                    CLogger().debug(
                        '存储[{0}]下的目录[{1}]质检任务正在进行, 识别的数据还未分析处理完毕! '.format(
                            ds_storage_title,
                            ds_ib_directory_name
                        )
                    )
                    continue

                self.update_inbound_qi_result(
                    ds_ib_id,
                    CResult.merge_result(
                        self.Success,
                        '存储[{0}]下的目录[{1}]质检任务已经完成! '.format(
                            ds_storage_title,
                            ds_ib_directory_name
                        )
                    )
                )

            except Exception as error:
                self.update_inbound_qi_result(
                    ds_ib_id,
                    CResult.merge_result(
                        self.Failure,
                        '存储[{0}]下的目录[{1}]质检任务检查过程出现异常情况, 详细错误信息为: [{2}]'.format(
                            ds_storage_title,
                            ds_ib_directory_name,
                            error.__str__()
                        )
                    )
                )
                continue

        return CResult.merge_result(self.Success, '本次入库质检任务成功结束！')

    def update_inbound_qi_result(self, notify_id, result):
        CLogger().debug(CResult.result_message(result))
        if CResult.result_success(result):
            switch_inbound_after_qi_immediately_status = CUtils.equal_ignore_case(
                settings.application.xpath_one(
                    self.path_switch(
                        self.Path_Setting_MetaData_QI_Switch,
                        self.Switch_Inbound_After_QI_Immediately
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
                set dsiStatus = {0}, dsiprocmemo = :notify_message
                where dsiid = :notify_id   
                '''.format(self.IB_Status_QI_Error),
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound_qi_monitor('', '').execute()
