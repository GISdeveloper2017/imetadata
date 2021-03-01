# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.inbound.plugins.file.plugins_1000_1002_ffyx_tj2000 import plugins_1000_1002_ffyx_tj2000


class plugins_1000_1001_ffyx_cgcs2000(plugins_1000_1002_ffyx_tj2000):

    def get_information(self) -> dict:
        information = super().get_information()

        information[self.Plugins_Info_Type_Code] = '10001001'
        information[self.Plugins_Info_Coordinate_System] = 'cgcs2000'
        information[self.Plugins_Info_Coordinate_System_Title] = '2000国家标准坐标系'
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        file_mian_name = self.file_info.file_main_name
        file_path = self.file_info.file_path
        same_name_list = CFile.file_or_subpath_of_path(file_path, file_mian_name[:-1] + r'.\..*$',
                                                       CFile.MatchType_Regex)
        last_letter_list = list()
        if len(same_name_list) > 0:
            for same_file_full_name in same_name_list:
                same_file_name = CFile.file_name(same_file_full_name)
                last_letter_list.append(same_file_name[-1:].lower())
            if 'a' in last_letter_list:
                RegularExpression_letter = 'a'
            elif 'b' in last_letter_list:
                RegularExpression_letter = 'b'
            elif 'c' in last_letter_list:
                RegularExpression_letter = 'c'
            elif 'd' in last_letter_list:
                RegularExpression_letter = 'd'
            else:
                RegularExpression_letter = 'a'
        else:
            RegularExpression_letter = 'a'
        return [
            {
                self.Name_ID: self.Name_FileName,  # 配置数据文件名的匹配规则
                self.Name_RegularExpression: r'(?i)^.{13}\d{2}[pm]\d{4}[' + RegularExpression_letter + 'o]$'
            },
            {
                self.Name_ID: self.Name_FilePath,  # 配置数据文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)\d{4}.{2}[\\\\/]FenFu[\\\\/]' + self.get_coordinate_system_title()
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.Name_RegularExpression: '(?i)^(tif|tiff)$'  # 配置数据文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileAffiliated,
                self.Name_FilePath: None,  # 配置需要验证附属文件存在性的 文件路径
                # 配置需要验证附属文件的匹配规则,对于文件全名匹配
                self.Name_RegularExpression: None
            }
        ]

    def get_classified_character_of_affiliated_keyword(self):
        """
        设置识别的特征
        """
        file_mian_name = self.file_info.file_main_name
        file_path = self.file_info.file_path
        same_name_list = CFile.file_or_subpath_of_path(file_path, file_mian_name[:-1] + r'.\..*$',
                                                       CFile.MatchType_Regex)
        last_letter_list = list()
        if len(same_name_list) > 0:
            for same_file_full_name in same_name_list:
                same_file_name = CFile.file_name(same_file_full_name)
                last_letter_list.append(same_file_name[-1:].lower())
            if 'a' in last_letter_list:
                RegularExpression_letter = 'bcd'
                RegularExpression_main_letter = 'a'
            elif 'b' in last_letter_list:
                RegularExpression_letter = 'cd'
                RegularExpression_main_letter = 'b'
            elif 'c' in last_letter_list:
                RegularExpression_letter = 'd'
                RegularExpression_main_letter = 'c'
            elif 'd' in last_letter_list:
                RegularExpression_letter = ''
                RegularExpression_main_letter = 'd'
            else:
                RegularExpression_letter = 'bcd'
                RegularExpression_main_letter = 'a'
        else:
            RegularExpression_letter = 'bcd'
            RegularExpression_main_letter = 'a'
        return [
            {
                self.Name_ID: self.Name_FileName,  # 配置附属文件名的匹配规则
                self.Name_RegularExpression: r'(?i)^.{13}\d{2}[pm]\d{4}[' + RegularExpression_letter + 'mp]$'
            },
            {
                self.Name_ID: self.Name_FilePath,
                # 配置附属文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)\d{4}.{2}[\\\\/]FenFu[\\\\/]' + self.get_coordinate_system_title()
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.Name_RegularExpression: '(?i)^(tif|tiff|tfw|xml)$'  # 配置附属文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileMain,  # 配置需要验证主文件存在性的 文件路径
                self.Name_FilePath: self.file_info.file_path,
                # 配置需要验证主文件的匹配规则,对于文件全名匹配
                self.Name_RegularExpression: '(?i)^' + self.file_info.file_main_name[:-1] +
                                             r'[o' + RegularExpression_main_letter + r']\.tif[f]?'
            }
        ]
