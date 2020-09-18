# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:33 
# @Author : 王西亚 
# @File : c_dmFileInfo.py

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.job.c_dmFilePathInfoEx import CDMFilePathInfoEx
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
            select dsfid, dsfstorageid, dsfdirectoryid, dsffilerelationname, dsffilename, dsffilemainname, dsfext, dsffilecreatetime, dsffilemodifytime, dsfaddtime, dsflastmodifytime, dsffilevalid, dsfscanstatus, dsfprocessid, dsf_object_type, dsf_object_confirm, dsf_object_id, dsffileattr, dsffilesize, dsfparentobjid from dm2_storage_file
            where dsdstorageid = :dsdStorageID and dsddirectory = :dsdDirectory'
            ''', {'dsdStorageID': self.__storage_id__, 'dsdDirectory': self.__file_path_with_rel_path__})
            if not self.__ds_file_or_path__.is_empty():
                self.__my_id__ = self.__ds_file_or_path__.value_by_name(0, 'dsfid', None)
            if self.__my_id__ is None:
                self.__my_id__ = CMetaDataUtils.one_id()
        else:
            self.__ds_file_or_path__ = engine.one_row(
                'select dsdid, dsdparentid, dsddirectory, dsddirtype, dsddirectoryname, dsd_object_type, \
                        dsd_object_confirm, dsd_object_id, dsd_directory_valid, dsdpath, dsddircreatetime, \
                        dsddirlastmodifytime, dsdparentobjid, dsdscanrule from dm2_storage_directory \
                        where dsdid = :dsdID',
                {'dsdid': self.__my_id__})

    def db_check_and_update(self):
        """
        检查并更新dm2_storage_directory表中记录
        :return:
        """
        if not self.__ds_file_or_path__.is_empty():
            # 如果记录已经存在
            db_path_modify_time = self.__ds_file_or_path__.value_by_name(0, 'dsddirlastmodifytime', '')
            if CMetaDataUtils.equal_ignore_case(CMetaDataUtils.any_2_str(db_path_modify_time),
                                                CMetaDataUtils.any_2_str(self.__file_modify_time__)):
                CLogger().info('目录[{0}]的最后修改时间, 和库中登记的没有变化, 子目录将被设置为忽略刷新! '.format(self.__file_name_with_full_path__))
                CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_directory set dsdScanStatus = 0, dsdScanFileStatus = 0, dsd_directory_valid = -1
                    where dsdid = :dsdid 
                    ''', {'dsdid': self.__my_id__})
            else:
                CLogger().info('目录[{0}]的最后修改时间, 和库中登记的有变化, 子目录将被设置为重新刷新! '.format(self.__file_name_with_full_path__))
                CFactory().give_me_db(self.__db_server_id__).execute('''
                    update dm2_storage_directory set dsdScanStatus = 1, dsdScanFileStatus = 1, dsd_directory_valid = -1
                    where dsdid = :dsdid 
                    ''', {'dsdid': self.__my_id__})
        else:
            CLogger().info('目录[{0}]未在库中登记, 系统将登记该记录! '.format(self.__file_name_with_full_path__))
            self.db_insert()

    def db_insert(self):
        """
        将当前目录, 创建一条新记录到dm2_storage_directory表中
        :return:
        """
        sql_insert = '''
        insert into dm2_storage_directory(dsdid, dsdparentid, dsdstorageid, dsddirectory, dsddirtype, dsdlastmodifytime, 
            dsddirectoryname, dsdpath, dsddircreatetime, dsddirlastmodifytime, dsdparentobjid, 
            dsdscanstatus, dsdscanfilestatus, dsdscandirstatus, dsd_directory_valid) 
        values(:dsdid, :dsdparentid, :dsdstorageid, :dsddirectory, :dsddirtype, now(), 
            :dsddirectoryname, :dsdpath, :dsddircreatetime, :dsddirlastmodifytime, :dsdparentobjid,
            1, 1, 1, -1)
        '''
        params = dict()
        params['dsdid'] = self.__my_id__
        params['dsdparentid'] = self.__parent_id__
        params['dsdstorageid'] = self.__storage_id__
        params['dsddirectory'] = self.__file_name_with_rel_path__
        params['dsddirtype'] = self.FileType_Dir
        params['dsddirectoryname'] = self.__file_name_without_path__
        params['dsdpath'] = self.__file_path_with_rel_path__
        params['dsddircreatetime'] = self.__file_create_time__
        params['dsddirlastmodifytime'] = self.__file_modify_time__
        params['dsdparentobjid'] = self.__owner_obj_id__
        CFactory().give_me_db(self.__db_server_id__).execute(sql_insert, params)