# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:03
# @Author : 赵宇飞
# @File : plugins_1030_mosaic.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_21at import \
    CFilePlugins_GUOTU_21AT


class plugins_1030_mosaic(CFilePlugins_GUOTU_21AT):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '镶嵌影像'
        information[self.Plugins_Info_Name] = 'mosaic'

        return information

    def classified(self):
        """
        设计国土行业数据mosaic的验证规则（镶嵌影像）
        todo 负责人 王学谦 在这里检验mosaic的识别规则
        :return:
        """
        pass