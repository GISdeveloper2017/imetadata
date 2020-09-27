# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_wfv.py

from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins


class CSatFilePlugins_gf1_wfv(CSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'gf1_wfv'
        information[self.Plugins_Info_Name] = 'gf1_wfv'

        return information

    def get_classified_character_of_zip_and_path(self):
        """
        设置识别的特征
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return 'gf1_wfv_*_l1a*', self.TextMatchType_Common

    def get_classified_character_of_file(self):
        """
        设置识别的特征
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return 'gf1_wfv_*_l1a*-pan1.tiff', self.TextMatchType_Common

    def get_classified_object_name_by_file(self) -> str:
        """
        当卫星数据是解压后的散落文件时, 如何从解压后的文件名中, 解析出卫星数据的原名
        :return:
        """
        return self.file_info.__file_main_name__.replace('-PAN1', '')
