# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4001_triplesat_pms import plugins_4001_triplesat_pms
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("北京二号PMS传感器目录文件")  # 模块标题
class Test_plugins_4001_triplesat_pms_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4001_triplesat_pms(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'TRIPLESAT_1_PMS_20190111022824_001F3FVI_016',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'TRIPLESAT_1_PMS_20190111022824_001F3FVI_016'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'TRIPLESAT_2_PMS_20191125021402_002047VI_021',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'TRIPLESAT_2_PMS_20191125021402_002047VI_021'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'TRIPLESAT_3_PMS_20190108021412_001E18VI_007',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'TRIPLESAT_3_PMS_20190108021412_001E18VI_007'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'TRIPLESAT_4_PMS_20191111021739_0007C9VI_032',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'TRIPLESAT_4_PMS_20191111021739_0007C9VI_032'
            },
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'CB04-P10-365-64-B2-20170819-L20003200907',
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: 'CB04-P10-365-64-B2-20170819-L20003200907'
            }
        ]


if __name__ == '__main__':
    pytest.main()
