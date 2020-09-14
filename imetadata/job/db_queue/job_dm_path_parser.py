# -*- coding: utf-8 -*- 
# @Time : 2020/9/11 15:57 
# @Author : 王西亚 
# @File : job_dm_path_parser.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.core.Exceptions import DBException
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.database.c_factory import CFactory
from imetadata.base.c_logger import CLogger
from imetadata.job.db_queue.c_dmBaseJob import CDMBaseJob


class job_dm_path_parser(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscandirprocessid = '{0}', dsdscandirstatus = 2
where dsdid = (
  select dsdid  
  from   dm2_storage_directory 
  where  dsdscandirstatus = 1 
    and dsdscanstatus = 0  
    and dsd_directory_valid = -1
    and dsddirtype <> '2'
  order by dsddirscanpriority desc, dsdaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage.dstunipath as query_rootpath
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage_directory.dsdid as query_dir_id
  , dm2_storage_directory.dsddirtype as query_dir_type
  , dm2_storage_directory.dsddirscanpriority as query_dir_scan_priority
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dstOtherOption as query_storage_OtherOption  
  , COALESCE(dm2_storage_directory.dsd_object_id, dm2_storage_directory.dsdparentobjid)  as query_dir_parent_objid
  , dm2_storage_object.dsoobjecttype as query_dir_parent_objtype
from dm2_storage_directory 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  left join dm2_storage_object on dm2_storage_object.dsoid = COALESCE(dm2_storage_directory.dsd_object_id, dm2_storage_directory.dsdparentobjid) 
where dm2_storage_directory.dsdscandirprocessid = '{0}'
            '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscandirstatus = 1, dsdscandirprocessid = null 
where dsdscandirstatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
        ds_root_path = dataset.value_by_name(0, 'query_rootpath', '')
        ds_storage_option = dataset.value_by_name(0, 'query_storage_OtherOption', '')

        if ds_subpath == '':
            ds_subpath = ds_root_path
        else:
            ds_subpath = CFile.join_file(ds_root_path, ds_subpath)
        CLogger().debug('处理的子目录为: {0}'.format(ds_subpath))

        if not CFile.file_or_path_exist(ds_subpath):
            return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_subpath))
        else:
            file_list = CFile.file_or_subpath_of_path(ds_subpath)
            for file_name in file_list:
                file_name_with_path = CFile.join_file(ds_subpath, file_name)
                ds_path_with_relation_path = CFile.file_relation_path(file_name_with_path, ds_root_path)
                if super().bus_white_black_valid(ds_path_with_relation_path, ds_storage_option,
                                              CFile.is_dir(file_name_with_path)):
                    if CFile.is_dir(file_name_with_path):
                        CLogger().debug('发现子目录: {0}'.format(file_name_with_path))
                        self.save_subpath(dataset, file_name_with_path)
                    else:
                        CLogger().debug('发现文件: {0}'.format(file_name_with_path))
                        self.save_file(dataset, file_name_with_path)

            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_directory
                set dsdscandirstatus = 0, dsddirscanpriority = 0
                where dsdid = '{0}'
                '''.format(dataset.value_by_name(0, 'query_dir_id', ''))
            )
            return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_subpath))

    def save_subpath(self, dataset, file_name_with_path):
        """
        在这里将指定目录入库
        :param dataset: 数据集
        :param file_name_with_path: 完整路径的目录名
        :return:
        """
        storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_root_path = dataset.value_by_name(0, 'query_rootpath', '')
        ds_path_with_relation_path = CFile.file_relation_path(file_name_with_path, ds_root_path)

        sql_get_exist = '''
select dsdid as exist_dir_id, dsddirlastmodifytime
from dm2_storage_directory 
where dsddirectory = :dsdDirectory and dsdstorageid = :dsdStorageID
        '''

        params = dict()
        params['dsdDirectory'] = ds_path_with_relation_path
        params['dsdStorageID'] = storage_id
        dataset_existed = CFactory().give_me_db(self.get_mission_db_id()).one_row(sql_get_exist, params)
        if dataset_existed.is_empty():
            sql_insert = '''
            insert into dm2_storage_directory(
                dsdid, dsdparentid, dsdstorageid, dsddirectory, dsddirtype
                , dsddirectoryname, dsdpath, dsddircreatetime, dsddirlastmodifytime, dsdparentobjid
            ) VALUES(
                uuid_generate_v4(), :dsdparentid, :dsdstorageid, :dsddirectory, :dsddirtype
                , :dsddirectoryname, :dsdpath, :dsddircreatetime, :dsddirlastmodifytime, :dsdparentobjid     
            ) 
            '''
            params = dict()
            params['dsdparentid'] = dataset.value_by_name(0, 'query_dir_id', '')
            params['dsdstorageid'] = storage_id
            params['dsddirectory'] = ds_path_with_relation_path
            params['dsddirtype'] = self.Dir_Type_Directory
            params['dsddirectoryname'] = CFile.file_name(file_name_with_path)
            params['dsdpath'] = CFile.file_path(ds_path_with_relation_path)
            params['dsddircreatetime'] = CFile.file_create_time(file_name_with_path)
            params['dsddirlastmodifytime'] = CFile.file_modify_time(file_name_with_path)
            params['dsdparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', None)

            CFactory().give_me_db(self.get_mission_db_id()).execute(sql_insert, params)
        else:
            file_m_date = CFile.file_modify_time(file_name_with_path)
            if file_m_date == dataset_existed.value_by_name(0, 'dsddirlastmodifytime', None):
                return CMetaDataUtils.merge_result(CMetaDataUtils.Success,
                                                   '目录[{0}]自上次入库后无变化, 本次将被忽略!'.format(file_name_with_path))
            else:
                sql_update = '''
                update dm2_storage_directory
                set dsdparentid = :dsdparentid
                    , dsddirectory = :dsddirectory
                    , dsddirtype = :dsddirtype
                    , dsddirectoryname = :dsddirectoryname
                    , dsdpath = :dsdpath
                    , dsddircreatetime = :dsddircreatetime
                    , dsddirlastmodifytime = :dsddirlastmodifytime
                    , dsdparentobjid = :dsdparentobjid    
                where dsdid = :dsdid
                '''
                params = dict()
                params['dsdid'] = dataset_existed.value_by_name(0, 'exist_dir_id', '')
                params['dsddirectory'] = ds_path_with_relation_path
                params['dsddirtype'] = self.Dir_Type_Directory
                params['dsddirectoryname'] = CFile.file_name(file_name_with_path)
                params['dsdpath'] = CFile.file_path(ds_path_with_relation_path)
                params['dsddircreatetime'] = CFile.file_create_time(file_name_with_path)
                params['dsddirlastmodifytime'] = CFile.file_modify_time(file_name_with_path)
                params['dsdparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', None)

                CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update, params)

    def save_file(self, dataset, file_name_with_path):
        """
        在这里将指定文件入库
        todo 文件入库
        :param dataset: 数据集
        :param file_name_with_path: 完整路径的文件名
        :return:
        """
        pass


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path_parser('', '').execute()
