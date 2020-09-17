#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time : 2020/8/12 17:28
# @Author : 王西亚
# @File : job_dm_root_parser.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.core.Exceptions import DBException
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.metadata.base.job.c_dbBusJob import CDBBusJob
from imetadata.database.c_factory import CFactory
from imetadata.base.c_logger import CLogger


class job_dm_root_parser(CDBBusJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage 
set dstprocessid = '{0}', dstscanstatus = 2
where dstid = (
  select dstid  
  from   dm2_storage 
  where  dstscanstatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dstid as root_directory_id, dstunipath as root_directory from dm2_storage where dstprocessid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage 
set dstscanstatus = 1, dstprocessid = null 
where dstscanstatus = 2
        '''

    def process_mission(self, dataset):
        storage_id = dataset.value_by_name(0, 'root_directory_id', '')
        storage_root_path = dataset.value_by_name(0, 'root_directory', '')

        CLogger().debug('storage_id: {0}'.format(storage_id))
        sql_check_root_storage_dir_exist = '''
        select dsdid
        from dm2_storage_directory
        where dsdStorageId = '{0}' and dsdid = '{0}'
        '''.format(storage_id)

        sql_update_root_storage_dir = '''
        update dm2_storage_directory
        set dsdParentID = '-1', dsdDirectory = '', dsdDirtype = :dsdDirType
            , dsdDirectoryName = '', dsdPath = ''
            , dsdDirCreateTime = :dsddircreatetime, dsdDirLastModifyTime = :dsddirlastmodifytime
            , dsdLastModifyTime = Now()
        where dsdStorageId = '{0}' and dsdid = '{0}'
        '''.format(storage_id)

        sql_insert_root_storage_dir = '''
        insert into dm2_storage_directory(
            dsdid, dsdparentid, dsdstorageid, dsddirectory, dsddirtype, dsdlastmodifytime
            , dsddirectoryname, dsd_directory_valid, dsdpath, dsddircreatetime, dsddirlastmodifytime)
        values('{0}', '-1', '{0}', '', :dsdDirType, Now()
            , '', -1, '', :dsddircreatetime, :dsddirlastmodifytime
        )
        '''.format(storage_id)

        sql_on_mission_finished = '''
update dm2_storage 
set dstscanstatus = 0
where dstid = '{0}'
'''.format(storage_id)

        try:
            factory = CFactory()
            db = factory.give_me_db(self.get_mission_db_id())
            params = dict()
            params['dsdDirType'] = self.Dir_Type_Root
            if CFile.file_or_path_exist(storage_root_path):
                params['dsdDirCreateTime'] = CFile.file_modify_time(storage_root_path)
                params['dsddirlastmodifytime'] = CFile.file_modify_time(storage_root_path)

            if db.if_exists(sql_check_root_storage_dir_exist):
                db.execute(sql_update_root_storage_dir, params)
            else:
                db.execute(sql_insert_root_storage_dir, params)

            db.execute(sql_on_mission_finished)
            return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '存储扫描处理成功')
        except DBException as err:
            return CMetaDataUtils.merge_result(CMetaDataUtils.Exception, '存储扫描失败, 原因为{0}'.format(err.__str__()))


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_root_parser('', '').execute()
