# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 10:14 
# @Author : 王西亚 
# @File : c_dmFilePathInfoEx.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CDMFilePathInfoEx(CFileInfoEx):
    __db_server_id__: str

    __storage_id__: str
    __my_id__ = None

    def __init__(self, file_name_with_full_path, root_path, storage_id, file_or_path_id, db_server_id):
        """

        :param file_name_with_full_path:
        :param root_path:
        :param storage_id: 必须提供
        :param file_or_path_id:
            如果为None, 则首先根据文件相对路径和storage_id, 查找数据库中登记的标识, 如果不存在, 则自行创建uuid;
            如果不为空, 则表明数据库中已经存储该文件标识
        """
        super().__init__(file_name_with_full_path, root_path)
        self.__storage_id__ = storage_id
        self.__my_id__ = file_or_path_id
        self.__db_server_id__ = db_server_id
        self.custom_init()

    def custom_init(self):
        """
        自定义初始化方法
        :return:
        """
        pass

    def white_black_valid(self, ds_storage_option):
        """
        检查指定文件是否符合白名单, 黑名单验证
        """
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

    def plugins_classified(self) -> CPlugins:
        target = self.__file_path_with_rel_path__
        target_type = self.__file_type__
        target_id = self.__my_id__
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_list = CFile.search_file_or_subpath_of_path(path,
                                                                 '{0}_*.{1}'.format(self.Name_Plugins, self.FileExt_Py))
        for file_name_with_path in plugins_file_list:
            file_main_name = CFile.file_main_name(file_name_with_path)
            class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name,
                                                                   target, target_type, target_id)
            object_confirm, object_name = class_classified_obj.classified()
            if object_confirm != self.Object_Confirm_IUnKnown:
                CLogger().debug(
                    '{0} is plugins_classified as {1}.{2}'.format(target, class_classified_obj.get_group_name(),
                                                                  class_classified_obj.get_id()))
                return class_classified_obj
        else:
            return None

    def plugins(self, plugins_id: str) -> CPlugins:
        target = self.__file_path_with_rel_path__
        target_type = self.__file_type__
        target_id = self.__my_id__
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_list = CFile.search_file_or_subpath_of_path(path,
                                                                 '{0}_*.{1}'.format(self.Name_Plugins, self.FileExt_Py))
        for file_name_with_path in plugins_file_list:
            file_main_name = CFile.file_main_name(file_name_with_path)
            if CMetaDataUtils.plugins_id_by_file_main_name(file_main_name) == plugins_id:
                class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name,
                                                                       target, target_type, target_id)
                return class_classified_obj
        else:
            return None
