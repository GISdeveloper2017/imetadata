# -*- coding: utf-8 -*-
# @Time : 2020/9/15 09:54
# @Author : 王西亚
# @File : plugins_4001_triplesat_pms.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.custom.c_filePlugins_keyword import CFilePlugins_keyword


class plugins_1000_1002_ffyx_tj2000(CFilePlugins_keyword):
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
            return super().classified()

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
                self.Name_RegularExpression: r'(?i)^.{10}\d{2}[pm]\d{4}[o' + RegularExpression_letter + ']$'
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
                self.Name_RegularExpression: r'(?i)^.{10}\d{2}[pm]\d{4}[' + RegularExpression_letter + 'mp]$'
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
                                             '[o' + RegularExpression_main_letter + r']\.tif[f]?'
            }
        ]

    def get_custom_affiliated_file_character(self):
        file_path = self.file_info.file_path
        file_main_name = self.file_info.file_main_name
        regularexpression = '(?i)^' + file_main_name[:-1] + r'.\..*'

        letter_location_FenFu = file_path.find('FenFu')
        file_path_sub = file_path[letter_location_FenFu + 6:]
        letter_location = file_path_sub.find(CFile.sep())
        shp_path = CFile.join_file(file_path[:letter_location_FenFu + 5], file_path_sub[:letter_location])
        return [
            {
                self.Name_FilePath: file_path,  # 附属文件的路径
                self.Name_RegularExpression: regularexpression,  # 附属文件的匹配规则
                # 应该从上面匹配到的文件剔除的文件的匹配规则
                self.Name_No_Match_RegularExpression: '(?i)^' + file_main_name + r'\..*$'
            }, {
                self.Name_FilePath: shp_path,  # 附属文件的路径
                self.Name_RegularExpression: r'(?i)\.shp$',  # 附属文件的匹配规则
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
                self.Name_FileName: '{0}P.xml'.format(file_main_name[:-1]),
                self.Name_ID: 'P_xml',
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
        file_path = self.file_info.file_path
        file_main_name = self.file_info.file_main_name
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        metadata_name_with_path = CFile.join_file(file_path, '{0}M.xml'.format(file_main_name[:-1]))
        if CFile.file_or_path_exist(metadata_name_with_path):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = metadata_name_with_path

        if not check_file_metadata_bus_exist:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: self.metadata_bus_src_filename_with_path,
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '业务元数据[{0}]存在'.format(
                        CFile.file_name(self.metadata_bus_src_filename_with_path)
                    )
                }
            )

        letter_location_FenFu = file_path.find('FenFu')
        file_path_sub = file_path[letter_location_FenFu + 6:]
        letter_location = file_path_sub.find(CFile.sep())
        shp_path = CFile.join_file(file_path[:letter_location_FenFu + 5], file_path_sub[:letter_location])
        shp_list = CFile.file_or_subpath_of_path(shp_path, '(?i).shp$', CFile.MatchType_Regex)
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

    def get_coordinate_system(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System, None)

    def get_coordinate_system_title(self):
        return CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Coordinate_System_Title, None)

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        完成 负责人 王学谦 在这里将业务元数据***Y/M/P.xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            return CResult.merge_result(
                self.Failure,
                '数据{0}无业务元数据文件，请检查数据业务元数据文件是否存在!'.format(self.file_info.file_main_name)
            )

        transformer = CMDTransformerCommon(
            parser.object_id,
            parser.object_name,
            parser.file_info,
            parser.file_content,
            parser.metadata,
            self.metadata_bus_transformer_type,
            self.metadata_bus_src_filename_with_path
        )
        return transformer.process()

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        """
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: "//PhotoDate|PbandDate|MultiBandDate",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: "//PhotoDate|PbandDate|MultiBandDate",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: "//PhotoDate|PbandDate|MultiBandDate",
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
        qa_metadata_bus_xml_list = [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//MetaDataFileName",
                self.Name_ID: 'MetaDataFileName',
                self.Name_Title: '带扩展名元数据文件名',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 60
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ProductName",
                self.Name_ID: 'ProductName',
                self.Name_Title: '对象名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Owner",
                self.Name_ID: 'Owner',
                self.Name_Title: '所有者',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Producer",
                self.Name_ID: 'Producer',
                self.Name_Title: '生产商',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Publisher",
                self.Name_ID: 'Publisher',
                self.Name_Title: '出版商',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ProduceDate",
                self.Name_ID: 'ProduceDate',
                self.Name_Title: '生产日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_date,
                self.Name_NotNull: True
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ConfidentialLevel",
                self.Name_ID: 'ConfidentialLevel',
                self.Name_Title: '密级',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/GroundResolution",
                self.Name_ID: 'GroundResolution',
                self.Name_Title: '地面分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 10
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ImgColorModel",
                self.Name_ID: 'ImgColorModel',
                self.Name_Title: '影像类型',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/PixelBits",
                self.Name_ID: 'PixelBits',
                self.Name_Title: '位深',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/DataFormat",
                self.Name_ID: 'DataFormat',
                self.Name_Title: '格式',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 25
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Mathfoundation/MapProjection",
                self.Name_ID: 'MapProjection',
                self.Name_Title: '地图投影',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//SateName",
                self.Name_ID: 'SateName',
                self.Name_Title: '星源',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            }
        ]
        try:
            imgtype = parser.metadata.metadata_bus_xml().get_element_text_by_xpath_one('//ImgSource')
        except Exception:
            imgtype = None
        if CUtils.equal_ignore_case(imgtype, '0'):
            qa_metadata_bus_xml_list.extend([
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//CameraType",
                    self.Name_ID: 'CameraType',
                    self.Name_Title: '航摄仪型号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//DigitalPhotoResolution",
                    self.Name_ID: 'DigitalPhotoResolution',
                    self.Name_Title: '航片分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_decimal_or_integer,
                    self.Name_Width: 8
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//PhotoDate",
                    self.Name_ID: 'PhotoDate',
                    self.Name_Title: '航片日期',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_date
                }
            ])
        elif CUtils.equal_ignore_case(imgtype, '1'):
            qa_metadata_bus_xml_list.extend([
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//PBandSensorType",
                    self.Name_ID: 'PBandSensorType',
                    self.Name_Title: '全色传感器',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//SateResolution",
                    self.Name_ID: 'SateResolution',
                    self.Name_Title: '全色分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_decimal_or_integer,
                    self.Name_Width: 8
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//PbandOrbitCode",
                    self.Name_ID: 'PBandOribitCode',
                    self.Name_Title: '全色轨道号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 38
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//PbandDate",
                    self.Name_ID: 'PbandDate',
                    self.Name_Title: '全色拍摄日期',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_date
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//MultiBandSensorType",
                    self.Name_ID: 'MultiBandSensorType',
                    self.Name_Title: '多光谱传感器或航摄仪型号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//MultiBandResolution",
                    self.Name_ID: 'MultiBandResolution',
                    self.Name_Title: '多光谱分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_decimal_or_integer,
                    self.Name_Width: 8
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//MultiBandOrbitCode",
                    self.Name_ID: 'MultiBandOrbitCode',
                    self.Name_Title: '多光谱轨道号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//MultiBandDate",
                    self.Name_ID: 'MultiBandDate',
                    self.Name_Title: '多光谱拍摄日期',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_decimal_or_integer
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//MultiBandNum",
                    self.Name_ID: 'MultiBandNum',
                    self.Name_Title: '多光谱波段数量',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_decimal_or_integer
                }, {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//MultiBandName",
                    self.Name_ID: 'MultiBandName',
                    self.Name_Title: '多光谱波段名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20
                }
            ])
        else:
            qa_metadata_bus_xml_list.extend([
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_XPath: "//ImgSource",
                    self.Name_ID: 'ImgSource',
                    self.Name_Title: '影像数据源类型',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_NotNull: True,
                    self.Name_List: ['0', '1']
                }
            ])
        return qa_metadata_bus_xml_list

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
