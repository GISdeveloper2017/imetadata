# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 10:14 
# @Author : 王西亚 
# @File : c_dmFilePathInfoEx.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.database.c_factory import CFactory


class CDMFilePathInfoEx(CFileInfoEx):
    __db_server_id__ = None
    __parent_id__ = None
    __owner_obj_id__ = None

    __storage_id__ = None
    __my_id__ = None

    __ds_storage__ = None
    __ds_file_or_path__ = None

    def __init__(self, file_type, file_name_with_full_path, storage_id, file_or_path_id, parent_id, owner_obj_id,
                 db_server_id, rule_content):
        """

        :param file_name_with_full_path:
        :param root_path:
        :param storage_id: 必须提供
        :param file_or_path_id:
            如果为None, 则首先根据文件相对路径和storage_id, 查找数据库中登记的标识, 如果不存在, 则自行创建uuid;
            如果不为空, 则表明数据库中已经存储该文件标识
        """
        self.__storage_id__ = storage_id
        self.__my_id__ = file_or_path_id
        self.__db_server_id__ = db_server_id
        self.__parent_id__ = parent_id
        self.__owner_obj_id__ = owner_obj_id

        self.__ds_storage__ = CFactory().give_me_db(self.__db_server_id__).one_row(
            'select dstid, dsttitle, dstunipath, dstotheroption from dm2_storage where dstid = :dstID',
            {'dstid': self.__storage_id__})

        root_path = self.__ds_storage__.value_by_name(0, 'dstunipath', '')
        super().__init__(file_type, file_name_with_full_path, root_path, rule_content)
        self.custom_init()

    @property
    def db_server_id(self):
        return self.__db_server_id__

    def custom_init(self):
        """
        自定义初始化方法
        :return:
        """
        pass

    def db_init_object_of_directory_by_id(self, dir_id):
        sql_update_path_object = '''
            update dm2_storage_directory
            set dsd_object_confirm = 0, dsd_object_id = null, dsd_object_type = null
                , dsdscanfilestatus = 1, dsdscandirstatus = 1, dsd_directory_valid = -1
            where dsdid = :dsdid
            '''

        CFactory().give_me_db(self.__db_server_id__).execute(sql_update_path_object, {'dsdid': dir_id})

    def db_delete_object_by_id(self, object_id):
        if object_id == '' or object_id is None:
            return

        sql_delete_object_by_id = '''
        delete from dm2_storage_object
        where dsoid = :dsoID
        '''

        sql_delete_object_details_by_id = '''
        delete from dm2_storage_obj_detail
        where dodid = :dsoID
        '''

        engine = CFactory().give_me_db(self.__db_server_id__)
        session = engine.give_me_session()
        try:
            engine.session_execute(session, sql_delete_object_details_by_id, {'dsoid': object_id})
            engine.session_execute(session, sql_delete_object_by_id, {'dsoid': object_id})
            engine.session_commit(session)
        except Exception as error:
            CLogger().warning('数据库处理出现异常, 错误信息为: {0}'.format(error.__str__))
            engine.session_rollback(session)
        finally:
            engine.session_close(session)

    def white_black_valid(self):
        """
        检查指定文件是否符合白名单, 黑名单验证
        """
        ds_storage_option = self.__ds_storage__.value_by_name(0, 'dstotheroption', None)
        if ds_storage_option == '' or ds_storage_option is None:
            return True

        dir_filter_white_list = CJson.json_attr_value(ds_storage_option,
                                                      CJson.json_join(self.Name_Filter, self.Name_Directory,
                                                                      self.Name_White_List), '')
        dir_filter_black_list = CJson.json_attr_value(ds_storage_option,
                                                      CJson.json_join(self.Name_Filter, self.Name_Directory,
                                                                      self.Name_Black_List), '')
        file_filter_white_list = CJson.json_attr_value(ds_storage_option,
                                                       CJson.json_join(self.Name_Filter, self.Name_File,
                                                                       self.Name_White_List), '')
        file_filter_black_list = CJson.json_attr_value(ds_storage_option,
                                                       CJson.json_join(self.Name_Filter, self.Name_File,
                                                                       self.Name_Black_List), '')

        result = True
        if self.__file_type__ != self.FileType_Unknown:
            if (dir_filter_white_list != '') and (dir_filter_black_list != ''):
                result = CFile.file_match(self.__file_path_with_rel_path__, dir_filter_white_list) and (
                    not CFile.file_match(self.__file_path_with_rel_path__, dir_filter_black_list))
            elif dir_filter_white_list != '':
                result = CFile.file_match(self.__file_path_with_rel_path__, dir_filter_white_list)
            elif dir_filter_black_list != '':
                result = not CFile.file_match(self.__file_path_with_rel_path__, dir_filter_black_list)

        if not result:
            return result

        if self.__file_type__ == self.FileType_File:
            if (file_filter_white_list != '') and (file_filter_black_list != ''):
                return CFile.file_match(self.__file_name_without_path__, file_filter_white_list) and (
                    not CFile.file_match(self.__file_name_without_path__, file_filter_black_list))
            elif file_filter_white_list != '':
                return CFile.file_match(self.__file_name_without_path__, file_filter_white_list)
            elif file_filter_black_list != '':
                return not CFile.file_match(self.__file_name_without_path__, file_filter_black_list)
            else:
                return True
