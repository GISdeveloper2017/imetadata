# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_4001_triplesat_pms import plugins_4001_triplesat_pms
from imetadata.business.metadata.inbound.plugins.dir.plugins_4033_radarsat import plugins_4033_radarsat
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("radarsat星目录文件")  # 模块标题
class Test_plugins_4033_radarsat_dir(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_4033_radarsat(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'RS2_OK102431_PK669810_DK904241_SLA76_20180930_102901_HH_SLC',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'RS2_OK102431_PK669810_DK904241_SLA76_20180930_102901_HH_SLC'
            }
        ]


if __name__ == '__main__':
    pytest.main()
