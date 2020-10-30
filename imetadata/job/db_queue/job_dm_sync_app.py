# -*- coding: utf-8 -*- 
# @Time : 2020/10/24 12:53 
# @Author : 王西亚 
# @File : job_dm_inbound.py
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_sync_app(CDMBaseJob):

    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_obj_na 
set dson_notify_proc_id = '{0}', dson_notify_status = 2
where dsonid = (
  select dsonid  
  from   dm2_storage_obj_na 
  where  dson_notify_status = 1
  order by dson_addtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage_obj_na.dsonid as na_id
  , dm2_storage_obj_na.dson_app_id as app_id
  , dm2_storage_object.dsoid as object_id
  , dm2_storage_object.dsoobjecttype as object_type
  , dm2_storage_object.dsoobjectname as object_name
from dm2_storage_obj_na 
  left join dm2_storage_object on dm2_storage_obj_na.dson_object_id = dm2_storage_object.dsoid 
where dm2_storage_obj_na.dson_notify_proc_id = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_obj_na 
set dson_notify_status = 1, dson_notify_proc_id = null 
where dson_notify_status = 2
        '''

    def process_mission(self, dataset) -> str:
        """
        :param dataset:
        :return:
        """
        ds_na_id = dataset.value_by_name(0, 'na_id', '')
        ds_app_id = dataset.value_by_name(0, 'app_id', '')
        ds_object_id = dataset.value_by_name(0, 'object_id', '')
        ds_object_type = dataset.value_by_name(0, 'object_type', '')
        ds_object_name = dataset.value_by_name(0, 'object_name', '')

        CLogger().debug('与第三方模块[{0}]同步的对象为: [{1}]'.format(ds_app_id, ds_object_name))
        try:
            module_file_name = CFile.join_file(
                CSys.get_metadata_data_access_modules_root_dir(),
                '{0}.{1}'.format(ds_app_id, self.FileExt_Py)
            )
            if not CFile.file_or_path_exist(module_file_name):
                message = '第三方模块[{0}]没有设置对应的算法, 直接通过!'.format(ds_app_id)
                result = CResult.merge_result(self.Success, message)
                self.update_sync_result(ds_na_id, result)
                return result

            module_obj = CObject.create_module_instance(
                CSys.get_metadata_data_access_modules_root_name(),
                ds_app_id,
                self.get_mission_db_id(),
                ds_object_id,
                ds_object_name,
                ds_object_type,
                None
            )
            if module_obj is None:
                message = '第三方模块[{0}]没有设置对应的算法, 直接通过!'.format(ds_app_id)
                result = CResult.merge_result(self.Success, message)
                self.update_sync_result(ds_na_id, result)
                return result

            module_title = CUtils.dict_value_by_name(module_obj.information(), self.Name_Title, '')

            result = module_obj.sync()
            self.update_sync_result(ds_na_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '与第三方模块[{0}]同步的对象: [{1}]的同步过程出现异常, 详细情况: [{2}]!'.format(
                    ds_app_id,
                    ds_object_name,
                    error.__str__()
                )
            )
            self.update_sync_result(ds_na_id, result)
            return result

    def update_sync_result(self, na_id, result):
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_obj_na 
                set dson_notify_status = 0, dson_notify_proc_id = null, dson_notify_proc_memo = :proc_message
                where dsonid = :id   
                ''', {'id': na_id, 'proc_message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_obj_na 
                set dson_notify_status = 3, dson_notify_proc_id = null, dson_notify_proc_memo = :proc_message
                where dsonid = :id   
                ''', {'id': na_id, 'proc_message': CResult.result_message(result)}
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_sync_app('', '').execute()
