# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_4032_ikonos import plugins_4032_ikonos
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("ikonos星压缩包文件")  # 模块标题
class Test_plugins_4032_ikonos_file(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4032_ikonos(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '2002110505262570000011625219.zip',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '2002110505262570000011625219'
            }
        ]


if __name__ == '__main__':
    pytest.main()
