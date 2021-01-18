# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_4003_de2_pms import plugins_4003_de2_pms
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("DEIMOS-2_PMS压缩包文件")  # 模块标题
class Test_plugins_4003_de2_pms_file(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4003_de2_pms(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'DE2_PM4_L1B_000000_20161121T033746_20161121T033749_DE2_13136_D2F2.zip',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'DE2_PM4_L1B_000000_20161121T033746_20161121T033749_DE2_13136_D2F2'
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'CB04-P10-365-64-B2-20170819-L20003200907.tar.gz',
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: 'CB04-P10-365-64-B2-20170819-L20003200907'
            }
        ]


if __name__ == '__main__':
    pytest.main()
