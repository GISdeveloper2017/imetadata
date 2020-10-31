# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:31 
# @Author : 王西亚 
# @File : job_dm_path2object.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.fileinfo.c_dmPathInfo import CDMPathInfo
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_path2object(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdprocessid = '{0}', dsdscanstatus = 2
where dsdid = (
  select dsdid  
  from   dm2_storage_directory 
  where  dsdscanstatus = 1 and dsddirtype <> '2'
  order by dsdaddtime 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage.dstunipath as query_root_path
  , dm2_storage_directory.dsdparentid as query_dir_parent_id
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage.dstunipath || dm2_storage_directory.dsdpath as query_dir_full_path
  , dm2_storage_directory.dsddirectoryname as query_subpath_name
  , dm2_storage_directory.dsdid as query_dir_id
  , dm2_storage_directory.dsddirtype as query_dir_type
  , dm2_storage_directory.dsddirlastmodifytime as query_dir_lastmodifytime
  , dm2_storage.dstid as query_storage_id
  , dm2_storage_directory.dsd_object_type as query_dir_object_type
  , dm2_storage_directory.dsd_object_confirm as query_dir_object_confirm
  , dm2_storage_directory.dsd_object_id as query_dir_object_id
  , dm2_storage_directory.dsdscandirstatus as query_dir_ScanDirStatus
  , dm2_storage_directory.dsdparentobjid as query_dir_parent_objid
  , dm2_storage_object.dsoobjecttype as query_dir_parent_objtype
from dm2_storage_directory 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  left join dm2_storage_object on dm2_storage_object.dsoid = dm2_storage_directory.dsdparentobjid
where dm2_storage_directory.dsdprocessid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanstatus = 1, dsdprocessid = null 
where dsdscanstatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
        ds_root_path = dataset.value_by_name(0, 'query_root_path', '')
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_id = dataset.value_by_name(0, 'query_dir_id', '')
        owner_obj_id = dataset.value_by_name(0, 'query_dir_parent_objid', '')
        parent_id = dataset.value_by_name(0, 'query_dir_parent_id', '')

        sql_get_rule = '''
            select dsdScanRule
            from dm2_storage_directory
            where dsdStorageid = :dsdStorageID and Position(dsddirectory || '/' in :dsdDirectory) = 1
                and dsdScanRule is not null
            order by dsddirectory desc
            limit 1
            '''
        rule_ds = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_rule, {'dsdStorageID': ds_storage_id,
                                                                                         'dsdDirectory': ds_subpath})
        ds_rule_content = rule_ds.value_by_name(0, 'dsdScanRule', '')

        if ds_subpath == '':
            ds_path_full_name = ds_root_path
        else:
            ds_path_full_name = CFile.join_file(ds_root_path, ds_subpath)
        CLogger().debug('处理的子目录为: {0}'.format(ds_path_full_name))

        path_obj = CDMPathInfo(self.FileType_Dir, ds_path_full_name, ds_storage_id, ds_id, parent_id, owner_obj_id,
                               self.get_mission_db_id(), ds_rule_content)
        if not path_obj.file_existed:
            path_obj.db_update_status_on_path_invalid()
            return CResult.merge_result(CResult.Success,
                                        '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_path_full_name))
        else:
            path_obj.db_check_and_update_metadata_rule(CFile.join_file(ds_path_full_name, self.FileName_MetaData_Rule))

            path_obj.db_path2object()

        sql_update_directory_status = '''
            update dm2_storage_directory
            set dsdscanstatus = 0, dsdlastmodifytime = now()
            where dsdid = :dsdid
            '''
        params = dict()
        params['dsdid'] = dataset.value_by_name(0, 'query_dir_id', '')
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_directory_status, params)

        return CResult.merge_result(CResult.Success, '目录[{0}]处理顺利完成!'.format(ds_path_full_name))


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path2object('', '').execute()
