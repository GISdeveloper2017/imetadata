# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4027_wordview_or_quickbrid import \
    plugins_4027_wordview_or_quickbrid
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("WordView星或Quickbird星目录文件")  # 模块标题
class Test_plugins_4027_wordview_or_quickbrid_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4027_wordview_or_quickbrid(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: '056007609080_01',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '056007609080_01'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: '056221192010_01',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '056221192010_01'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: '059336717010_01',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '059336717010_01'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: '059629130020_01',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '059629130020_01'
            }
        ]


if __name__ == '__main__':
    pytest.main()
