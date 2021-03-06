# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.inbound.plugins.file.plugins_1000_1005_zjyx_tj2000 import plugins_1000_1005_zjyx_tj2000


class plugins_1000_1004_zjyx_cgcs2000(plugins_1000_1005_zjyx_tj2000):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Coordinate_System] = 'cgcs2000'
        information[self.Plugins_Info_Coordinate_System_Title] = '2000国家标准坐标系'
        return information
