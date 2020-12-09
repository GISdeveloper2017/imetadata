# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 16:12 
# @Author : 王西亚 
# @File : job_dm_obj_tags.py

from __future__ import absolute_import

from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.business.metadata.base.parser.tags.c_tagsParser import CTagsParser
from imetadata.business.metadata.base.plugins.manager.c_pluginsMng import CPluginsMng
from imetadata.database.c_factory import CFactory


class job_dm_obj_tags(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsotagsparseprocid = '{0}', dsotagsparsestatus = {1}
where dsoid = (
  select dsoid  
  from   dm2_storage_object 
  where  dsotagsparsestatus = {2} 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID, self.ProcStatus_Processing, self.ProcStatus_InQueue)

    def get_mission_info_sql(self):
        return '''
select dsoid, dsodatatype, dsoobjecttype, dsoobjectname 
from dm2_storage_object 
where dsotagsparseprocid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsotagsparsestatus = {0}, dsotagsparseprocid = null 
where dsotagsparsestatus = {1}
        '''.format(self.ProcStatus_InQueue, self.ProcStatus_Processing)

    def process_mission(self, dataset, is_retry_mission: bool):
        dso_id = dataset.value_by_name(0, 'dsoid', '')
        dso_data_type = dataset.value_by_name(0, 'dsodatatype', '')
        dso_object_type = dataset.value_by_name(0, 'dsoobjecttype', '')
        dso_object_name = dataset.value_by_name(0, 'dsoobjectname', '')

        CLogger().debug('开始处理对象: {0}.{1}.{2}.{3}的元数据'.format(dso_id, dso_data_type, dso_object_type, dso_object_name))

        ds_object_info = self.get_object_info(dso_id, dso_data_type)
        ds_object_storage_option = ds_object_info.value_by_name(0, 'query_object_storage_option', None)

        if ds_object_info.value_by_name(0, 'query_object_valid', self.DB_False) == self.DB_False:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_object
                set dsotagsparsestatus = 0
                  , dsolastmodifytime = now()
                  , dsotagsparsememo = '文件或目录不存在，标签无法解析'
                where dsoid = :dsoid
                ''',
                {'dsoid': dso_id}
            )
            return CResult.merge_result(self.Success, '文件或目录[{0}]不存在，标签处理正常结束!'.format(
                ds_object_info.value_by_name(0, 'query_object_fullname', '')))

        sql_get_rule = '''
            select dsdScanRule
            from dm2_storage_directory
            where dsdStorageid = :dsdStorageID and Position(dsddirectory || '{0}' in :dsdDirectory) = 1
                and dsdScanRule is not null
            order by dsddirectory desc
            limit 1
            '''.format(CFile.sep())
        rule_ds = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_rule, {
            'dsdStorageID': ds_object_info.value_by_name(0, 'query_object_storage_id', ''),
            'dsdDirectory': ds_object_info.value_by_name(0, 'query_object_relation_path', '')})
        ds_rule_content = rule_ds.value_by_name(0, 'dsScanRule', '')
        file_info_obj = CDMFilePathInfoEx(
            dso_data_type,
            ds_object_info.value_by_name(0, 'query_object_fullname', ''),
            ds_object_info.value_by_name(0, 'query_object_storage_id', ''),
            ds_object_info.value_by_name(0, 'query_object_file_id', ''),
            ds_object_info.value_by_name(0, 'query_object_file_parent_id', ''),
            ds_object_info.value_by_name(0, 'query_object_owner_id', ''),
            self.get_mission_db_id(),
            ds_rule_content
        )
        plugins_obj = CPluginsMng.plugins(file_info_obj, dso_object_type)
        if plugins_obj is None:
            return CResult.merge_result(
                self.Failure,
                '文件或目录[{0}]的类型插件[{1}]不存在，对象详情无法解析, 处理结束!'.format(
                    ds_object_info.value_by_name(0, 'query_object_fullname', ''),
                    dso_object_type
                )
            )

        try:
            plugins_information = plugins_obj.get_information()
            tags_parser_rule = CUtils.dict_value_by_name(plugins_information, plugins_obj.Plugins_Info_TagsEngine, None)

            if tags_parser_rule is None:
                tags_parser_rule = CJson.json_attr_value(
                    CUtils.any_2_str(ds_object_storage_option),
                    self.Path_Setting_MetaData_Tags_Rule,
                    None
                )

            if tags_parser_rule is None:
                tags_parser_rule = settings.application.xpath_one(self.Path_Setting_MetaData_Tags_Rule, None)

            if tags_parser_rule is None:
                process_result = CResult.merge_result(CResult.Success, '系统未设置标签库和识别模式, 标签解析将自动结束')
            else:
                process_result = plugins_obj.parser_tags(
                    CTagsParser(
                        dso_id,
                        dso_object_name,
                        file_info_obj,
                        tags_parser_rule
                    )
                )

            self.db_update_object_status(dso_id, process_result)
            return process_result
        except Exception as err:
            process_result = CResult.merge_result(
                self.Failure,
                '文件或目录[{0}]对象业务分类解析过程出现错误! 错误原因为: {1}'.format(
                    ds_object_info.value_by_name(0, 'query_object_fullname', ''),
                    err.__str__()
                )
            )
            self.db_update_object_status(dso_id, process_result)
            return process_result

    def db_update_object_status(self, dso_id, process_result):
        CLogger().debug(CResult.result_message(process_result))
        if CResult.result_success(process_result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_object
                set dsotagsparsestatus = {0}
                  , dsolastmodifytime = now()
                  , dsotagsparsememo = :dsotagsparsememo
                where dsoid = :dsoid
                '''.format(self.ProcStatus_Finished),
                {
                    'dsoid': dso_id,
                    'dsotagsparsememo': CResult.result_message(process_result)
                }
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_object
                set dsotagsparsestatus = {0}
                  , dsolastmodifytime = now()
                  , dsotagsparsememo = :dsotagsparsememo
                where dsoid = :dsoid
                '''.format(self.ProcStatus_Error),
                {
                    'dsoid': dso_id,
                    'dsotagsparsememo': CResult.result_message(process_result)
                }
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_obj_tags('', '').execute()
