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
from imetadata.business.metadata.inbound.plugins.file.plugins_6002_mdb import plugins_6002_mdb
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


#  运行前建议注释掉CPlugins类中parser_metadata_with_qa方法中853行，不然新建的layer污染数据库
@allure.feature("mdb")  # 模块标题
class Test_plugins_6002_mdb(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_6002_mdb(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '影像{0}云南高分影像{0}F47{0}'
                                          'F47E001007BJ210M2017A.MDB'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'F47E001007BJ210M2017A'
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '影像{0}云南高分影像{0}F48{0}'
                                          'F48E001001BJ210M2017A.MDB'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'F48E001001BJ210M2017A'
            }
        ]

    def init_before_test(self):
        plugins_info = self.create_plugins().get_information()
        plugins_catalog = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Catalog_Title, '')
        plugins_group = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Group_Title, '')
        plugins_type = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Type, '')
        self._test_file_root_path = settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, '')
        self._test_file_parent_path = CFile.join_file(
            settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, ''),
            plugins_catalog
        )


if __name__ == '__main__':
    pytest.main()
