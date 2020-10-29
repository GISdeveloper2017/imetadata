# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:22
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_guoqing.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
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
        todo 负责人 王学谦 在这里检验初始化国情的质检列表
        """
        # file_main_name = self.classified_object_name()
        # file_ext = self.file_info.__file_ext__
        # file_main_name_with_path = '{0}.{1}'.format(
        #     CFile.join_file(self.file_info.__file_path__, file_main_name), file_ext)  # 获取初始化需要的参数

        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.__file_name_with_full_path__))  # 调用默认的规则列表

        return list_qa

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return [
            {
                self.Name_XPath: 'pixelsize.width',
                self.Name_ID: 'pixelsize.width',
                self.Name_Title: '影像宽度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer_positive
            }, {
                self.Name_XPath: "coordinate",
                self.Name_ID: 'coordinate',
                self.Name_Title: '坐标系参考存在',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000
            }, {
                self.Name_XPath: "boundingbox.top",
                self.Name_ID: 'boundingbox.top',
                self.Name_Title: '经纬度坐标（top）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    }
            }, {
                self.Name_XPath: "boundingbox.left",
                self.Name_ID: 'boundingbox.left',
                self.Name_Title: '经纬度坐标（left）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    }
            }, {
                self.Name_XPath: "boundingbox.right",
                self.Name_ID: 'boundingbox.right',
                self.Name_Title: '经纬度坐标（right）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    }
            }, {
                self.Name_XPath: "boundingbox.bottom",
                self.Name_ID: 'boundingbox.bottom',
                self.Name_Title: '经纬度坐标（bottom）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    }
            }
        ]

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 王学谦 在这里将业务元数据***_21at.xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_src_filename_with_path is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本卫星数据无业务元数据, 无须解析!')

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

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        todo 负责人 王学谦
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/MetaDataFileName",
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
                self.Name_XPath: "/Metadatafile/SATEIMGSOURCE/SateName",
                self.Name_ID: 'SateName',
                self.Name_Title: '星源',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/PBandSensorType",
                self.Name_ID: 'PBandSensorType',
                self.Name_Title: '全色传感器',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/SateResolution",
                self.Name_ID: 'SateResolution',
                self.Name_Title: '全色分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/PBandOribitCode",
                self.Name_ID: 'PBandOribitCode',
                self.Name_Title: '全色轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/PBandDate",
                self.Name_ID: 'PBandDate',
                self.Name_Title: '拍摄日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_date
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/MultiBandSensorType",
                self.Name_ID: 'MultiBandSensorType',
                self.Name_Title: '多光谱传感器',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/MultiBandResolution",
                self.Name_ID: 'MultiBandResolution',
                self.Name_Title: '多光谱分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/MultiBandOrbitCode",
                self.Name_ID: 'MultiBandOrbitCode',
                self.Name_Title: '多光谱轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/MultiBandDate",
                self.Name_ID: 'MultiBandDate',
                self.Name_Title: '多光谱拍摄日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/MultiBandNum",
                self.Name_ID: 'MultiBandNum',
                self.Name_Title: '波段数量',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_integer
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/MultiBandName",
                self.Name_ID: 'MultiBandName',
                self.Name_Title: '波段名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }
        ]
