# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest

import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.file.plugins_1000_1013_ffyx_qt import \
    plugins_1000_1013_ffyx_qt
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("天津测绘分幅影像其他国家标准坐标系")  # 模块标题
class Test_plugins_1000_1013_ffyx_qt(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_1000_1013_ffyx_qt(file_info)

    def test_file_info_list(self):
        return [

            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '202008{0}FenFu{0}其他国家标准坐标系{0}2772.0-509.0.tif'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: '2772.0-509.0'
            }
        ]

    def init_before_test(self):
        plugins_info = self.create_plugins().get_information()
        plugins_catalog = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Catalog_Title, '')
        self._test_file_root_path = settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, '')
        self._test_file_parent_path = CFile.join_file(
            settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, ''),
            plugins_catalog
        )


if __name__ == '__main__':
    pytest.main()
