from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_s2a_s2msi1c(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'S2A'
        information[self.Plugins_Info_Type_Title] = '哨兵二号'
        information[self.Plugins_Info_Group] = 'S2A'
        information[self.Plugins_Info_Group_Title] = '哨兵二号'
        information[self.Plugins_Info_CopyRight] = 'PDGS'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^S2A_MSIL1C.*', self.TextMatchType_Regex
        else:
            # 主文件为数据的方式存疑
            return r'(?i)^S2A_MSIL1C.*', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i).*INSPIRE[.]xml',
                'INSPIRE.xml', True
            )
        )

    def get_multiple_metadata_bus_filename_from_regex(self) -> dict:
        """
        return {
            'PAN': '',
            'MS': ''
        }
        """
        return {
            'MTD_TL': r'.*MTD_TL.xml',
            'INSPIRE': r'.*INSPIRE.xml',
            'MTD_MSIL1C': r'.*MTD_MSIL1C.xml'
        }

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return []

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*PVI[.]jp2',
                    'PVI.jp2', True
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*PVI[.]jp2',
                    'PVI.jp2', True
                )
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/n1:Level-1C_Tile_ID/n1:General_Info/SENSING_TIME',
                self.Name_Format: self.MetaDataFormat_XML,
                self.Name_Other_Metadata_Bus_Xml: 'MTD_TL'
            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//PRODUCT_START_TIME',
                self.Name_Format: self.MetaDataFormat_XML,
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//PRODUCT_STOP_TIME',
                self.Name_Format: self.MetaDataFormat_XML,
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            }
        ]

    def get_metadata_bus_configuration_list(self) -> list:
        """
        固定的列表，重写时不可缺项
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # 卫星，必填，从元数据组织定义，必须是标准命名的卫星名称
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//SPACECRAFT_NAME',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//PRODUCT_TYPE',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_Value: None
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/'
                                 'gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/'
                                 'gmd:northBoundLatitude/gco:Decimal'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/'
                                 'gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/'
                                 'gmd:westBoundLongitude/gco:Decimal'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/'
                                 'gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/'
                                 'gmd:northBoundLatitude/gco:Decimal'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent'
                                 '/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox'
                                 '/gmd:eastBoundLongitude/gco:Decimal'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent'
                                 '/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox'
                                 '/gmd:southBoundLatitude/gco:Decimal'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent'
                                 '/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox'
                                 '/gmd:eastBoundLongitude/gco:Decimal'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent'
                                 '/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox'
                                 '/gmd:southBoundLatitude/gco:Decimal'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent'
                                 '/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox'
                                 '/gmd:westBoundLongitude/gco:Decimal'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/n1:Level-1C_Tile_ID/n1:General_Info/Archiving_Info/ARCHIVING_TIME',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_TL'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//RESOLUTION',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/n1:Level-1C_Tile_ID/n1:Geometric_Info/Tile_Angles/Mean_Sun_Angle/ZENITH_ANGLE',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_TL'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:Quality_Indicators_Info/Cloud_Coverage_Assessment',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_XPath: '/n1:Level-1C_Tile_ID/n1:Geometric_Info//HORIZONTAL_CS_NAME',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_TL'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//GENERATION_TIME',
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: 'remark',  # 备注 可空
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productname',  # 产品名称，有的能从卫星元数据里面取，没有就不取
                self.Name_XPath: '/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation'
                                 '/gmd:CI_Citation/gmd:title/gco:CharacterString'
            },
            {
                self.Name_ID: 'producttype',  # 产品类型 必填
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_ProductType, None)
            },
            {
                self.Name_ID: 'productattribute',  # 产品属性 必填
                self.Name_XPath: '/n1:Level-1C_User_Product/n1:General_Info//PROCESSING_LEVEL',
                self.Name_Map: {  # 映射，当取到的值为key时，将值转换为value
                    'Level-1C': 'L1'
                },
                self.Name_Other_Metadata_Bus_Xml: 'MTD_MSIL1C'
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，配置正则
                self.Name_Value: None
            }
        ]
