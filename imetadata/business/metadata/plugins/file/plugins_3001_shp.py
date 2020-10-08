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
        """
        初始化默认的, 文件的质检列表
        质检项目应包括并不限于如下内容:
        1. 实体数据的附属文件是否完整, 实体数据是否可以正常打开和读取
        1. 元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        1. 业务元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        示例:
        return [
            {self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()), self.Name_ID: 'pan_tif',
             self.Name_Title: '全色文件', self.Name_Type: self.QualityAudit_Type_Error}
            , {self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()), self.Name_ID: 'mss_tif',
               self.Name_Title: '多光谱文件', self.Name_Type: self.QualityAudit_Type_Error}
        ]
        :param parser:
        :return:
        """
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
