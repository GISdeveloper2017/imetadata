# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4008_gf5_gmi import plugins_4008_gf5_gmi
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("高分五号GMI传感器目录文件")  # 模块标题
class Test_plugins_4008_gf5_gmi_Dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4008_gf5_gmi(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'GF5_GMI_N26.89_E113.27_20190406_004844_L10002440213',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF5_GMI_N26.89_E113.27_20190406_004844_L10002440213'
            }
        ]


if __name__ == '__main__':
    pytest.main()
