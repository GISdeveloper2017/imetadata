# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.business.metadata.base.plugins.custom.c_dirPlugins_keyword import CDirPlugins_keyword


class plugins_1001_0002_bzff(CDirPlugins_keyword):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津海图'
        information[self.Plugins_Info_Catalog_Title] = '天津海图'
        information[self.Plugins_Info_Group] = '分幅数据'
        information[self.Plugins_Info_Group_Title] = '分幅数据'
        information[self.Plugins_Info_Type] = 'JB标准分幅'
        information[self.Plugins_Info_Type_Title] = 'JB标准分幅'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: '(?i)^[DKL][SN].{3,10}$'  # 配置数据文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,  # 配置数据文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)^.*'
                                             r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
                                             r'.*'
                                             r'[\\/]影像$'
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
        file_path = self.file_info.file_path
        affiliated_file_path = '影像'.join(file_path.rsplit('矢量', 1))  # 替换最后一个字符
        file_main_name = self.file_info.file_main_name
        file_main_name_reg = '(?i)^' + file_main_name[:6] + '.*[.](img|tif|tiff)'
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: '(?i)^[DKL][SN].{3,}$'  # 配置附属文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,
                self.Name_RegularExpression: r'(?i)^.*'
                                             r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
                                             r'.*'
                                             r'[\\/]矢量$'  # 配置附属文件路径的匹配规则
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.Name_RegularExpression: '(?i)^shp$'  # 配置附属文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileMain,  # 配置需要验证主文件存在性的 文件路径
                self.Name_FilePath: affiliated_file_path,
                self.Name_RegularExpression: file_main_name_reg  # 配置需要验证主文件的匹配规则,对于文件全名匹配
            }
        ]

    def get_custom_affiliated_file_character(self):
        file_path = self.file_info.file_path
        affiliated_file_path = '矢量'.join(file_path.rsplit('影像', 1))  # 替换最后一个字符
        file_main_name = self.file_info.file_main_name
        affiliated_file_reg = '(?i)^'+file_main_name+'.*[.]shp$'
        return [
            {
                self.Name_FilePath: affiliated_file_path,  # 附属文件的路径
                self.Name_RegularExpression: affiliated_file_reg,  # 附属文件的匹配规则
                self.Name_No_Match_RegularExpression: None  # 应该从上面匹配到的文件剔除的文件的匹配规则
            }
        ]
