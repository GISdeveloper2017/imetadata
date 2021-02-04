# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4018_landsat8 import plugins_4018_landsat8
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("landsat8目录文件")  # 模块标题
class Test_plugins_4018_landsat8_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4018_landsat8(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'LS8_C_20170912_025912_000000_123046_GEOTIFF_SNC_L4',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'LS8_C_20170912_025912_000000_123046_GEOTIFF_SNC_L4'
            }
        ]


if __name__ == '__main__':
    pytest.main()
