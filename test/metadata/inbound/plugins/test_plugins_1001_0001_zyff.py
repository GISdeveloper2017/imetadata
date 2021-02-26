# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest

from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_1001_0001_zyff import plugins_1001_0001_zyff
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("天津海图JB自由分幅")  # 模块标题
class Test_plugins_1001_0001_zyff(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_1001_0001_zyff(file_info)

    def test_file_info_list(self):
        return [

            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '北京市20200101自由分幅测试{0}影像{0}b.tif'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'b'
            }
        ]


if __name__ == '__main__':
    pytest.main()
