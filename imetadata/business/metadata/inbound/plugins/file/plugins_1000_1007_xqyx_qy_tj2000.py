# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
import re

from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.custom.c_filePlugins_keyword import CFilePlugins_keyword
from imetadata.business.metadata.inbound.plugins.file.plugins_8030_mosaic import plugins_8030_mosaic


class plugins_1000_1007_xqyx_qy_tj2000(plugins_8030_mosaic, CFilePlugins_keyword):
    Plugins_Info_Coordinate_System = 'coordinate_system'
    Plugins_Info_Coordinate_System_Title = 'coordinate_system_title'
    Plugins_Info_yuji = 'yuji'

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Project_ID] = 'tjch'
        information[self.Plugins_Info_Catalog] = '天津测绘'
        information[self.Plugins_Info_Catalog_Title] = '天津测绘'
        information[self.Plugins_Info_Group] = '成果影像'
        information[self.Plugins_Info_Group_Title] = '成果影像'
        information[self.Plugins_Info_Type] = '区域镶嵌'
        information[self.Plugins_Info_Type_Title] = '区域镶嵌'
        information[self.Plugins_Info_Type_Code] = '10001007'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        information[self.Plugins_Info_SpatialEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_ViewEngine] = self.BrowseEngine_Raster
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_TagsEngine] = None

        information[self.Plugins_Info_Coordinate_System] = 'tj2000'
        information[self.Plugins_Info_Coordinate_System_Title] = '2000天津城市坐标系'
        information[self.Plugins_Info_yuji] = '区域镶嵌'
        return information

    def classified(self):
        file_path = self.file_info.file_path
        file_ext = self.file_info.file_ext
        if CUtils.text_match_re(file_path, r'(?i)\d{4}.{2}[\\\\/]影像时相接边图[\\\\/]' + self.get_yuji()) and \
                CUtils.equal_ignore_case(file_ext, 'shp'):
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
                self.Name_RegularExpression: r'(?i).*_\d{8}_.{3}_.*_' + self.get_coordinate_system()  # 配置数据文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,  # 配置数据文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)\d{4}.{2}[\\\\/]镶嵌影像成果[\\\\/]' +
                                             self.get_yuji() + '[\\\\/]' + self.get_coordinate_system_title()
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.Name_RegularExpression: '(?i)^img$'  # 配置数据文件后缀名的匹配规则
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
                self.Name_RegularExpression: r'(?i).*_\d{8}_.{3}_.*_' + self.get_coordinate_system()  # 配置数据文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,  # 配置数据文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)\d{4}.{2}[\\\\/]镶嵌影像成果[\\\\/]' +
                                             self.get_yuji() + '[\\\\/]' + self.get_coordinate_system_title()
            },
            {
                self.Name_ID: self.Name_FileExt,
                self.Name_RegularExpression: '.*'  # 配置附属文件后缀名的匹配规则
            },
            {
                self.Name_ID: self.Name_FileMain,  # 配置需要验证主文件存在性的 文件路径
                self.Name_FilePath: self.file_info.file_path,
                # 配置需要验证主文件的匹配规则,对于文件全名匹配
                self.Name_RegularExpression: r'(?i)' + self.file_info.file_main_name + '.img'
            }
        ]

    def get_custom_affiliated_file_character(self):
        file_path = self.file_info.file_path

        shp_path_list = re.split(
            file_path,
            '(?i)[\\\\/]镶嵌影像成果[\\\\/]' + self.get_yuji() + '[\\\\/]' + self.get_coordinate_system_title()
        )
        if len(shp_path_list) > 0:
            time_path = CFile.file_name(shp_path_list[0])
            shp_path = CFile.join_file(shp_path_list[0], '影像时相接边图', self.get_yuji())
            shp_regularexpression = '(?i)^' + time_path + '_.*_' + self.get_coordinate_system() + '[.]shp$'
        else:
            shp_path = CFile.join_file('镶嵌影像成果', self.get_yuji(), self.get_coordinate_system_title())
            shp_path = file_path.replace(shp_path, '影像时相接边图' + CFile.sep() + self.get_yuji())
            shp_regularexpression = '(?i)^.*_.*_' + self.get_coordinate_system() + '[.]shp$'
        return [
            {
                self.Name_FilePath: shp_path,  # 附属文件的路径
                self.Name_RegularExpression: shp_regularexpression,  # 附属文件的匹配规则
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
        # 调用默认的规则列表
        # list_qa.extend(self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))
        return list_qa

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        file_path = self.file_info.file_path

        shp_path_list = re.split(
            file_path,
            '(?i)[\\\\/]镶嵌影像成果[\\\\/]' + self.get_yuji() + '[\\\\/]' + self.get_coordinate_system_title()
        )
        if len(shp_path_list) > 0:
            time_path = CFile.file_name(shp_path_list[0])
            shp_path = CFile.join_file(shp_path_list[0], '影像时相接边图', self.get_yuji())
            shp_regularexpression = '(?i)^' + time_path + '_.*_' + self.get_coordinate_system() + '[.]shp$'
        else:
            shp_path = CFile.join_file('镶嵌影像成果', self.get_yuji(), self.get_coordinate_system_title())
            shp_path = file_path.replace(shp_path, '影像时相接边图' + CFile.sep() + self.get_yuji())
            shp_regularexpression = '(?i)^.*_.*_' + self.get_coordinate_system() + '[.]shp$'

        shp_list = CFile.file_or_subpath_of_path(shp_path, shp_regularexpression, CFile.MatchType_Regex)
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

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml或json格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        parser.metadata.set_metadata_bus(self.Not_Support, None, self.MetaDataFormat_Text, None)
        return CResult.merge_result(self.Success, '不支持解析业务元数据! ')

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        return list()

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return list()

    def get_coordinate_system(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System, None)

    def get_coordinate_system_title(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System_Title, None)

    def get_yuji(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_yuji, None)
