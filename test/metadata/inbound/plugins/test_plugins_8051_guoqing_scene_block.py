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
from imetadata.business.metadata.inbound.plugins.file.plugins_8051_guoqing_scene_block import \
    plugins_8051_guoqing_scene_block
from test.metadata.inbound.plugins.plugins_test_base import Plugins_Test_Base


@allure.feature("国情影像_整景纠正_分块")  # 模块标题
class Test_plugins_8051_guoqing_scene_block(Plugins_Test_Base):
    def create_plugins(self, file_info: CDMFilePathInfoEx = None) -> CPlugins:
        return plugins_8051_guoqing_scene_block(file_info)

    def test_file_info_list(self):
        return [
            {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204.rar'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204.xls'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204_M_rpc.txt'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204_P_rpc.txt'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204F-1.ige'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204F-1.img'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown,
                self.Name_Test_object_name: 'GF2365199920181204F-1'
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204F-1.img.aux.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204F-1.img.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204F-1.rde'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204F-1.rrd'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204G.dbf'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204G.prj'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204G.sbn'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204G.sbx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204G.shp'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204G.shx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204M-1.img'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204M-1.img.aux.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204M.XML'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204P.img'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IUnKnown,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204P.XML'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204P-1.img'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204P-1.img.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204RGB.tfw'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204RGB.tif'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204RGB.tif.aux.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204RGB.tif.xml'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204T.XML'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Y.XML'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Y问题说明.docx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Q.dbf'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Q.prj'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Q.sbn'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Q.sbx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Q.shp'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }, {
                self.Name_Test_File_Type: self.FileType_File,
                self.Name_Test_file_path: '整景纠正带-{0}GF2365199920181204Q.shx'.format(CFile.sep()),
                self.Name_Test_object_confirm: self.Object_Confirm_IKnown_Not,
                self.Name_Test_object_name: None
            }
        ]

    def init_before_test(self):
        plugins_info = self.create_plugins().get_information()
        plugins_catalog = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Catalog_Title, '')
        plugins_group = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Group_Title, '')
        plugins_type = CUtils.dict_value_by_name(plugins_info, CPlugins.Plugins_Info_Type, '')
        self._test_file_root_path = settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, '')
        self._test_file_parent_path = CFile.join_file(
            settings.application.xpath_one(self.Path_Setting_Dir_Test_Data, ''),
            plugins_catalog,
            plugins_group,
            '国情影像',
            plugins_type
        )


if __name__ == '__main__':
    pytest.main()
