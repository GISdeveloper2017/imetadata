# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4008_gf5_vims import plugins_4008_gf5_vims
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("高分五号VIMS传感器目录文件")  # 模块标题
class Test_plugins_4008_gf5_vims_Dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4008_gf5_vims(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'GF5_VIMS_N29.3_E112.4_20190321_010277_L10000129147',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF5_VIMS_N29.3_E112.4_20190321_010277_L10000129147'
            }
        ]


if __name__ == '__main__':
    pytest.main()
