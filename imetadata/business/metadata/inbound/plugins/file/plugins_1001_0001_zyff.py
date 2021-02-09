# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.inbound.plugins.file.plugins_1001_0002_bzff import plugins_1001_0002_bzff


class plugins_1001_0001_zyff(plugins_1001_0002_bzff):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津海图'
        information[self.Plugins_Info_Catalog_Title] = '天津海图'
        information[self.Plugins_Info_Group] = '分幅数据'
        information[self.Plugins_Info_Group_Title] = '分幅数据'
        information[self.Plugins_Info_Type] = 'JB自由分幅'
        information[self.Plugins_Info_Type_Title] = 'JB自由分幅'
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,  # 配置数据文件名的匹配规则
                self.Name_RegularExpression: '(?i)^([^DKL]|[DKL][^SN]|[DKL][SN].{,2}$)'
            },
            {
                self.Name_ID: self.Name_FilePath,  # 配置数据文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)^.+'
                                             r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
                                             r'.+'
                                             r'[\\\\/]影像'
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.Name_RegularExpression: '(?i)^(img|tif|tiff)$'  # 配置数据文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileAffiliated,
                self.Name_FilePath: None,  # 配置需要验证附属文件存在性的 文件路径
                self.Name_RegularExpression: None  # 配置需要验证附属文件的匹配规则,对于文件全名匹配
            }
        ]

    def get_classified_character_of_affiliated_keyword(self):
        """
        设置识别的特征
        """
        return []

    def get_custom_affiliated_file_character(self):
        return []

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
