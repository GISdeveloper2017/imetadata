# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.base.plugins.custom.c_dirPlugins_keyword import CDirPlugins_keyword


class plugins_1000_0008_zttcg(CDirPlugins_keyword):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津测绘'
        information[self.Plugins_Info_Catalog_Title] = '天津测绘'
        information[self.Plugins_Info_Group] = '信息产品'
        information[self.Plugins_Info_Group_Title] = '信息产品'
        information[self.Plugins_Info_Type] = '专题图成果'
        information[self.Plugins_Info_Type_Title] = '专题图成果'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        return information

    def get_classified_character_of_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: 'file_name',
                self.TextMatchType_Regex: '(?i)专题图成果'
            },
            {
                self.Name_ID: 'file_path',
                self.TextMatchType_Regex: None
            },
            {
                self.Name_ID: 'file_ext',
                self.TextMatchType_Regex: None
            }
        ]

    def get_classified_object_name_of_keyword(self, file_main_name) -> str:
        return super().get_classified_object_name_of_keyword(file_main_name)
