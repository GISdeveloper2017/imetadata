# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest

import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_3001_gdb import plugins_3001_gdb
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


#  运行前建议注释掉CPlugins类中parser_metadata_with_qa方法中853行，不然新建的layer污染数据库
@allure.feature("gdb")  # 模块标题
class Test_plugins_3001_gdb(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_3001_gdb(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'gdb数据集{0}FileGeodb.gdb'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'FileGeodb'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'gdb数据集{0}FileGeodb2.gdb'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'FileGeodb2'
            }
            # ,
            # {
            #     self.Name_Test_File_Type: self.FileType_Dir,
            #     self.Name_Test_file_path: 'gdb数据集{0}FileGeoNone.gdb'.format(CFile.sep()),
            #     self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
            #     self.Name_Test_object_name: 'FileGeoNone'
            # }
        ]

    def init_before_test(self):
        plugins_info = self.create_plugins().get_information()
        plugins_catalog = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Catalog_Title, '')
        plugins_group = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Group_Title, '')
        plugins_type = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Type, '')
        self._test_file_root_path = settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, '')
        self._test_file_parent_path = CFile.join_file(
            settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, ''),
            plugins_catalog,
            plugins_group
        )


if __name__ == '__main__':
    pytest.main()
