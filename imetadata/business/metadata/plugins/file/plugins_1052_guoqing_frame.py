# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:27
# @Author : 赵宇飞
# @File : plugins_1052_guoqing_frame.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class plugins_1052_guoqing_frame(CFilePlugins_GUOTU):
    """
    与国情影像-整景纠正有差别(业务元数据xml的字段),xml文件的识别也不同，也不是***_21at.xml模式，所以直接继承于CFilePlugins_GUOTU
        数据内容	    文件格式	是否有坐标系	内容样例	说明
        影像文件	    tif/TIF	有	H50E003006AP005P2011A.TIF	融合影像文件
        元数据文件	xml/XML	无	H50E003006AP005P2011M.XML	整体元数据文件
    """
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-分幅影像'
        information[self.Plugins_Info_Name] = 'guoqing_frame'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_frame的验证规则（国情影像—分幅影像）
        todo 负责人 王学谦 在这里检验guoqing_frame的识别规则
        :return:
        """
        pass