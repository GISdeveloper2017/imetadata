# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_4014_kompsat3_pms import plugins_4014_kompsat3_pms
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("kompsat3压缩包文件")  # 模块标题
class Test_plugins_4014_kompsat3_file(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4014_kompsat3_pms(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'K3_20180728053929_33051_08291282_L1R_DZ_Bundle.zip',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'K3_20180728053929_33051_08291282_L1R_DZ_Bundle'
            }
        ]


if __name__ == '__main__':
    pytest.main()
