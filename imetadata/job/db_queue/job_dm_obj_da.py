# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 16:14 
# @Author : 王西亚 
# @File : job_dm_obj_detail.py


from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_obj_da(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_object 
set dso_da_proc_id = '{0}', dso_da_status = 2
where dsoid = (
  select dsoid  
  from   dm2_storage_object 
  where  dso_da_status = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dsoid, dsodatatype, dsoobjecttype, dsoobjectname, dso_quality, dso_da_result from dm2_storage_object where dso_da_proc_id = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_object 
set dso_da_status = 1, dso_da_proc_id = null 
where dso_da_status = 2
        '''

    def process_mission(self, dataset):
        dso_id = dataset.value_by_name(0, 'dsoid', '')
        dso_data_type = dataset.value_by_name(0, 'dsodatatype', '')
        dso_object_type = dataset.value_by_name(0, 'dsoobjecttype', '')
        dso_object_name = dataset.value_by_name(0, 'dsoobjectname', '')
        dso_object_da_content = CUtils.any_2_str(dataset.value_by_name(0, 'dso_da_result', ''))
        dso_object_quality = dataset.value_by_name(0, 'dso_quality', '')

        dso_quality = CXml()
        dso_quality.load_xml(dso_object_quality)

        dso_da_json = CJson()
        dso_da_json.load_json_text(dso_object_da_content)

        CLogger().debug(
            '开始处理对象: {0}.{1}.{2}.{3}对各个子系统的支撑能力'.format(dso_id, dso_data_type, dso_object_type, dso_object_name))

        try:
            modules_root_dir = CSys.get_metadata_data_access_modules_root_dir()
            modules_file_list = CFile.file_or_subpath_of_path(
                modules_root_dir,
                '{0}_*.{1}'.format(self.Name_Module, self.FileExt_Py)
            )
            for file_name_without_path in modules_file_list:
                file_main_name = CFile.file_main_name(file_name_without_path)
                # 判断模块的可访问是否已经被人工审批, 如果人工审批, 则这里不再计算和覆盖
                module_access = dso_da_json.xpath_one(
                    '{0}.{1}'.format(file_main_name, self.Name_Audit),
                    self.Name_System
                )
                if CUtils.equal_ignore_case(module_access, self.Name_User):
                    continue

                try:
                    module_obj = CObject.create_module_instance(
                        CSys.get_metadata_data_access_modules_root_name(),
                        file_main_name,
                        self.get_mission_db_id(),
                        dso_id,
                        dso_object_name,
                        dso_data_type,
                        dso_quality
                    )
                    module_title = CUtils.dict_value_by_name(module_obj.information(), self.Name_Title, '')
                    result = CUtils.any_2_str(module_obj.access())
                    if CResult.result_success(result):
                        module_access = CResult.result_info(result, self.Name_Access, self.DataAccess_Forbid)
                        module_obj = {self.Name_Audit: self.Name_System, self.Name_Result: module_access,
                                      self.Name_Title: module_title}
                        dso_da_json.set_value_of_name(file_main_name, module_obj)
                    else:
                        CLogger().debug('模块[{0}]解析出现错误, 系统将忽略本模块, 继续处理下一个!'.format(file_main_name))
                        continue
                except Exception as error:
                    CLogger().debug('模块[{0}]解析出现异常, 原因为[{1}], 请检查!'.format(file_main_name, error.__str__()))
                    continue

            self.db_update_status(
                dso_id, self.ProcStatus_Finished, dso_da_json.to_json(),
                '对象[{0}]访问权限解析成功!'.format(dso_object_name)
            )
            return CResult.merge_result(self.Success, '对象[{0}.{1}]访问权限解析成功!'.format(dso_id, dso_object_name))
        except Exception as error:
            self.db_update_status(
                dso_id, self.ProcStatus_Error, dso_da_json.to_json(),
                '对象[{0}]访问权限解析出错, 原因为[{1}]!'.format(dso_object_name, error.__str__())
            )
            return CResult.merge_result(
                self.Failure,
                '对象[{0}.{1}]访问权限解析出错, 原因为[{2}]!'.format(dso_id, dso_object_name, error.__str__())
            )

    def db_update_status(self, dso_id, status, da_result, memo):
        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage_object
            set dso_da_result = :da_result
                , dso_da_status = :status
                , dso_da_proc_memo = :memo
                , dsolastmodifytime = now()
            where dsoid = :dsoid
            ''',
            {'dsoid': dso_id, 'da_result': da_result, 'status': status, 'memo': memo}
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_obj_da('', '').execute()
