# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4022_s2a_s2msi1c import plugins_4022_s2a_s2msi1c
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("哨兵二号目录文件")  # 模块标题
class Test_plugins_4022_s2a_s2msi1c_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4022_s2a_s2msi1c(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'S2A_MSIL1C_20170512T024551_N0205_R132_T50SNB_20170512T025555.SAFE',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'S2A_MSIL1C_20170512T024551_N0205_R132_T50SNB_20170512T025555.SAFE'
            }
        ]


if __name__ == '__main__':
    pytest.main()
