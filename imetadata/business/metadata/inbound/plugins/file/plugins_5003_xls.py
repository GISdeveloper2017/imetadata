# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 14:51 
# @Author : 王西亚 
# @File : plugins_5001_doc.py
from imetadata.business.metadata.base.plugins.industry.common.c_documentFilePlugins import CDocumentFilePlugins


class plugins_5003_xls(CDocumentFilePlugins):
    def default_document_file_ext(self):
        return 'xls'
