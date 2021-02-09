# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4016_landsat5 import plugins_4016_landsat5
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("landsat5目录文件")  # 模块标题
class Test_plugins_4016_landsat5_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4016_landsat5(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'LT51190341984265HAJ00-119-34-80',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'LT51190341984265HAJ00-119-34-80'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'LT51190351984137HAJ00-119-35-80',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'LT51190351984137HAJ00-119-35-80'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'LT51200341988123HAJ00-120-34-80',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'LT51200341988123HAJ00-120-34-80'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'LT51210351988242HAJ00_121-35_80',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'LT51210351988242HAJ00_121-35_80'
            }
        ]


if __name__ == '__main__':
    pytest.main()
