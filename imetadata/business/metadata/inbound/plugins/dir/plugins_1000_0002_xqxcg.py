# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.custom.c_dirPlugins_keyword import CDirPlugins_keyword


class plugins_1000_0002_xqxcg(CDirPlugins_keyword):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津测绘'
        information[self.Plugins_Info_Catalog_Title] = '天津测绘'
        information[self.Plugins_Info_Group] = '中间成果'
        information[self.Plugins_Info_Group_Title] = '中间成果'
        information[self.Plugins_Info_Type] = '镶嵌线成果'
        information[self.Plugins_Info_Type_Title] = '镶嵌线成果'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        return information

    def get_classified_character_of_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: 'file_name',  # 左下角经度 必填
                self.TextMatchType_Common: None,
                self.TextMatchType_Regex: '(?i)镶嵌线成果|镶嵌线'
            },
            {
                self.Name_ID: 'file_path',  # 左下角经度 必填
                self.TextMatchType_Common: None,
                self.TextMatchType_Regex: None
            }
        ]
