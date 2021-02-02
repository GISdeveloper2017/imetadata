# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4016_planet import plugins_4016_planet
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("PLANET星CCD传感器目录文件")  # 模块标题
class Test_plugins_4016_planet_ccd_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4016_planet(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: '20190312_023843_0e16',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '20190312_023843_0e16'
            }
        ]


if __name__ == '__main__':
    pytest.main()
