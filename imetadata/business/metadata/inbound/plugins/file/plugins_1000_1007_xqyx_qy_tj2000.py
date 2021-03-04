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


class plugins_1000_1007_xqyx_qy_tj2000(CFilePlugins_keyword):
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
        information[self.Plugins_Info_Type_Code] = '02010601'
        information[self.Plugins_Info_Is_Spatial] = self.DB_True
        information[self.Plugins_Info_Is_Dataset] = self.DB_False
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
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_tjch_xqyx'
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
            return super().classified()

    def get_classified_character_of_object_keyword(self):
        """
        设置识别的特征
        """
        return [
            {
                self.Name_ID: self.Name_FileName,
                self.Name_RegularExpression: r'(?i).*_\d{6,8}_.{3}_.*_' + self.get_coordinate_system()  # 配置数据文件名的匹配规则
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
                self.Name_ID: self.Name_FileName,  # 配置数据文件名的匹配规则
                self.Name_RegularExpression: r'.*_\d{6,8}_.{3}_.*_' + self.get_coordinate_system() +
                                             r'|.*_.{3}_.*_' + self.get_coordinate_system()
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
        letter_location = file_path.find('镶嵌影像成果')
        shp_path = CFile.join_file(file_path[:letter_location - 1], '影像时相接边图', self.get_yuji())
        shp_regularexpression = '(?i)^.*_.*_' + self.get_coordinate_system() + r'\.shp$'
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
        return [
            {
                self.Name_FileName: self.file_info.file_name_without_path,
                self.Name_ID: 'img',
                self.Name_Title: 'IMG影像',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        file_path = self.file_info.file_path

        letter_location = file_path.find('镶嵌影像成果')
        shp_path = CFile.join_file(file_path[:letter_location - 1], '影像时相接边图', self.get_yuji())
        shp_regularexpression = '(?i)^.*_.*_' + self.get_coordinate_system() + r'\.shp$'
        shp_list = CFile.file_or_subpath_of_path(shp_path, shp_regularexpression, CFile.MatchType_Regex)
        if len(shp_list) == 0:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'shp_file',
                    self.Name_Title: '影像时相接边图',
                    self.Name_Result: self.QA_Result_Warn,
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
        通过相应信息转换xml
        """
        file_main_name = parser.file_info.file_main_name
        file_path = parser.file_info.file_path
        xml_obj = CXml()  # 建立xml对象
        node_root = xml_obj.new_xml('root')

        node_item1 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item1, self.Name_Name, 'ProductName')
        xml_obj.set_element_text(node_item1, file_main_name)  # 设置item节点与属性与内容

        if CUtils.text_match_re(file_main_name, r'.*_\d{6,8}_.{3}_.*_' + self.get_coordinate_system()):
            pathdata_list = re.findall(
                r'.*_(\d{6,8})_.{3}_.*_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                pathdata = CUtils.any_2_str(pathdata_list[0])
            else:
                pathdata = ''
        else:
            pathdata_list = re.findall(
                r'(?i)(\d{4}.{2})[\\\\/]镶嵌影像成果',
                file_path
            )
            if len(pathdata_list) > 0:
                pathdata = CUtils.any_2_str(pathdata_list[0])
            else:
                pathdata = ''
        node_item2 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item2, self.Name_Name, 'DataDate')
        xml_obj.set_element_text(node_item2, pathdata)  # 设置item节点与属性与内容

        if CUtils.text_match_re(file_main_name, r'.*_\d{6,8}_.{3}_.*_' + self.get_coordinate_system()):
            pixelsize_list = re.findall(
                r'.*_\d{6,8}_.{3}_(.*)_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                pixelsize = CUtils.any_2_str(pixelsize_list[0])
            else:
                pixelsize = ''
        elif CUtils.text_match_re(file_main_name, r'.*_.{3}_.*_' + self.get_coordinate_system()):
            pixelsize_list = re.findall(
                r'.*_.{3}_(.*)_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                pixelsize = CUtils.any_2_str(pixelsize_list[0])
            else:
                pixelsize = ''
        else:
            pixelsize = ''
        if CUtils.text_match_re(pixelsize, r'^\d+[a-zA-z]+$'):
            pixelsize_list = re.findall(r'(\d+)[a-zA-z]+', pixelsize)
            if len(pathdata_list) > 0:
                pixelsize = CUtils.any_2_str(pixelsize_list[0])

        if len(pixelsize) == 2:
            pixelsize_value = '{0}.{1}'.format(pixelsize[:1], pixelsize[-1:])
        else:
            pixelsize_value = pixelsize
        node_item3 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item3, self.Name_Name, 'Resolution')
        xml_obj.set_element_text(node_item3, pixelsize_value)  # 设置item节点与属性与内容

        if CUtils.text_match_re(file_main_name, r'.*_\d{6,8}_.{3}_.*_' + self.get_coordinate_system()):
            SatelliteID_list = re.findall(
                r'.*_\d{6,8}_(.{3})_.*_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                SatelliteID = CUtils.any_2_str(SatelliteID_list[0])
            else:
                SatelliteID = ''
        elif CUtils.text_match_re(file_main_name, r'.*_.{3}_.*_' + self.get_coordinate_system()):
            SatelliteID_list = re.findall(
                r'.*_(.{3})_.*_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                SatelliteID = CUtils.any_2_str(SatelliteID_list[0])
            else:
                SatelliteID = ''
        else:
            SatelliteID = ''
        node_item4 = xml_obj.create_element(node_root, 'item')
        xml_obj.set_attr(node_item4, self.Name_Name, 'SatelliteID')
        xml_obj.set_element_text(node_item4, SatelliteID)  # 设置item节点与属性与内容

        if CUtils.text_match_re(file_main_name, r'.*_\d{6,8}_.{3}_.*_' + self.get_coordinate_system()):
            GeographicName_list = re.findall(
                r'(.*)_\d{6,8}_.{3}_.*_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                GeographicName = CUtils.any_2_str(GeographicName_list[0])
            else:
                GeographicName = ''
        elif CUtils.text_match_re(file_main_name, r'.*_.{3}_.*_' + self.get_coordinate_system()):
            GeographicName_list = re.findall(
                r'(.*)_.{3}_.*_' + self.get_coordinate_system(),
                file_main_name
            )
            if len(pathdata_list) > 0:
                GeographicName = CUtils.any_2_str(GeographicName_list[0])
            else:
                GeographicName = ''
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
                self.Name_Width: 50
            }
            # {
            #     self.Name_Type: self.QA_Type_XML_Node_Exist,
            #     self.Name_XPath: "//item[@name='Description']",
            #     self.Name_ID: 'Description',
            #     self.Name_Title: 'Description',
            #     self.Name_Group: self.QA_Group_Data_Integrity,
            #     self.Name_Result: self.QA_Result_Error,
            #     self.Name_DataType: self.value_type_string,
            #     self.Name_Width: 500
            # }
        ]

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

    def get_coordinate_system(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System, None)

    def get_coordinate_system_title(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System_Title, None)

    def get_yuji(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_yuji, None)

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

    def parser_metadata_spatial_after_qa(self, parser: CMetaDataParser):
        """
        在这里直接指定坐标系
        """
        result = super().parser_metadata_spatial_after_qa(parser)
        try:
            Prj_Project = CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System, '')
            if not CUtils.equal_ignore_case(Prj_Project, ''):
                parser.metadata.set_metadata_spatial(
                    self.DB_True,
                    '元数据文件[{0}]成功加载! '.format(self.file_info.file_name_with_full_path),
                    self.Spatial_MetaData_Type_Prj_Project,
                    Prj_Project
                )
                parser.metadata.set_metadata_spatial(
                    self.DB_True,
                    '元数据文件[{0}]成功加载! '.format(self.file_info.file_name_with_full_path),
                    self.Spatial_MetaData_Type_Prj_Source,
                    self.Prj_Source_Custom
                )
        except Exception as error:
            parser.metadata.set_metadata_spatial(
                self.DB_False,
                '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(self.file_info.file_name_with_full_path,
                                                           error.__str__()),
                self.MetaDataFormat_Text,
                '')
            return CResult.merge_result(self.Exception,
                                        '元数据文件[{0}]格式不合法, 无法处理! '.format(
                                            self.file_info.file_name_with_full_path))
        return result
