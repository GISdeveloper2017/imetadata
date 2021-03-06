# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4001_triplesat_pms import plugins_4001_triplesat_pms
from imetadata.business.metadata.inbound.plugins.dir.plugins_4035_terrasar import plugins_4035_terrasar
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("terrasar星目录文件")  # 模块标题
class Test_plugins_4035_terrasar_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4035_terrasar(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'SO_000107707_0002_1',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'SO_000107707_0002_1'
            }
        ]


if __name__ == '__main__':
    pytest.main()
