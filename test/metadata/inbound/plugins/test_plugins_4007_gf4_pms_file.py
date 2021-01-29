# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_4007_gf4_pms import plugins_4007_gf4_pms
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("高分四号PMS传感器压缩包文件")  # 模块标题
class Test_plugins_4007_gf4_pms_file(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4007_gf4_pms(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'GF4_PMS_E72.9_N28.9_20170211_L1A0000155286.tar.gz',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF4_PMS_E72.9_N28.9_20170211_L1A0000155286'
            }
        ]


if __name__ == '__main__':
    pytest.main()
