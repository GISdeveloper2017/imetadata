# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 15:05 
# @Author : 王西亚 
# @File : c_documentFilePlugins.py
from abc import abstractmethod

from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class CDocumentFilePlugins(CFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = self.default_document_file_ext()
        information[self.Plugins_Info_Type_Code] = None
        information[self.Plugins_Info_Group] = self.DataGroup_Document
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Common
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Document_Tika
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_File_Itself
        information[self.Plugins_Info_Is_Space] = self.DB_False
        information[self.Plugins_Info_Is_Dataset] = self.DB_False
        return information

    def get_classified_character(self):
        """
        设置识别的特征
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return '*.{0}'.format(self.default_document_file_ext()), self.TextMatchType_Common

    @abstractmethod
    def default_document_file_ext(self) -> str:
        """
        设置默认的文档文件扩展名
        :return:
        """
        return ''
