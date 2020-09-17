# -*- coding: utf-8 -*- 
# @Time : 2020/9/15 12:54 
# @Author : 王西亚 
# @File : job_dm_file2object.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_xml import CXml
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.metadata.base.job.c_dbBusJob import CDBBusJob
from imetadata.database.c_factory import CFactory
from imetadata.base.c_logger import CLogger


class job_dm_file2object(CDBBusJob):
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
        ds_rootpath = dataset.value_by_name(0, 'query_rootpath', '')

        if ds_subpath == '':
            ds_path_full_name = ds_rootpath
        else:
            ds_path_full_name = CFile.join_file(ds_rootpath, ds_subpath)
        CLogger().debug('处理的子目录为: {0}'.format(ds_path_full_name))

        if not CFile.file_or_path_exist(ds_path_full_name):
            self.bus_path_invalid(dataset, ds_path_full_name)
            return CMetaDataUtils.merge_result(CMetaDataUtils.Success, '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_path_full_name))
        else:
            self.bus_path_valid(dataset, ds_path_full_name)

    def bus_path_invalid(self, dataset, path_name_with_full_path):
        """
        处理目录不存在时的业务
        :param dataset:
        :param path_name_with_full_path:
        :return:
        """
        path_name_with_relation_path = dataset.value_by_name(0, 'query_subpath', '')
        path_name_with_relation_path = CFile.join_file(path_name_with_relation_path, '')

        params = dict()
        params['dsdStorageID'] = dataset.value_by_name(0, 'query_storage_id', '')
        params['dsdSubDirectory'] = path_name_with_relation_path

        sql_update_file_invalid = '''
        update dm2_storage_file
        set dsffilevalid = 0, dsfscanstatus = 0
        where dsfdirectoryid in (
            select dsdid
            from dm2_storage_directory
            where dsdstorageid = '1'
              and dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
        )
        '''

        sql_update_path_invalid = '''
update dm2_storage_directory
set dsd_directory_valid = 0, dsdscanstatus = 0, dsdscanfilestatus = 0, dsdscandirstatus = 0
where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
        '''

        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_file_invalid, params)
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_path_invalid, params)

    def bus_path_valid(self, dataset, path_name_with_full_path):
        """
        处理目录存在时的业务:
        1. 检查目录下是否有metadata.rule
        :param dataset:
        :param path_name_with_full_path:
        :return:
        """

        query_dir_object_id = dataset.value_by_name(0, 'query_dir_object_id', '')
        query_dir_object_type = dataset.value_by_name(0, 'query_dir_object_type', '')
        params = dict()
        params['dsdID'] = dataset.value_by_name(0, 'query_dir_id', '')
        if CFile.file_or_path_exist(CFile.join_file(path_name_with_full_path, self.FileName_MetaData_Rule)):
            try:
                params['dsdScanRule'] = CXml.file_2_str(CFile.join_file(path_name_with_full_path, self.FileName_MetaData_Rule))
            except:
                params['dsdScanRule'] = None

        sql_update_path_valid = '''
        update dm2_storage_directory
        set dsd_directory_valid = -1, dsdscanrule = :dsdScanRule
        where dsdid = :dsdID
        '''

        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_path_valid, params)

        classified_obj = super().plugins_classified(dataset.value_by_name(0, 'query_subpath_name', ''), self.Plugins_Target_Type_Path, dataset.value_by_name(0, 'query_dir_id', ''))
        if classified_obj is None:
            sql_update_path_object = '''
            update dm2_storage_directory
            set dsd_object_confirm = 0, dsd_object_id = null, dsd_object_type = null
                , dsdscanfilestatus = 1, dsdscandirstatus = 1
            where dsdid = :dsdid
            '''

            CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_path_object, params)
            if query_dir_object_id != '':
                sql_clear_old_path_object = '''
                delete from dm2_storage_object where dsoid = :dsoid
                '''
                params = dict()
                params['dsoid'] = query_dir_object_id

                CFactory().give_me_db(self.get_mission_db_id()).execute(sql_clear_old_path_object, params)
        else:
            object_name = classified_obj.get_classified_object_name()
            object_confirm = classified_obj.get_classified_object_confirm()
            object_type = classified_obj.get_id()
            if not CMetaDataUtils.equal_ignore_case(object_type, query_dir_object_type):
                if query_dir_object_type != '':
                    sql_clear_old_path_object = '''
                    delete from dm2_storage_object where dsoid = :dsoid
                    '''
                    params = dict()
                    params['dsoid'] = query_dir_object_id

                    CFactory().give_me_db(self.get_mission_db_id()).execute(sql_clear_old_path_object, params)

                new_dso_id = CMetaDataUtils.one_id()
                sql_insert_object = '''
                insert into dm2_storage_object(dsoid, dsoobjectname, dsoobjecttype, dsodatatype, dsoalphacode, dsoaliasname, dsoparentobjid) 
                values(:dsoid, :dsoobjectname, :dsoobjecttype, :dsodatatype, :dsoalphacode, :dsoaliasname, :dsoparentobjid)
                '''
                params = dict()
                params['dsoid'] = new_dso_id
                params['dsoobjectname'] = object_name
                params['dsoobjecttype'] = object_type
                params['dsodatatype'] = 'dir'
                params['dsoalphacode'] = object_name
                params['dsoaliasname'] = object_name
                params['dsoparentobjid'] = dataset.value_by_name(0, 'query_dir_parent_objid', '')
                CFactory().give_me_db(self.get_mission_db_id()).execute(sql_insert_object, params)

                sql_update_path_object = '''
                update dm2_storage_directory
                set dsd_object_confirm = :ObjectConfirm, dsd_object_id = :Object_ID, dsd_object_type = :ObjectType
                    , dsdscanfilestatus = 0, dsdscandirstatus = 0
                where dsdid = :dsdid
                '''
                params = dict()
                params['dsdid'] = dataset.value_by_name(0, 'query_dir_id', '')
                params['ObjectConfirm'] = object_confirm
                params['Object_ID'] = new_dso_id
                params['ObjectType'] = object_type
                CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_path_object, params)

        sql_update_directory_status = '''
        update dm2_storage_directory
        set dsdscanstatus = 0, dsdlastmodifytime = now()
        where dsdid = :dsdid
        '''
        params = dict()
        params['dsdid'] = dataset.value_by_name(0, 'query_dir_id', '')
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_directory_status, params)


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_file2object('', '').execute()
