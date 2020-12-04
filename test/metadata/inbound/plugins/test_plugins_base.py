# -*- coding: utf-8 -*- 
# @Time : 2020/12/4 08:55 
# @Author : 王西亚 
# @File : test_plugins_base.py

from abc import abstractmethod

import allure

from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class Plugins_Test_Base(CResource):
    _test_file_with_full_path_list = []
    _test_file_root_path = ''
    _test_file_parent_path = ''

    @abstractmethod
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return None

    @abstractmethod
    def file_name_with_rel_path_list(self) -> list:
        return []

    def init_before_test(self):
        plugins_info = self.create_plugins().get_information()
        plugins_catalog = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Catalog_Title, '')
        plugins_group = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Group_Title, '')
        plugins_type = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Type_Title, '')
        self._test_file_root_path = settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, '')
        self._test_file_parent_path = CFile.join_file(
            settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, ''),
            plugins_catalog,
            plugins_group,
            plugins_type
        )

        self._test_file_with_full_path_list = list()
        for file_type, file_name_with_rel_path in self.file_name_with_rel_path_list():
            self._test_file_with_full_path_list.append(
                (
                    file_type,
                    CFile.join_file(self._test_file_parent_path, file_name_with_rel_path)
                )
            )

    @allure.title("文件识别")  # 方法标题
    @allure.description("测试classified方法")  # 描述
    def test_classified(self):
        self.init_before_test()

        file_name_with_full_path_all_list = CFile.file_or_dir_fullname_of_path(self._test_file_root_path, True)
        for test_file_with_full_path in file_name_with_full_path_all_list:
            if CFile.is_file(test_file_with_full_path):
                file_type = self.FileType_File
            elif CFile.is_dir(test_file_with_full_path):
                file_type = self.FileType_Dir
            else:
                file_type = self.FileType_Layer

            file_info = CDMFilePathInfoEx(
                file_type,
                test_file_with_full_path,
                None,  # storage_id
                None,  # file_id
                None,  # file_parent_id
                None,  # owner_id
                self.DB_Server_ID_Default,
                None
            )
            plugins_obj = self.create_plugins(file_info)
            object_confirm, object_name = plugins_obj.classified()
            flag = object_confirm == self.Object_Confirm_IKnown
            if not flag:
                if test_file_with_full_path not in self._test_file_with_full_path_list:
                    flag = True
            allure.attach(
                '可能性为{0},识别出的对象名为{1}'.format(object_confirm, CUtils.any_2_str(object_name)),
                'classified方法信息',
                allure.attachment_type.TEXT
            )
            assert flag
