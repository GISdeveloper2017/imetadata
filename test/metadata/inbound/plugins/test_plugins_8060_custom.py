# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_8020_ortho import plugins_8020_ortho
from imetadata.business.metadata.inbound.plugins.file.plugins_8060_custom import plugins_8060_custom
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("其它成果影像")  # 模块标题
class Test_plugins_8060_custom(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_8060_custom(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'qwe124513asa.tif',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'qwe124513asa'
            },
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: 'qwe124513asa_21at.xml',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }
        ]


if __name__ == '__main__':
    pytest.main()
