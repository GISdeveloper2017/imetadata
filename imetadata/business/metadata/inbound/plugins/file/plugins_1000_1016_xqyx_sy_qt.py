# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.inbound.plugins.file.plugins_1000_1015_xqyx_qy_qt import plugins_1000_1015_xqyx_qy_qt


class plugins_1000_1016_xqyx_sy_qt(plugins_1000_1015_xqyx_qy_qt):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type_Code] = '02010602'

        information[self.Plugins_Info_Coordinate_System] = ''
        information[self.Plugins_Info_Coordinate_System_Title] = ''
        information[self.Plugins_Info_yuji] = '市域镶嵌'
        return information
