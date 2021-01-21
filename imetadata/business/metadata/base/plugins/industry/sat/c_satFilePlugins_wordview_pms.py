import datetime

from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_wordview_pms(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'WordView_PMS'
        information[self.Plugins_Info_Type_Title] = 'WordView星PMS传感器'
        information[self.Plugins_Info_Group] = 'WordView'
        information[self.Plugins_Info_Group_Title] = 'WordView'
        information[self.Plugins_Info_CopyRight] = 'DigitalGlobe Incorporated, Longmont CO USA 80503-6493'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^\d{11,12}_\d{2}.*', self.TextMatchType_Regex
        else:
            return r'(?i)^\d{11,12}_\d{2}.*[.]TIF', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i).*[-]P[0-9][A-Z]S.*.XML',
                '{0}.xml'.format(self.classified_object_name()), True
            )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*[-]P[0-9][A-Z]S.*[.]TIF',
                    '{0}.tif'.format(self.classified_object_name()), True
                ),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '影像文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*[-]M[0-9][A-Z]S.*[-]BROWSE.JPG',
                    '{0}-BROWSE.jpg'.format(self.classified_object_name()), True
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*[-]M[0-9][A-Z]S.*[-]BROWSE.JPG',
                    '{0}-BROWSE.jpg'.format(self.classified_object_name()), True
                )
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/isd/IMD/MAP_PROJECTED_PRODUCT/EARLIESTACQTIME|'
                                 '/isd/IMD/IMAGE/TLCTIME',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/isd/IMD/MAP_PROJECTED_PRODUCT/EARLIESTACQTIME|'
                                 '/isd/IMD/IMAGE/TLCTIME',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/isd/IMD/MAP_PROJECTED_PRODUCT/LATESTACQTIME|'
                                 '/isd/IMD/IMAGE/TLCTIME',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def get_metadata_bus_configuration_list(self) -> list:
        """
        固定的列表，重写时不可缺项
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # 卫星，必填，从元数据组织定义，必须是标准命名的卫星名称
                self.Name_XPath: '/isd/IMD/IMAGE/SATID'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_Value: 'PMS'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/ULLAT'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/ULLON'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/URLAT'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/URLON'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/LRLAT'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/LRLON'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/LLLAT'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/isd/IMD/BAND_P/LLLON'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: '(?i).*-M[0-9][A-Z]S.*-BROWSE.JPG'
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/isd/IMD/MAP_PROJECTED_PRODUCT/EARLIESTACQTIME|'
                                 '/isd/IMD/IMAGE/TLCTIME'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/isd/IMD/MAP_PROJECTED_PRODUCT/PRODUCTGSD|'
                                 '/isd/IMD/IMAGE/MEANPRODUCTGSD'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/isd/IMD/IMAGE/MAXOFFNADIRVIEWANGLE'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/isd/IMD/IMAGE/CLOUDCOVER'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/isd/RPB/SPECID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/isd/IMD/GENERATIONTIME'
            },
            {
                self.Name_ID: 'remark',  # 备注 可空
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productname',  # 产品名称，有的能从卫星元数据里面取，没有就不取
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'producttype',  # 产品类型 必填
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_ProductType, None)
            },
            {
                self.Name_ID: 'productattribute',  # 产品属性 必填
                self.Name_XPath: '/isd/IMD/PRODUCTLEVEL',
                self.Name_Map: {  # 映射，当取到的值为key时，将值转换为value
                    'LV1A': 'L1',
                    'LV2A': 'L2',
                    'LV4A': 'L4',
                    self.Name_Default: 'L1'  # 没有对应的的映射使用默认值
                }
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: '/isd/IMD/PRODUCTORDERID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，配置正则
                self.Name_Value: None
            }
        ]

