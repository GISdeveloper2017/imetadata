# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.inbound.plugins.file.plugins_1000_1007_xqyx_qy_tj2000 import \
    plugins_1000_1007_xqyx_qy_tj2000


class plugins_1000_1010_xqyx_sy_tj2000(plugins_1000_1007_xqyx_qy_tj2000):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type_Code] = '10001010'
        information[self.Plugins_Info_Coordinate_System] = 'tj2000'
        information[self.Plugins_Info_Coordinate_System_Title] = '2000天津城市坐标系'
        information[self.Plugins_Info_yuji] = '市域镶嵌'
        return information
