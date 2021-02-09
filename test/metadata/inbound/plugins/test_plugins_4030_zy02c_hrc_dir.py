# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4030_zy02c_hrc import plugins_4030_zy02c_hrc
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("资源三号02星HRC传感器目录文件")  # 模块标题
class Test_plugins_4030_zy02c_hrc_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4030_zy02c_hrc(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'ZY02C_HRC_E125.4_N51.1_20130622_L2C0001835341',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'ZY02C_HRC_E125.4_N51.1_20130622_L2C0001835341'
            }
        ]


if __name__ == '__main__':
    pytest.main()
