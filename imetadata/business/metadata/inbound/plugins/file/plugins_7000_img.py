# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:25 
# @Author : 王西亚 
# @File : plugins_7000_img.py

from imetadata.business.metadata.base.plugins.industry.common.c_rasterFilePlugins import CRasterFilePlugins


class plugins_7000_img(CRasterFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'img'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
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
        return '*.img', self.TextMatchType_Common
