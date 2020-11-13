# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 11:41 
# @Author : 王西亚 
# @File : c_dmBaseJob.py

from __future__ import absolute_import

from imetadata.base.c_xml import CXml
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob


class CDMBaseJob(CDBQueueJob):
    Path_MD_Bus_Root = '/root'
    Path_MD_Bus_ProductType = '{0}/ProductType'.format(Path_MD_Bus_Root)


    def metadata_bus_2_params(self, metadata_xml: CXml, params: dict):
        metadata_list = metadata_xml.xpath('{0}/*'.format(self.Path_MD_Bus_Root))
        for metadata_item in metadata_list:
            metadata_item_name = CXml.get_element_name(metadata_item).lower().strip()
            metadata_item_value = CXml.get_element_text(metadata_item).lower().strip()
            params[metadata_item_name] = metadata_item_value
