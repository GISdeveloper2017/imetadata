# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest

from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_1001_0002_bzff import plugins_1001_0002_bzff
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("天津海图JB标准分幅")  # 模块标题
class Test_plugins_1001_0002_bzff(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_1001_0002_bzff(file_info)

    def test_file_info_list(self):
        return [

            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '北京市20210204测试{0}影像{0}DS5010.tif'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'DS5010'
            }
        ]


if __name__ == '__main__':
    pytest.main()
