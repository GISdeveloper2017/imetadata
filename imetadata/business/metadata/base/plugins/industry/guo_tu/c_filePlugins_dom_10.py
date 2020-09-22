# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_wfv.py
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class CFilePlugins_DOM_10(CFilePlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'gf1_wfv'
        information[self.Plugins_Info_Name] = 'gf1_wfv'

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
        return 'gf1_wfv*', self.TextMatchType_Common