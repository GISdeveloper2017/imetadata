# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 16:12 
# @Author : 王西亚 
# @File : job_dm_obj_tags.py

from __future__ import absolute_import

from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.business.metadata.base.parser.tags.c_tagsParserMng import CTagsParserMng
from imetadata.business.metadata.base.plugins.manager.c_pluginsMng import CPluginsMng
from imetadata.database.c_factory import CFactory


class job_dm_obj_tags(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsotagsparseprocid = '{0}', dsotagsparsestatus = 2
where dsoid = (
  select dsoid  
  from   dm2_storage_object 
  where  dsotagsparsestatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dsoid, dsodatatype, dsoobjecttype, dsoobjectname from dm2_storage_object where dsotagsparseprocid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsotagsparsestatus = 1, dsotagsparseprocid = null 
where dsotagsparsestatus = 2
        '''

    def process_mission(self, dataset):
        dso_id = dataset.value_by_name(0, 'dsoid', '')
        dso_data_type = dataset.value_by_name(0, 'dsodatatype', '')
        dso_object_type = dataset.value_by_name(0, 'dsoobjecttype', '')
        dso_object_name = dataset.value_by_name(0, 'dsoobjectname', '')

        CLogger().debug('开始处理对象: {0}.{1}.{2}.{3}的元数据'.format(dso_id, dso_data_type, dso_object_type, dso_object_name))

        sql_get_info = ''
        if CUtils.equal_ignore_case(dso_data_type, self.FileType_Dir):
            sql_get_info = '''
                select 
                    dm2_storage.dstunipath || dm2_storage_directory.dsddirectory as query_object_fullname   
                    , dm2_storage_directory.dsd_directory_valid as query_object_valid  
                    , dm2_storage.dstunipath as query_object_root_dir 
                    , dm2_storage.dstid as query_object_storage_id
                    , dm2_storage_directory.dsddirectory as query_object_relation_path
                    , dm2_storage_directory.dsdid as query_object_file_id
                    , dm2_storage_directory.dsdparentid as query_object_file_parent_id
                    , dm2_storage_object.dsoparentobjid as query_object_owner_id
                from dm2_storage_object, dm2_storage_directory, dm2_storage  
                where 
                    dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id    
                    and dm2_storage_directory.dsdstorageid = dm2_storage.dstid    
                    and dm2_storage_object.dsoid = :dsoid
                '''
        else:
            sql_get_info = '''
                select 
                    dm2_storage.dstunipath || dm2_storage_file.dsffilerelationname as query_object_fullname 
                    , dm2_storage_file.dsffilevalid as query_object_valid     
                    , dm2_storage.dstunipath as query_object_root_dir 
                    , dm2_storage.dstid as query_object_storage_id
                    , dm2_storage_file.dsffilerelationname as query_object_relation_path
                    , dm2_storage_file.dsfid as query_object_file_id
                    , dm2_storage_file.dsfdirectoryid as query_object_file_parent_id
                    , dm2_storage_object.dsoparentobjid as query_object_owner_id
                from dm2_storage_object, dm2_storage_file, dm2_storage, dm2_storage_directory   
                where dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id 
                    and dm2_storage_file.dsfstorageid = dm2_storage.dstid 
                    and dm2_storage_directory.dsdid = dm2_storage_file.dsfdirectoryid 
                    and dm2_storage_object.dsoid = :dsoid
                '''
        ds_file_info = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_info, {'dsoid': dso_id})

        if ds_file_info.value_by_name(0, 'query_object_valid', self.DB_False) == self.DB_False:
            CFactory().give_me_db(self.get_mission_db_id()).execute('''
                update dm2_storage_object
                set dsotagsparsestatus = 0
                  , dsolastmodifytime = now()
                  , dsotagsparsememo = '文件或目录不存在，标签无法解析'
                where dsoid = :dsoid
                ''', {'dsoid': dso_id})
            return CResult.merge_result(self.Success, '文件或目录[{0}]不存在，标签处理正常结束!'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', '')))

        sql_get_rule = '''
            select dsdScanRule
            from dm2_storage_directory
            where dsdStorageid = :dsdStorageID and Position(dsddirectory || '/' in :dsdDirectory) = 1
                and dsdScanRule is not null
            order by dsddirectory desc
            limit 1
            '''
        rule_ds = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_rule, {
            'dsdStorageID': ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
            'dsdDirectory': ds_file_info.value_by_name(0, 'query_object_relation_path', '')})
        ds_rule_content = rule_ds.value_by_name(0, 'dsScanRule', '')
        file_info_obj = CDMFilePathInfoEx(dso_data_type,
                                          ds_file_info.value_by_name(0, 'query_object_fullname', ''),
                                          ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
                                          ds_file_info.value_by_name(0, 'query_object_file_id', ''),
                                          ds_file_info.value_by_name(0, 'query_object_file_parent_id', ''),
                                          ds_file_info.value_by_name(0, 'query_object_owner_id', ''),
                                          self.get_mission_db_id(),
                                          ds_rule_content
                                          )
        # file_info_obj = CFileInfoEx(dso_data_type,
        #                             ds_file_info.value_by_name(0, 'query_object_fullname', ''),
        #                             ds_file_info.value_by_name(0, 'query_object_root_dir', ''),
        #                             ds_rule_content
        #                             )
        plugins_obj = CPluginsMng.plugins(file_info_obj, dso_object_type)
        if plugins_obj is None:
            return CResult.merge_result(self.Failure, '文件或目录[{0}]的类型插件[{1}]不存在，对象详情无法解析, 处理结束!'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', ''),
                dso_object_type)
                                       )

        try:
            plugins_information = plugins_obj.get_information()
            tags_parser = CTagsParserMng.give_me_parser(
                CUtils.dict_value_by_name(plugins_information, plugins_obj.Plugins_Info_TagsEngine, None),
                dso_id, dso_object_name, file_info_obj)
            process_result = plugins_obj.parser_tags(tags_parser)
            if CResult.result_success(process_result):
                CFactory().give_me_db(self.get_mission_db_id()).execute('''
                    update dm2_storage_object
                    set dsotagsparsestatus = 0
                      , dsolastmodifytime = now()
                      , dsotagsparsememo = :dsotagsparsememo
                    where dsoid = :dsoid
                    ''', {'dsoid': dso_id, 'dsotagsparsememo': '文件或目录[{0}]对象详情解析成功结束!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''))})
                return CResult.merge_result(self.Success, '文件或目录[{0}]对象详情解析成功结束!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', '')))
            else:
                self.db_update_object_status(dso_id, '文件或目录[{0}]对象详情解析过程出现错误! 错误原因为: {1}'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''), CResult.result_message(process_result)))

                return CResult.merge_result(self.Failure, '文件或目录[{0}]对象详情解析过程出现错误!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', '')))
        except Exception as err:
            self.db_update_object_status(dso_id, '文件或目录[{0}]对象详情解析过程出现错误! 错误原因为: {1}'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', ''), err.__str__()))

            return CResult.merge_result(self.Failure, '文件或目录[{0}]对象详情解析过程出现错误!'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', '')))

    def db_update_object_status(self, dso_id, memo):
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_object
            set dsotagsparsestatus = 3
              , dsolastmodifytime = now()
              , dsotagsparsememo = :dsotagsparsememo
            where dsoid = :dsoid
            ''', {'dsoid': dso_id, 'dsotagsparsememo': memo})


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_obj_tags('', '').execute()
