# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_8040_third_survey_block import \
    plugins_8040_third_survey_block
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("三调分块")  # 模块标题
class Test_plugins_8040_third_survey_block(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_8040_third_survey_block(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}632701BJ2+GF1+GJ1+GF2+ZY3DOM02.img'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '632701BJ2+GF1+GJ1+GF2+ZY3DOM02'
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}632701BJ2+GF1+GJ1+GF2+ZY3DOM02.img.aux.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}632701BJ2+GF1+GJ1+GF2+ZY3DOM02.img.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}632701BJ2+GF1+GJ1+GF2+ZY3DOM02.rrd'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}632701玉树市.mdb'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}63270102XQ.dbf'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}63270102XQ.prj'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}63270102XQ.sbn'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}63270102XQ.sbx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}63270102XQ.shp'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '分块{0}63270102XQ.shx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }
        ]


if __name__ == '__main__':
    pytest.main()
