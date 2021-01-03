# -*- coding: utf-8 -*- 
# @Time : 2020/11/19 17:11 
# @Author : 王西亚 
# @File : job_dm_inbound_qi_monitor.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_dm_inbound_notify_monitor(CTimeJob):
    def execute(self) -> str:
        inbound_ib_n_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select 
                dsiid as query_ib_id
                , dsiotheroption as query_ib_option
                , dsidirectory as query_ib_relation_dir
                , dsidirectoryid as query_ib_dir_id
                , dsitargetstorageid as query_ib_target_storage_id
            from dm2_storage_inbound 
            where dsi_na_status = {0}
            '''.format(self.ProcStatus_WaitConfirm)
        )
        if inbound_ib_n_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有需要检查的通知任务！')

        for data_index in range(inbound_ib_n_list.size()):
            ds_ib_id = inbound_ib_n_list.value_by_name(data_index, 'query_ib_id', '')
            ds_ib_option = CUtils.any_2_str(inbound_ib_n_list.value_by_name(data_index, 'query_ib_option', ''))
            ds_ib_directory_name = inbound_ib_n_list.value_by_name(data_index, 'query_ib_relation_dir', '')
            ds_ib_directory_id = inbound_ib_n_list.value_by_name(data_index, 'query_ib_dir_id', '')
            ds_ib_target_storage_id = inbound_ib_n_list.value_by_name(data_index, 'query_ib_target_storage_id', '')

            module_name_list = CJson.json_attr_value(ds_ib_option, self.Path_IB_Opt_Notify_module, None)
            if module_name_list is None:
                modules_root_dir = CSys.get_metadata_data_access_modules_root_dir()
                module_file_list = CFile.file_or_subpath_of_path(
                    modules_root_dir,
                    '{0}_*.{1}'.format(self.Name_Module, self.FileExt_Py)
                )
                module_name_list = list()
                for module_file in module_file_list:
                    module_name_list.append(CFile.file_main_name(module_file))

            CLogger().debug('正在检查入库批次[ds_ib_id]的通知进度...'.format(ds_ib_id))

            try:
                # 所有通知对象的统计数
                sql_record_total_count = CUtils.replace_placeholder(
                    '''
                    select count(*)
                    from dm2_storage_obj_na
                    where dson_app_id in ($module_name_list)
                          and  dson_object_id in (
                                select dsoid
                                from dm2_storage_object 
                                where dso_ib_id = :ib_id
                          )
                    ''',
                    {'module_name_list': CUtils.list_2_str(module_name_list, "'", ',', "'")}
                )

                record_total_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    sql_record_total_count,
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )

                if record_total_count == 0:
                    self.update_inbound_na_result(
                        ds_ib_id,
                        CResult.merge_result(
                            self.Failure,
                            '入库任务下没有可通知的数据, 请检查异常情况! '.format(ds_ib_id)
                        )
                    )
                    continue

                # 已经完成的通知对象的统计数, 包括正常完成和错误的
                sql_record_finished_count = CUtils.replace_placeholder(
                    '''
                    select count(*)
                    from dm2_storage_obj_na
                    where dson_notify_status in ({0}, {1})
                          and  dson_app_id in ($module_name_list)
                          and  dson_object_id in (
                                select dsoid
                                from dm2_storage_object 
                                where dso_ib_id = :ib_id
                          )
                    '''.format(self.ProcStatus_Finished, self.ProcStatus_Error),
                    {'module_name_list': CUtils.list_2_str(module_name_list, "'", ',', "'")}
                )

                record_finished_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    sql_record_finished_count,
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )

                # 错误的记录数
                sql_record_error_count = CUtils.replace_placeholder(
                    '''
                    select count(*)
                    from dm2_storage_obj_na
                    where dson_notify_status = {0}
                          and  dson_app_id in ($module_name_list)
                          and  dson_object_id in (
                                select dsoid
                                from dm2_storage_object 
                                where dso_ib_id = :ib_id
                          )
                    '''.format(self.ProcStatus_Error),
                    {'module_name_list': CUtils.list_2_str(module_name_list, "'", ',', "'")}
                )

                record_error_count = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                    sql_record_error_count,
                    {
                        'ib_id': ds_ib_id
                    },
                    0
                )

                if record_total_count != record_finished_count:
                    message = '入库任务[{0}]下的数据正在通知其他子系统, 共有[{1}]个, 已正确完成[{2}]个, 失败[{3}]个...'.format(
                        ds_ib_id,
                        record_total_count,
                        record_finished_count,
                        record_error_count
                    )
                    CLogger().debug(message)
                    self.update_inbound_na_progress(ds_ib_id, message)
                else:
                    message = '入库任务[{0}]下的数据已经通知其他子系统, 共有[{1}]个, 已正确完成[{2}]个, 失败[{3}]个, 请检查修正! '.format(
                        ds_ib_id,
                        record_total_count,
                        record_finished_count,
                        record_error_count
                    )
                    CLogger().debug(message)
                    self.update_inbound_na_result(ds_ib_id, message)

            except Exception as error:
                self.update_inbound_na_result(
                    ds_ib_id,
                    CResult.merge_result(
                        self.Failure,
                        '入库任务下的数据通知其他子系统过程中出现异常情况, 详细错误信息为: [{1}]'.format(
                            ds_ib_id,
                            error.__str__()
                        )
                    )
                )
                continue

        return CResult.merge_result(self.Success, '本次通知监控任务成功结束！')

    def update_inbound_na_result(self, notify_id, result):
        CLogger().debug(CResult.result_message(result))
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsi_na_status = {0}, dsi_na_proc_memo = :notify_message, dsiproctime = now()
                where dsiid = :notify_id   
                '''.format(self.ProcStatus_Finished),
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsi_na_proc_memo = :notify_message, dsiproctime = now()
                where dsiid = :notify_id   
                ''',
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )

    def update_inbound_na_progress(self, notify_id, message):
        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage_inbound 
            set dsi_na_proc_memo = :notify_message, dsiproctime = now()
            where dsiid = :notify_id   
            ''',
            {'notify_id': notify_id, 'notify_message': message}
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound_notify_monitor('', '').execute()
