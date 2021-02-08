# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
import re

from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.custom.c_filePlugins_keyword import CFilePlugins_keyword


class plugins_1001_0001_zyff(CFilePlugins_keyword):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Catalog] = '天津海图'
        information[self.Plugins_Info_Catalog_Title] = '天津海图'
        information[self.Plugins_Info_Group] = '分幅数据'
        information[self.Plugins_Info_Group_Title] = '分幅数据'
        information[self.Plugins_Info_Type] = 'JB自由分幅'
        information[self.Plugins_Info_Type_Title] = 'JB自由分幅'
        return information

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,  # 配置数据文件名的匹配规则
                self.Name_RegularExpression: '(?i)^([^DKL]|[DKL][^SN]|[DKL][SN].{,2}$)'
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
        return []

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
            pathdata = pathdata_list[0][0]
        else:
            pathdata = ''
        node_item2 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item2, self.Name_Name, 'DataDate')
        xml_obj.set_element_text(node_item2, pathdata)  # 设置item节点与属性与内容

        # 影像元数据dsometadatajson.pixelsize.width节点
        # width < 0.01时，resolution = width * 110000,
        # width > 0.01时，resolution = width
        pixelsize_value = parser.metadata.metadata_json().xpath_one('pixelsize.width', None)
        if pixelsize_value is not None:
            pixelsize_num = CUtils.to_decimal(pixelsize_value, None)
            if pixelsize_num is not None:
                if CUtils.to_decimal(pixelsize_value, 0) < 0.01:
                    pixelsize_value = pixelsize_num * 110000
            else:
                pixelsize_value = ''
        else:
            pixelsize_value = ''
        pixelsize_value = CUtils.any_2_str(pixelsize_value)
        if len(pixelsize_value) > 10:
            pixelsize_value = pixelsize_value[:10]
        node_item3 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item3, self.Name_Name, 'Resolution')
        xml_obj.set_element_text(node_item3, pixelsize_value)  # 设置item节点与属性与内容

        SatelliteID_list = re.findall(
            r'(?i)^.+'
            r'[-_/]?[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[-_/]?'
            r'(.+)'
            r'[\\/]影像$',
            parser.file_info.file_path
        )
        if len(SatelliteID_list) > 0:
            SatelliteID = SatelliteID_list[0][2]
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
        if len(GeographicName_list) > 0:
            GeographicName = GeographicName_list[0][0]
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

        try:
            if xml_obj is not None:
                parser.metadata.set_metadata_bus(
                    self.Success,
                    '元数据文件成功构建! ',
                    self.MetaDataFormat_XML,
                    xml_obj.to_xml()
                )

                return CResult.merge_result(
                    self.Success,
                    '元数据文件成功构建! '
                )
            else:
                raise
        except Exception as error:
            parser.metadata.set_metadata_bus(
                self.Exception,
                '构建元数据文件失败, 无法处理! 错误原因为{0}'.format(error.__str__()),
                self.MetaDataFormat_Text,
                ''
            )
            return CResult.merge_result(
                self.Exception,
                '构建元数据文件失败, 无法处理! 错误原因为{0}'.format(error.__str__())
            )

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        """
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '//item[@name="DataDate"]',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '//item[@name="DataDate"]',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '//item[@name="DataDate"]',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[@name='ProductName']",
                self.Name_ID: 'ProductName',
                self.Name_Title: 'ProductName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[@name='DataDate']",
                self.Name_ID: 'DataDate',
                self.Name_Title: 'DataDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[@name='SatelliteID']",
                self.Name_ID: 'SatelliteID',
                self.Name_Title: 'SatelliteID',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[@name='Resolution']",
                self.Name_ID: 'Resolution',
                self.Name_Title: 'Resolution',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 10
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[@name='GeographicName']",
                self.Name_ID: 'GeographicName',
                self.Name_Title: 'GeographicName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[@name='Description']",
                self.Name_ID: 'Description',
                self.Name_Title: 'Description',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 500
            }
        ]
