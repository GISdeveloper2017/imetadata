# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4006_gf3_VHVV import plugins_4006_gf3_VHVV
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("GF3_VHVV文件夹类型成果影像")  # 模块标题
class Test_Dir_plugins_4006_gf3_VHVV(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4006_gf3_VHVV(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'GF3_KAS_WSC_000823_E122.8_N39.8_20161005_L1A_VHVV_L10002039504',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF3_KAS_WSC_000823_E122.8_N39.8_20161005_L1A_VHVV_L10002039504'
            }
        ]


if __name__ == '__main__':
    pytest.main()
