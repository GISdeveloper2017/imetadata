# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_wfv.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins


class CSatFilePlugins_gf1_pms(CSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'gf1_pms'
        information[self.Plugins_Info_Name] = 'gf1_pms'

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
        return 'gf1_pms1_*_l1a*', self.TextMatchType_Common

    def get_classified_character_of_file(self):
        """
        设置识别的特征
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return 'gf1_pms1_*_l1a*-pan1.tiff', self.TextMatchType_Common

    def get_classified_object_name_by_file(self) -> str:
        """
        当卫星数据是解压后的散落文件时, 如何从解压后的文件名中, 解析出卫星数据的原名
        :return:
        """
        return self.file_info.__file_main_name__.replace('-PAN1', '')

    def init_aq_file_exist_list(self, parser) -> list:
        return [
            {self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()), self.Name_ID: 'pan_tif',
             self.Name_Title: '全色文件', self.Name_Type: self.QualityAudit_Type_Error}
            , {self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()), self.Name_ID: 'mss_tif',
               self.Name_Title: '多光谱文件', self.Name_Type: self.QualityAudit_Type_Error}
        ]

    def init_aq_metadata_xml_item_list(self, parser):
        """
        初始化默认的, 元数据xml文件的检验列表
        :param parser:
        :return:
        """
        pass

    def init_aq_metadata_bus_xml_item_list(self, parser):
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        pass

    def parser_metadata_custom(self, parser):
        """
        自定义的元数据处理逻辑
        :param parser:
        :return:
        """
        pass
