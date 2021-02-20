# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
import re

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.custom.c_filePlugins_keyword import CFilePlugins_keyword
from imetadata.business.metadata.inbound.plugins.file.plugins_8052_guoqing_frame import plugins_8052_guoqing_frame


class plugins_1000_1002_ffyx_tj2000(plugins_8052_guoqing_frame, CFilePlugins_keyword):
    Plugins_Info_Coordinate_System = 'coordinate_system'
    Plugins_Info_Coordinate_System_Title = 'coordinate_system_title'

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Project_ID] = 'tjch'
        information[self.Plugins_Info_Catalog] = '天津测绘'
        information[self.Plugins_Info_Catalog_Title] = '天津测绘'
        information[self.Plugins_Info_Group] = '成果影像'
        information[self.Plugins_Info_Group_Title] = '成果影像'
        information[self.Plugins_Info_Type] = '分幅影像'
        information[self.Plugins_Info_Type_Title] = '分幅影像'
        information[self.Plugins_Info_Type_Code] = '10001002'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        information[self.Plugins_Info_SpatialEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_ViewEngine] = self.BrowseEngine_Raster
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_TagsEngine] = None

        information[self.Plugins_Info_Coordinate_System] = 'tj2000'
        information[self.Plugins_Info_Coordinate_System_Title] = '2000天津城市坐标系'
        return information

    def classified(self):
        file_path = self.file_info.file_path
        file_ext = self.file_info.file_ext
        if CUtils.text_match_re(file_path, r'(?i)\d{4}.{2}[\\\\/]FenFu[\\\\/]' + self.get_coordinate_system_title()) \
                and CUtils.equal_ignore_case(file_ext, 'shp'):
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None
            return self._object_confirm, self._object_name
        else:
            return CFilePlugins_keyword.classified(self)

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: r'(?i)^.{10}\d{2}[pm]\d{4}[ao]$'  # 配置数据文件名的匹配规则
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
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: r'(?i)^.{10}\d{2}[pm]\d{4}[bcdmp]$'  # 配置附属文件名的匹配规则
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
                self.Name_RegularExpression: '(?i)^' + self.file_info.file_main_name[:-1] + '[ao].tif[f]?'
            }
        ]

    def get_custom_affiliated_file_character(self):
        file_path = self.file_info.file_path
        file_main_name = self.file_info.file_main_name
        regularexpression = '(?i)^' + file_main_name[:-1] + '.[.].*'

        shp_path_list = re.split(file_path, '(?i)[\\\\/]FenFu[\\\\/]' + self.get_coordinate_system_title())
        if len(shp_path_list) > 1:
            shp_path = file_path.replace(shp_path_list[1], '')
        else:
            if len(shp_path_list) > 0:
                shp_path = CFile.join_file(shp_path_list[0], 'FenFu', self.get_coordinate_system_title())
            else:
                shp_path = file_path
        if shp_path.endswith(r'/') or shp_path.endswith('\\'):
            shp_path = shp_path[:-1]
        return [
            {
                self.Name_FilePath: file_path,  # 附属文件的路径
                self.Name_RegularExpression: regularexpression,  # 附属文件的匹配规则
                # 应该从上面匹配到的文件剔除的文件的匹配规则
                self.Name_No_Match_RegularExpression: '(?i)^' + file_main_name + '[.].*$'
            }, {
                self.Name_FilePath: shp_path,  # 附属文件的路径
                self.Name_RegularExpression: '(?i).shp$',  # 附属文件的匹配规则
                # 应该从上面匹配到的文件剔除的文件的匹配规则
                self.Name_No_Match_RegularExpression: None
            }
        ]

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化ortho文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        完成 负责人 王学谦 在这里检验初始化ortho的质检列表
        """
        list_qa = list()
        file_main_name = self.file_info.file_main_name
        # 调用默认的规则列表
        list_qa.extend(self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))
        list_qa.extend([
            {
                self.Name_FileName: '{0}p.xml'.format(file_main_name[:-1]),
                self.Name_ID: 'p_xml',
                self.Name_Title: '投影信息文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.MetaDataFormat_XML
            }
        ])
        return list_qa

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        file_path = self.file_info.file_path
        shp_path_list = re.split(file_path, '(?i)[\\\\/]FenFu[\\\\/]' + self.get_coordinate_system_title())
        if len(shp_path_list) > 1:
            shp_path = file_path.replace(shp_path_list[1], '')
        else:
            if len(shp_path_list) > 0:
                shp_path = CFile.join_file(shp_path_list[0], 'FenFu', self.get_coordinate_system_title())
            else:
                shp_path = file_path
        if shp_path.endswith(r'/') or shp_path.endswith('\\'):
            shp_path = shp_path[:-1]

        shp_list = CFile.file_or_subpath_of_path(shp_path, '(?i).shp$', CFile.MatchType_Regex)
        if len(shp_list) == 0:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'shp_file',
                    self.Name_Title: '影像时相接边图',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少影像时相接边图'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: shp_list[0],
                    self.Name_ID: 'shp_file',
                    self.Name_Title: '影像时相接边图',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '影像时相接边图[{0}]存在'.format(shp_list[0])
                }
            )

    def get_coordinate_system(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System, None)

    def get_coordinate_system_title(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System_Title, None)
