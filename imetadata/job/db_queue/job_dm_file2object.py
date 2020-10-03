# -*- coding: utf-8 -*- 
# @Time : 2020/9/15 12:54 
# @Author : 王西亚 
# @File : job_dm_file2object.py

from __future__ import absolute_import

from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.fileinfo.c_dmFileInfo import CDMFileInfo
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_file2object(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_file 
set dsfprocessid = '{0}', dsfscanstatus = 2
where dsfid = (
  select dsfid  
  from   dm2_storage_file 
  where  dsfscanstatus = 1 
  order by dsfaddtime 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage.dstunipath as query_rootpath
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage.dstid as query_storage_id
  , dm2_storage_file.dsfid as query_file_id
  , dm2_storage_file.dsfdirectoryid as query_directory_id
  , dm2_storage.dstunipath || dm2_storage_file.dsffilerelationname as query_file_full_name
  , dm2_storage.dstunipath || dm2_storage_directory.dsddirectory as query_file_full_path
  , dm2_storage_file.dsffilename as query_file_name
  , dm2_storage_file.dsffilemainname as query_file_main_name
  , dm2_storage_file.dsfext as query_file_ext
  , dm2_storage_file.dsffilemodifytime as query_file_modifytime
  , dm2_storage_file.dsffilesize as query_file_size
  , dm2_storage_file.dsffileattr as query_file_attr
  , dm2_storage_file.dsf_object_type as query_file_object_type
  , dm2_storage_file.dsf_object_confirm as query_file_object_confirm
  , dm2_storage_file.dsf_object_id as query_file_object_id
  , dm2_storage_file.dsfparentobjid as query_dir_parent_objid
from dm2_storage, dm2_storage_directory, dm2_storage_file
where dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  and dm2_storage_file.dsfdirectoryid = dm2_storage_directory.dsdid
  and dm2_storage_file.dsfprocessid ='{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_file 
set dsfscanstatus = 1
where dsfscanstatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
        ds_file_name_with_path = dataset.value_by_name(0, 'query_file_full_name', '')
        ds_dir_id = dataset.value_by_name(0, 'query_dir_id', '')
        ds_file_id = dataset.value_by_name(0, 'query_file_id', '')
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_owner_obj_id = dataset.value_by_name(0, 'query_dir_parent_objid', '')
        CLogger().debug('处理的文件为: {0}.{1}'.format(ds_file_id, ds_file_name_with_path))

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
        ds_rule_content = rule_ds.value_by_name(0, 'dsScanRule', '')

        file_obj = CDMFileInfo(self.FileType_File, ds_file_name_with_path,
                               ds_storage_id,
                               ds_file_id,
                               ds_dir_id,
                               ds_owner_obj_id,
                               self.get_mission_db_id(),
                               ds_rule_content)

        if not file_obj.__file_existed__:
            file_obj.db_update_status_on_file_invalid()
            return CResult.merge_result(CResult.Success, '文件[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_file_name_with_path))
        else:
            file_obj.db_file2object()

        sql_update_directory_status = '''
        update dm2_storage_file
        set dsfscanstatus = 0, dsflastmodifytime = now()
        where dsfid = :dsfid
        '''
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_directory_status, {'dsfid': ds_file_id})

        return CResult.merge_result(CResult.Success, '文件[{0}]处理顺利完成!'.format(ds_file_name_with_path))


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_file2object('', '').execute()
