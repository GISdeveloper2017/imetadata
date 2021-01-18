# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4004_gf1_c import plugins_4004_gf1_c
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("GF1_C文件夹类型成果影像")  # 模块标题
class Test_plugins_4004_gf1_c_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4004_gf1_c(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'GF1C_PMS_E117.0_N33.0_20180930_L1A1021333125',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF1C_PMS_E117.0_N33.0_20180930_L1A1021333125'
            }
        ]


if __name__ == '__main__':
    pytest.main()
