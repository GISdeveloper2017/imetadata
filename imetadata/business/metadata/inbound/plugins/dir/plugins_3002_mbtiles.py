# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_3002_mbtiles.py

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class plugins_3002_mbtiles(CFilePlugins):
    __metadata_xml_file_name__ = None

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '二十一世纪公司切片'
        # information[self.Plugins_Info_Name] = '21at_mbtiles'
        information[self.Plugins_Info_Type_Code] = None
        information[self.Plugins_Info_Group] = self.DataGroup_Raster
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Common
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name

        return information

    def classified(self):
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_object_name = file_main_name[:]
        file_main_name_with_path = CFile.join_file(self.file_info.file_path, file_object_name)

        if CUtils.equal_ignore_case(file_ext, self.FileExt_Mbtiles):
            if CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[01HQ]\d[_][0]$') \
                    or CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[_][0]$'):  # 结尾为0
                self._object_confirm = self.Object_Confirm_IKnown
                self._object_name = file_main_name
            elif CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[01HQ]\d[_]\d+$') \
                    or CUtils.text_match_re(file_main_name, r'(?i)^\S+[12]\d{3}[_]\d+$'):  # 结尾为单个字母的情况
                self._object_confirm = self.Object_Confirm_IKnown_Not
                self._object_name = None
            else:
                self._object_confirm = self.Object_Confirm_IUnKnown
                self._object_name = self._object_name
        elif CUtils.equal_ignore_case(file_ext, self.Transformer_XML) \
                and CFile.file_or_path_exist('{0}_0.mbtiles'.format(file_main_name_with_path)):
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
        else:
            self._object_confirm = self.Object_Confirm_IUnKnown
            self._object_name = self._object_name

        return self._object_confirm, self._object_name

    def add_file_to_details(self, file_full_name):
        """
        追加到附属文件集合中
        """
        self._object_detail_file_full_name_list.append(file_full_name)

    def add_file_to_detail_list(self):
        """
        设定国土行业数据mosaic的附属文件的验证规则（镶嵌影像）
        完成 负责人 李宪 在这里检验mosaic的附属文件的识别规则
        :return:
        """
        file_detail_xml = '{0}.xml'.format(self.file_info.file_main_name_with_full_path[:-2])
        self.add_file_to_details(file_detail_xml)  # 将文件加入到附属文件列表中
        file_detail_mbtiles = '{0}_*.mbtiles'.format(self.file_info.file_main_name[:-2])
        if not CUtils.equal_ignore_case(self.file_info.file_path, ''):
            list_file_fullname_xq = CFile.file_or_dir_fullname_of_path(
                self.file_info.file_path,
                False,
                file_detail_mbtiles,
                CFile.MatchType_Common)  # 模糊匹配文件列表
            for list_file_fullname in list_file_fullname_xq:
                if not CUtils.equal_ignore_case(CFile.file_main_name(list_file_fullname),
                                                self.file_info.file_main_name):
                    self.add_file_to_details(list_file_fullname)  # 将文件加入到附属文件列表中
