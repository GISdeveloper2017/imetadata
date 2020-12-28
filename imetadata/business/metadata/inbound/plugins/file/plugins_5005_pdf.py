# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 14:51 
# @Author : 王西亚 
# @File : plugins_5001_doc.py
from imetadata.business.metadata.base.plugins.industry.common.c_documentFilePlugins import CDocumentFilePlugins


class plugins_5005_pdf(CDocumentFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type_Title] = '可携带文档'
        return information

    def default_document_file_ext(self):
        return 'pdf'
