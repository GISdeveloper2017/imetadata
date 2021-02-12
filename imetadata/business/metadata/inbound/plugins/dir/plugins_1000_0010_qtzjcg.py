# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.base.plugins.custom.c_dirPlugins_keyword import CDirPlugins_keyword


class plugins_1000_0010_qtzjcg(CDirPlugins_keyword):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Project_ID] = 'tjch'
        information[self.Plugins_Info_Catalog] = '天津测绘'
        information[self.Plugins_Info_Catalog_Title] = '天津测绘'
        information[self.Plugins_Info_Group] = '中间成果'
        information[self.Plugins_Info_Group_Title] = '中间成果'
        information[self.Plugins_Info_Type] = '其他中间成果'
        information[self.Plugins_Info_Type_Title] = '其他中间成果'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_Type_Code] = None
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: '(?i)其他中间成果'
            },
            {
                self.Name_ID: self.Name_FilePath,
                self.Name_RegularExpression: None
            },
            {
                self.Name_ID: self.Name_FileAffiliated,
                self.Name_FilePath: None,  # 配置需要验证附属文件存在性的 文件路径
                self.Name_RegularExpression: None  # 配置需要验证附属文件的匹配规则,对于文件全名匹配
            }
        ]
