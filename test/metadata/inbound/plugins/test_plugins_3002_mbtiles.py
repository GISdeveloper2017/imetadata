# -*- coding: utf-8 -*-
# @Time : 2020/12/4 09:05
# @Author : 王西亚
# @File : test_plugins_aaa.py
import allure
import pytest

from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.business.metadata.inbound.plugins.dir.plugins_3002_mbtiles import plugins_3002_mbtiles
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


#  运行前建议注释掉CPlugins类中parser_metadata_with_qa方法中853行，不然新建的layer污染数据库
@allure.feature("gdb")  # 模块标题
class Test_plugins_3002_mbtiles(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_3002_mbtiles(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_Dir,
                self.Name_Test_file_path: 'mbtiles',
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'mbtiles'
            }
        ]


if __name__ == '__main__':
    pytest.main()
