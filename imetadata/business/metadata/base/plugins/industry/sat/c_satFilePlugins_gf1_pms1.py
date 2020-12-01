# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_pms1.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins


class CSatFilePlugins_gf1_pms1(CSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'GF1_PMS'
        information[self.Plugins_Info_Group_Name] = 'GF1'
        information[self.Plugins_Info_Group_Title] = '高分一号'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return 'gf1_pms1_*_l1a*', self.TextMatchType_Common
        else:
            return 'gf1_pms1_*_l1a*-pan1.tiff', self.TextMatchType_Common

    def get_classified_object_name_of_sat(self, sat_file_status) -> str:
        """
        当卫星数据是解压后的散落文件时, 如何从解压后的文件名中, 解析出卫星数据的原名
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        . 如果是散落文件, 则是针对文件的全名
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        """
        if sat_file_status == self.Sat_Object_Status_Zip:
            return self.file_info.file_main_name
        elif sat_file_status == self.Sat_Object_Status_Dir:
            return self.file_info.file_name_without_path
        else:
            return self.file_info.file_main_name.replace('-PAN1', '')

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            '{0}-PAN1.xml'.format(self.classified_object_name())
        )

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
            {
                self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '全色文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            },
            {
                self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()),
                self.Name_ID: 'mss_tif',
                self.Name_Title: '多光谱文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser):
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/OrbitID',
                self.Name_ID: 'OrbitID',
                self.Name_Title: '轨道编号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/ProduceType',
                self.Name_ID: 'ProduceType',
                self.Name_Title: '产品类型',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/ProductLevel',
                self.Name_ID: 'ProductLevel',
                self.Name_Title: '产品属性',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/TopLeftLatitude',
                self.Name_ID: 'TopLeftLatitude',
                self.Name_Title: '左上角纬度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/TopLeftLongitude',
                self.Name_ID: 'TopLeftLongitude',
                self.Name_Title: '左上角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/TopRightLatitude',
                self.Name_ID: 'TopRightLatitude',
                self.Name_Title: '右上角纬度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/TopRightLongitude',
                self.Name_ID: 'TopRightLongitude',
                self.Name_Title: '右上角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/BottomRightLatitude',
                self.Name_ID: 'BottomRightLatitude',
                self.Name_Title: '右下角纬度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/BottomRightLongitude',
                self.Name_ID: 'BottomRightLongitude',
                self.Name_Title: '右下角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/BottomLeftLatitude',
                self.Name_ID: 'BottomLeftLatitude',
                self.Name_Title: '左下角纬度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/BottomLeftLongitude',
                self.Name_ID: 'BottomLeftLongitude',
                self.Name_Title: '左下角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_DataType: self.value_type_decimal
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/ProduceTime',
                self.Name_ID: 'ProduceTime',
                self.Name_Title: '发布时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/StartTime',
                self.Name_ID: 'StartTime',
                self.Name_Title: '开始时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/EndTime',
                self.Name_ID: 'EndTime',
                self.Name_Title: '结束时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/ImageGSD',
                self.Name_ID: 'ImageGSD',
                self.Name_Title: '分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_integer
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/CenterTime',
                self.Name_ID: 'CenterTime',
                self.Name_Title: '影像获取时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/RollViewingAngle',
                self.Name_ID: 'RollViewingAngle',
                self.Name_Title: '侧摆角',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_DataType: self.value_type_decimal

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: '/ProductMetaData/CloudPercent',
                self.Name_ID: 'CloudPercent',
                self.Name_Title: '云量',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer

            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/ProductMetaData/CenterTime',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/ProductMetaData/StartTime',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/ProductMetaData/EndTime',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def parser_metadata_spatial_after_qa(self, parser: CMetaDataParser):
        """
        继承本方法, 对详细的空间元数据信息进行处理
        注意:
            super().parser_metadata_spatial_after_qa(parser)
            要写在自定义的空间信息提取之后!!!
            完成 负责人 邢凯凯 继承本方法, 因为卫星数据的特殊性, 可以只取中心点和外包框

        :param parser:
        :return:
        """
        xml = parser.metadata.metadata_bus_xml()
        TopLeftLatitude = xml.xpath_one('/ProductMetaData/TopLeftLatitude')
        TopLeftLongitude = xml.xpath_one('/ProductMetaData/TopLeftLongitude')
        BottomRightLatitude = xml.xpath_one('/ProductMetaData/TopLeftLatitude')
        BottomRightLongitude = xml.xpath_one('/ProductMetaData/TopLeftLongitude')

        center_latitude = (float(xml.get_element_text(TopLeftLatitude)) + float(
            xml.get_element_text(BottomRightLatitude))) / 2
        center_longitude = (float(xml.get_element_text(TopLeftLongitude)) + float(
            xml.get_element_text(BottomRightLongitude))) / 2

        TopLeftLatitude_text = xml.get_element_text(TopLeftLatitude)
        TopLeftLongitude_text = xml.get_element_text(TopLeftLongitude)
        BottomLeftLatitude_text = xml.get_element_text(xml.xpath_one('/ProductMetaData/BottomLeftLatitude'))
        BottomLeftLongitude_text = xml.get_element_text(xml.xpath_one('/ProductMetaData/BottomLeftLongitude'))
        TopRightLatitude_text = xml.get_element_text(xml.xpath_one('/ProductMetaData/TopRightLatitude'))
        TopRightLongitude_text = xml.get_element_text(xml.xpath_one('/ProductMetaData/TopRightLongitude'))
        BottomRightLatitude_text = xml.get_element_text(BottomRightLatitude)
        BottomRightLongitude_text = xml.get_element_text(BottomRightLongitude)

        native_center_filename_with_path = CFile.join_file(self.file_content.work_root_dir,
                                                           '{0}_native_center.wkt'.format(CUtils.one_id()))
        native_bbox_filename_with_path = CFile.join_file(self.file_content.work_root_dir,
                                                         '{0}_native_bbox.wkt'.format(CUtils.one_id()))
        CFile.str_2_file('point({0} {1})'.format(center_latitude, center_longitude), native_center_filename_with_path)
        CFile.str_2_file(
            'POLYGON( ({0} {1},{2} {3},{4} {5},{6} {7},{0} {1}) )'.format(
                BottomLeftLatitude_text, BottomLeftLongitude_text,
                TopLeftLatitude_text, TopLeftLongitude_text,
                TopRightLatitude_text, TopRightLongitude_text,
                BottomRightLatitude_text, BottomRightLongitude_text
            )
            ,
            native_bbox_filename_with_path)

        parser.metadata.set_metadata_spatial(self.Success, '', self.Spatial_MetaData_Type_Native_Center,
                                             native_center_filename_with_path)
        parser.metadata.set_metadata_spatial(self.Success, '', self.Spatial_MetaData_Type_Native_BBox,
                                             native_bbox_filename_with_path)

        super().parser_metadata_spatial_after_qa(parser)

        return CResult.merge_result(
            self.Success,
            '数据文件[{0}]的空间信息解析成功! '.format(self.file_info.file_name_with_full_path)
        )

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: '{0}-PAN1.jpg'.format(self.classified_object_name())
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: '{0}-PAN1_thumb.jpg'.format(self.classified_object_name())
            }
        ]
