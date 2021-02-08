# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
import re

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.custom.c_filePlugins_keyword import CFilePlugins_keyword


class plugins_1001_0002_bzff(CFilePlugins_keyword):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津海图'
        information[self.Plugins_Info_Catalog_Title] = '天津海图'
        information[self.Plugins_Info_Group] = '分幅数据'
        information[self.Plugins_Info_Group_Title] = '分幅数据'
        information[self.Plugins_Info_Type] = 'JB标准分幅'
        information[self.Plugins_Info_Type_Title] = 'JB标准分幅'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        information[self.Plugins_Info_SpatialEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_ViewEngine] = self.BrowseEngine_Raster
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: '(?i)^[DKL][SN].{3,10}.*$'  # 配置数据文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,  # 配置数据文件路径的匹配规则
                self.Name_RegularExpression: r'(?i)^.+'
                                             r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
                                             r'.+'
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
        file_main_name_reg = '(?i)^' + file_main_name + '.*[.](img|tif|tiff)'
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: '(?i)^[DKL][SN].{3,10}$'  # 配置附属文件名的匹配规则
            },
            {
                self.Name_ID: self.Name_FilePath,
                self.Name_RegularExpression: r'(?i)^.+'
                                             r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
                                             r'.+'
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
        file_object_name_list = re.split('[-_/]', file_main_name, 1)
        affiliated_file_reg = '(?i)^' + file_object_name_list[0] + '.*[.].*$'
        return [
            {
                self.Name_FilePath: affiliated_file_path,  # 附属文件的路径
                self.Name_RegularExpression: affiliated_file_reg,  # 附属文件的匹配规则
                self.Name_No_Match_RegularExpression: None  # 应该从上面匹配到的文件剔除的文件的匹配规则
            }
        ]

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化ortho文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        完成 负责人 王学谦 在这里检验初始化ortho的质检列表
        """
        list_qa = list()
        # 调用默认的规则列表
        list_qa.extend(self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))
        return list_qa

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        完成 负责人 李宪
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer_positive,
                self.Name_XPath: 'pixelsize.width',
                self.Name_ID: 'width',
                self.Name_Title: '影像宽度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000,
                self.Name_XPath: 'coordinate.proj4',
                self.Name_ID: 'coordinate',
                self.Name_Title: '坐标参考系',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_XPath: 'wgs84.boundingbox.top',
                self.Name_ID: 'top',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_XPath: 'wgs84.boundingbox.left',
                self.Name_ID: 'left',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_XPath: 'wgs84.boundingbox.right',
                self.Name_ID: 'right',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_XPath: 'wgs84.boundingbox.bottom',
                self.Name_ID: 'bottom',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        通过相应信息转换xml
        """
        xml_obj = CXml()  # 建立xml对象
        node_root = xml_obj.new_xml('root')

        node_item1 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item1, self.Name_Name, 'ProductName')
        xml_obj.set_element_text(node_item1, parser.file_info.file_main_name)  # 设置item节点与属性与内容

        pathdata_list = re.findall(
            r'(?i)^.+'
            r'[-_/]?([1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1]))[-_/]?'
            r'.+'
            r'[\\/]影像$',
            parser.file_info.file_path
        )
        if len(pathdata_list) > 0:
            pathdata = pathdata_list[0]
        else:
            pathdata = ''
        node_item2 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item2, self.Name_Name, 'DataDate')
        xml_obj.set_element_text(node_item2, pathdata[0])  # 设置item节点与属性与内容

        node_item3 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item3, self.Name_Name, 'Resolution')
        xml_obj.set_element_text(node_item3, '')  # 设置item节点与属性与内容

        SatelliteID_list = re.findall(
            r'(?i)^.+'
            r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
            r'(.+)'
            r'[\\/]影像$',
            parser.file_info.file_path
        )
        if len(pathdata_list) >= 3:
            SatelliteID = SatelliteID_list[3]
        else:
            SatelliteID = ''
        node_item4 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item4, self.Name_Name, 'SatelliteID')
        xml_obj.set_element_text(node_item4, SatelliteID)  # 设置item节点与属性与内容

        GeographicName_list = re.findall(
            r'(?i)^(.+)'
            r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
            r'.+'
            r'[\\/]影像$',
            parser.file_info.file_path
        )
        if len(pathdata_list) > 0:
            GeographicName = GeographicName_list[0]
            if CUtils.text_match_re(GeographicName, '[-_/]$'):
                GeographicName = GeographicName[:-1]
            GeographicName = CFile.file_main_name(GeographicName)
        else:
            GeographicName = ''
        node_item5 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item5, self.Name_Name, 'GeographicName')
        xml_obj.set_element_text(node_item5, GeographicName)  # 设置item节点与属性与内容

        node_item6 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item6, self.Name_Name, 'Description')
        xml_obj.set_element_text(node_item6, '')  # 设置item节点与属性与内容
        return xml_obj
