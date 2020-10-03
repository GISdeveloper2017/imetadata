# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:25 
# @Author : 王西亚 
# @File : plugins_3001_shp.py.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.common.c_vectorFilePlugins import CVectorFilePlugins


class plugins_3001_shp(CVectorFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Name] = 'shp'
        # information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Same_Dir
        # information[self.Plugins_Info_DetailEngine] = self.DetailEngine_File_Of_Same_Dir
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
        return '*.shp', self.TextMatchType_Common

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {self.Name_FileName: '{0}.dbf'.format(self.classified_object_name()), self.Name_ID: 'dbf',
             self.Name_Title: '属性数据文件', self.Name_Result: self.QA_Result_Error}
            , {self.Name_FileName: '{0}.prj'.format(self.classified_object_name()), self.Name_ID: 'prj',
               self.Name_Title: '投影文件', self.Name_Result: self.QA_Result_Warn}
            , {self.Name_FileName: '{0}.shx'.format(self.classified_object_name()), self.Name_ID: 'shx',
               self.Name_Title: 'shx文件', self.Name_Result: self.QA_Result_Error}
            , {self.Name_FileName: '{0}.sbn'.format(self.classified_object_name()), self.Name_ID: 'sbn',
               self.Name_Title: 'sbn文件', self.Name_Result: self.QA_Result_Error}
            , {self.Name_FileName: '{0}.sbx'.format(self.classified_object_name()), self.Name_ID: 'sbx',
               self.Name_Title: 'sbx文件', self.Name_Result: self.QA_Result_Error}
        ]
