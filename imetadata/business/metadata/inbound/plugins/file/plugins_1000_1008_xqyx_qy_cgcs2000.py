# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.inbound.plugins.file.plugins_1000_1007_xqyx_qy_tj2000 import \
    plugins_1000_1007_xqyx_qy_tj2000


class plugins_1000_1008_xqyx_qy_cgcs2000(plugins_1000_1007_xqyx_qy_tj2000):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type_Code] = '02010601'
        information[self.Plugins_Info_Coordinate_System] = 'cgcs2000'
        information[self.Plugins_Info_Coordinate_System_Title] = '2000国家标准坐标系'
        information[self.Plugins_Info_yuji] = '区域镶嵌'
        return information
