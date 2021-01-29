# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4007_gf4_b1 import plugins_4007_gf4_b1
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("高分四号B1传感器目录文件")  # 模块标题
class Test_plugins_4007_gf4_b1_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4007_gf4_b1(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'GF4_B1_E120.4_N36.0_20180602_L1A0000197188',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF4_B1_E120.4_N36.0_20180602_L1A0000197188'
            }
        ]


if __name__ == '__main__':
    pytest.main()
