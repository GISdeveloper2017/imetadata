# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:45 
# @Author : 王西亚 
# @File : c_dmPathInfo.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.job.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.database.c_factory import CFactory


class CDMPathInfo(CDMFilePathInfoEx):

    def db_update_status_on_path_invalid(self):
        """
        处理目录不存在时的业务
        :return:
        """
        path_name_with_relation_path = CFile.join_file(self.__file_path_with_rel_path__, '')

        params = dict()
        params['dsdStorageID'] = self.__storage_id__
        params['dsdSubDirectory'] = path_name_with_relation_path

        sql_update_file_invalid = '''
            update dm2_storage_file
            set dsffilevalid = 0, dsfscanstatus = 0
            where dsfdirectoryid in (
                select dsdid
                from dm2_storage_directory
                where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
            )
            '''

        sql_update_path_invalid = '''
            update dm2_storage_directory
            set dsd_directory_valid = 0, dsdscanstatus = 0, dsdscanfilestatus = 0, dsdscandirstatus = 0
            where dsdstorageid = :dsdStorageID and position(:dsdSubDirectory in dsddirectory) = 1
            '''

        CFactory().give_me_db(self.__db_server_id__).execute(sql_update_file_invalid, params)
        CFactory().give_me_db(self.__db_server_id__).execute(sql_update_path_invalid, params)

    def path2object(self):
        """
        处理目录存在时的业务:
        1. 检查目录下是否有metadata.rule
        :return:
        """
        sql_get_object_info = '''
            select dsd_object_type, dsd_object_id, dsd_object_confirm
            from dm2_storage_directory
            where dsdid = :dsdID
        '''
        params = dict()
        params['dsdid'] = self.__my_id__
        dataset = CFactory().give_me_db(self.__db_server_id__).one_row(sql_get_object_info, params)

        query_dir_object_id = dataset.value_by_name(0, 'dsd_object_id', '')
        query_dir_object_type = dataset.value_by_name(0, 'dsd_object_type', '')
        params = dict()
        params['dsdID'] = dataset.value_by_name(0, 'query_dir_id', '')
        if CFile.file_or_path_exist(CFile.join_file(self.__file_path__, self.FileName_MetaData_Rule)):
            try:
                params['dsdScanRule'] = CXml.file_2_str(
                    CFile.join_file(self.__file_path__, self.FileName_MetaData_Rule))
            except:
                params['dsdScanRule'] = None

        sql_update_path_valid = '''
            update dm2_storage_directory
            set dsd_directory_valid = -1, dsdscanrule = :dsdScanRule
            where dsdid = :dsdID
            '''

        CFactory().give_me_db(self.__db_server_id__).execute(sql_update_path_valid, params)

        classified_obj = self.plugins_classified()
        if classified_obj is None:
            sql_update_path_object = '''
                update dm2_storage_directory
                set dsd_object_confirm = 0, dsd_object_id = null, dsd_object_type = null
                    , dsdscanfilestatus = 1, dsdscandirstatus = 1
                where dsdid = :dsdid
                '''

            CFactory().give_me_db(self.__db_server_id__).execute(sql_update_path_object, params)
            if query_dir_object_id != '':
                sql_clear_old_path_object = '''
                    delete from dm2_storage_object where dsoid = :dsoid
                    '''
                params = dict()
                params['dsoid'] = query_dir_object_id

                CFactory().give_me_db(self.__db_server_id__).execute(sql_clear_old_path_object, params)
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

                    CFactory().give_me_db(self.__db_server_id__).execute(sql_clear_old_path_object, params)

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
                CFactory().give_me_db(self.__db_server_id__).execute(sql_insert_object, params)

                sql_update_path_object = '''
                        update dm2_storage_directory
                        set dsd_object_confirm = :ObjectConfirm, dsd_object_id = :Object_ID, dsd_object_type = :ObjectType
                            , dsdscanfilestatus = 0, dsdscandirstatus = 0
                        where dsdid = :dsdid
                        '''
                params = dict()
                params['dsdid'] = self.__my_id__
                params['ObjectConfirm'] = object_confirm
                params['Object_ID'] = new_dso_id
                params['ObjectType'] = object_type
                CFactory().give_me_db(self.__db_server_id__).execute(sql_update_path_object, params)

    def update_db(self):
        pass
