# -*- coding: utf-8 -*- 
# @Time : 2020/10/24 12:53 
# @Author : 王西亚 
# @File : job_dm_inbound.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_inbound_notify(CDMBaseJob):

    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsi_na_proc_id = '{0}', dsi_na_status = 2
where dsiid = (
  select dsiid  
  from   dm2_storage_inbound 
  where  dsi_na_status = 1 and dsistatus = 0  
  order by dsiaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage_inbound.dsiid as query_ib_id
  , dm2_storage_inbound.dsibatchno as query_ib_batchno
  , dm2_storage_inbound.dsiotheroption as query_ib_option
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dsttitle as query_storage_title
  , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
  , dm2_storage_directory.dsdid as query_ib_dir_id 
  , dm2_storage_directory.dsddirectory as query_ib_relation_dir
from dm2_storage_inbound 
  left join dm2_storage_directory on dm2_storage_directory.dsdid = dm2_storage_inbound.dsidirectoryid 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
where dm2_storage_inbound.dsi_na_proc_id = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsi_na_status = 1, dsi_na_proc_id = null 
where dsi_na_status = 2
        '''

    def process_mission(self, dataset) -> str:
        """
        :param dataset:
        :return:
        """
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_storage_title = dataset.value_by_name(0, 'query_storage_title', '')
        ds_ib_id = dataset.value_by_name(0, 'query_ib_id', '')
        ds_ib_directory_name = dataset.value_by_name(0, 'query_ib_relation_dir', '')
        ds_ib_batch_no = dataset.value_by_name(0, 'query_ib_batchno', '')
        ds_ib_option = CUtils.any_2_str(dataset.value_by_name(0, 'query_ib_option', ''))

        CLogger().debug('与第三方模块同步的目录为: {0}.{1}'.format(ds_ib_id, ds_ib_directory_name))
        data_count = 0
        try:
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

            sql_ib_need_notify_object = '''
            select dsoid, dsoobjecttype, dsoobjectname, dso_da_result
            from dm2_storage_object 
            where (
                dm2_storage_object.dsoid in (
                    select dsd_object_id
                    from dm2_storage_directory
                    where dsdstorageid = :StorageID
                        and dsd_object_id is not null
                        and position(:SubDirectory in dsddirectory) = 1
                ) or dm2_storage_object.dsoid in (
                    select dsf_object_id
                    from dm2_storage_file
                    where dsfdirectoryid in (
                        select dsdid
                        from dm2_storage_directory
                        where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                    )
                )
            )
            '''
            dataset = CFactory().give_me_db(self.get_mission_db_id()).all_row(
                sql_ib_need_notify_object,
                {'StorageID': ds_storage_id, 'SubDirectory': ds_ib_directory_name}
            )
            if dataset.is_empty():
                result = CResult.merge_result(
                    self.Success,
                    '存储[{0}]下, 批次为[{1}]的目录[{2}]下无任何对象, 不再通知给第三方应用!'.format(
                        ds_storage_title,
                        ds_ib_batch_no,
                        ds_ib_directory_name
                    )
                )
                self.update_notify_result(ds_ib_id, result)
                return result

            CLogger().debug(
                '存储[{0}]下, 批次为[{1}]的目录[{2}]下有[{3}]个对象等待通知给第三方应用!'.format(
                    ds_storage_title,
                    ds_ib_batch_no,
                    ds_ib_directory_name,
                    dataset.size()
                )
            )
            data_count = dataset.size()
            error_message = ''
            for data_index in range(data_count):
                record_object = dataset.record(data_index)

                object_id = CUtils.dict_value_by_name(record_object, 'dsoid', '')
                object_type = CUtils.dict_value_by_name(record_object, 'dsoobjecttype', '')
                object_name = CUtils.dict_value_by_name(record_object, 'dsoobjectname', '')
                object_da_result_text = CUtils.any_2_str(CUtils.dict_value_by_name(record_object, 'dso_da_result', ''))

                object_da_result = CJson()
                object_da_result.load_json_text(object_da_result_text)

                for module_name in module_name_list:
                    module_obj = CObject.create_module_instance(
                        CSys.get_metadata_data_access_modules_root_name(),
                        module_name,
                        self.get_mission_db_id(),
                        object_id,
                        object_name,
                        object_type,
                        None
                    )
                    module_id = module_name
                    module_title = CUtils.dict_value_by_name(module_obj.information(), self.Name_Title, '')

                    module_access = object_da_result.xpath_one('{0}.{1}'.format(module_id, self.Name_Result),
                                                               self.DataAccess_Forbid)
                    CLogger().debug(
                        '存储[{0}]下, 批次为[{1}]的目录[{2}]下的对象[{3}], 与模块[{4}]的访问权限为[{5}]!'.format(
                            ds_storage_title,
                            ds_ib_batch_no,
                            ds_ib_directory_name,
                            object_name,
                            module_title,
                            module_access
                        )
                    )
                    # todo(王西亚) 仔细考虑这里是否要放开, 是放开pass的, 还是放开pass和wait!!!!!!
                    # if not \
                    #         (
                    #                 CUtils.equal_ignore_case(module_access, self.DataAccess_Pass)
                    #                 or CUtils.equal_ignore_case(module_access, self.DataAccess_Wait)
                    #         ):
                    #     continue

                    result = module_obj.notify(module_access)
                    if not CResult.result_success(result):
                        message = CResult.result_message(result)
                        CLogger().debug(
                            '存储[{0}]下, 批次为[{1}]的目录[{2}]下的对象[{3}], 与模块[{4}]的通知处理结果出现错误, 详细情况: [{5}]!'.format(
                                ds_storage_title,
                                ds_ib_batch_no,
                                ds_ib_directory_name,
                                object_name,
                                module_title,
                                message
                            )
                        )
                        error_message = CUtils.str_append(error_message, message)

            if CUtils.equal_ignore_case(error_message, ''):
                result = CResult.merge_result(
                    self.Success,
                    '存储[{0}]下, 批次为[{1}]的目录[{2}]下有[{3}]个对象成功通知给第三方应用!'.format(
                        ds_storage_title,
                        ds_ib_batch_no,
                        ds_ib_directory_name,
                        data_count
                    )
                )
                self.update_notify_result(ds_ib_id, result)
                return result
            else:
                result = CResult.merge_result(
                    self.Failure,
                    '存储[{0}]下, 批次为[{1}]的目录[{2}]下有[{3}]个对象在通知给第三方应用时, 部分出现错误! 错误信息如下: \n{4}'.format(
                        ds_storage_title,
                        ds_ib_batch_no,
                        ds_ib_directory_name,
                        data_count,
                        error_message
                    )
                )
                self.update_notify_result(ds_ib_id, result)
                return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '存储[{0}]下, 批次为[{1}]的目录[{2}]下有[{3}]个对象通知给第三方应用时出现异常! 错误原因为: {4}!'.format(
                    ds_storage_title,
                    ds_ib_batch_no,
                    ds_ib_directory_name,
                    data_count,
                    error.__str__()
                )
            )
            self.update_notify_result(ds_ib_id, result)
            return result

    def update_notify_result(self, notify_id, result):
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsi_na_status = {0}
                    , dsi_na_proc_id = null
                    , dsi_na_proc_memo = :notify_message
                    , dsiproctime = now()
                where dsiid = :notify_id   
                '''.format(self.ProcStatus_Finished),
                {
                    'notify_id': notify_id,
                    'notify_message': CResult.result_message(result)
                }
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsi_na_status = {0}
                    , dsi_na_proc_id = null
                    , dsi_na_proc_memo = :notify_message
                    , dsiproctime = now()
                where dsiid = :notify_id   
                '''.format(self.ProcStatus_Error),
                {
                    'notify_id': notify_id,
                    'notify_message': CResult.result_message(result)
                }
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound_notify('', '').execute()
