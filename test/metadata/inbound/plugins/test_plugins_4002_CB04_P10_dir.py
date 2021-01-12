# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4002_CB04_P10 import plugins_4002_CB04_P10
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("中巴地球资源卫星04星")  # 模块标题
class Test_plugins_4002_CB04_P10_file(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4002_CB04_P10(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'CB04-P10-365-64-B2-20170819-L20003200907',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'CB04-P10-365-64-B2-20170819-L20003200907'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'TRIPLESAT_4_PMS_20191111021739_0007C9VI_032',
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: 'TRIPLESAT_4_PMS_20191111021739_0007C9VI_032'
            }
        ]


if __name__ == '__main__':
    pytest.main()
