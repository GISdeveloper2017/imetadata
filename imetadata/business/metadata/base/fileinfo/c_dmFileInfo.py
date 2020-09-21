# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:33 
# @Author : 王西亚 
# @File : c_dmFileInfo.py

from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.database.c_factory import CFactory


class CDMFileInfo(CDMFilePathInfoEx):
    def custom_init(self):
        """
        自定义初始化方法
        :return:
        """
        engine = CFactory().give_me_db(self.__db_server_id__)
        if self.__my_id__ is None:
            self.__ds_file_or_path__ = engine.one_row('''
            select dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext, 
                dsffilecreatetime, dsffilemodifytime, dsffilevalid, 
                dsf_object_type, dsf_object_confirm, dsf_object_id, dsffileattr, dsffilesize, dsfparentobjid
            from dm2_storage_file
            where dsfstorageid = :dsfStorageID and dsfdirectoryid = :dsfDirectoryId and dsffilerelationname = :dsfFileRelationName
            ''', {'dsfStorageID': self.__storage_id__, 'dsfDirectoryId': self.__parent_id__,
                  'dsfFileRelationName': self.__file_name_with_rel_path__})
            if not self.__ds_file_or_path__.is_empty():
                self.__my_id__ = self.__ds_file_or_path__.value_by_name(0, 'dsfid', None)
            if self.__my_id__ is None:
                self.__my_id__ = CMetaDataUtils.one_id()
        else:
            self.__ds_file_or_path__ = engine.one_row('''
                select dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext, 
                    dsffilecreatetime, dsffilemodifytime, dsffilevalid, 
                    dsf_object_type, dsf_object_confirm, dsf_object_id, dsffileattr, dsffilesize, dsfparentobjid
                from dm2_storage_file
                where dsfid = :dsfID
                ''', {'dsfid': self.__my_id__})

    def db_check_and_update(self):
        """
        检查并更新dm2_storage_file表中记录
        :return:
        """
        if not self.__ds_file_or_path__.is_empty():
            # 如果记录已经存在
            db_file_modify_time = self.__ds_file_or_path__.value_by_name(0, 'dsddirlastmodifytime', '')
            db_file_size = self.__ds_file_or_path__.value_by_name(0, 'dsffilesize', 0)
            if CMetaDataUtils.equal_ignore_case(CMetaDataUtils.any_2_str(db_file_modify_time),
                                                CMetaDataUtils.any_2_str(self.__file_modify_time__)) and (
                    db_file_size == self.__file_size__):
                CLogger().info('文件[{0}]的大小和最后修改时间, 和库中登记的没有变化, 文件将被设置为忽略刷新! '.format(self.__file_name_with_full_path__))
                CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_file set dsfScanStatus = 0, dsffilevalid = -1
                    where dsfid = :dsfid 
                    ''', {'dsfid': self.__my_id__})
            else:
                CLogger().info('文件[{0}]的大小和最后修改时间, 和库中登记的有变化, 文件将被设置为重新刷新! '.format(self.__file_name_with_full_path__))
                CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_file set dsfScanStatus = 1, dsffilevalid = -1
                    where dsfid = :dsfid 
                    ''', {'dsfid': self.__my_id__})
        else:
            CLogger().info('文件[{0}]未在库中登记, 系统将登记该记录! '.format(self.__file_name_with_full_path__))
            self.db_insert()

    def db_insert(self):
        """
        将当前目录, 创建一条新记录到dm2_storage_directory表中
        :return:
        """
        sql_insert = '''
        insert into dm2_storage_file(
            dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext
            , dsffilecreatetime, dsffilemodifytime, dsfaddtime, dsflastmodifytime, dsffilevalid
            , dsfscanstatus, dsfprocessid, dsf_object_type, dsf_object_confirm, dsf_object_id
            , dsffileattr, dsffilesize, dsfparentobjid) 
        values(
            :dsfid, :dsfstorageid, :dsfdirectoryid, :dsffilerelationname, :dsffilename, :dsffilemainname, :dsfext
            , :dsffilecreatetime, :dsffilemodifytime, now(), now(), -1
            , 1, null, null, 0, null
            , 32, :dsffilesize, :dsfparentobjid)
        '''
        params = dict()
        params['dsfid'] = self.__my_id__
        params['dsfdirectoryid'] = self.__parent_id__
        params['dsfstorageid'] = self.__storage_id__
        params['dsffilerelationname'] = self.__file_name_with_rel_path__
        params['dsffilename'] = self.__file_name_without_path__
        params['dsffilemainname'] = self.__file_main_name__
        params['dsfext'] = self.__file_ext__
        params['dsffilecreatetime'] = self.__file_create_time__
        params['dsffilemodifytime'] = self.__file_modify_time__
        params['dsffilesize'] = self.__file_size__
        params['dsfparentobjid'] = self.__owner_obj_id__
        CFactory().give_me_db(self.__db_server_id__).execute(sql_insert, params)