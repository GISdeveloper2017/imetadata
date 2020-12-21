# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest

from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_6001_shp import plugins_6001_shp
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("shp")  # 模块标题
class Test_plugins_6001_shp(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_6001_shp(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.dbf'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.prj'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.sbn'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.sbx'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.shp'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK'
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.shp.xml'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '矢量数据{0}正确数据{0}'
                                          'BJ2_GF1_GF2_SPOT_KUNMING_20170204_20171116_CGCS2000_1_FBZXQK.shx'
                    .format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
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
            plugins_catalog,
            plugins_group
        )


if __name__ == '__main__':
    pytest.main()
