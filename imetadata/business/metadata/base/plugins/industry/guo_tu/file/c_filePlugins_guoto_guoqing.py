# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:22
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_guoqing.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class CFilePlugins_GUOTU_GuoQing(CFilePlugins_GUOTU):
    """
    国情影像
    """

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化国情文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        完成 负责人 王学谦 在这里检验初始化国情的质检列表
        """
        # file_main_name = self.classified_object_name()
        # file_ext = self.file_info.file_ext
        # file_main_name_with_path = '{0}.{1}'.format(
        #     CFile.join_file(self.file_info.file_path, file_main_name), file_ext)  # 获取初始化需要的参数

        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))  # 调用默认的规则列表

        return list_qa

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
