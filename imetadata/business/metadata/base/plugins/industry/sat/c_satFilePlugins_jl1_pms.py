from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_jl1_pms(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'JL1_PMS'
        information[self.Plugins_Info_Type_Title] = '吉林一号PMS传感器'
        information[self.Plugins_Info_Group] = 'JL1'
        information[self.Plugins_Info_Group_Title] = '吉林一号'
        information[self.Plugins_Info_CopyRight] = '长光卫星技术有限公司'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^JL\d{2,4}(A|B)_[A-Z]{3}_\d{13,15}_\d{8,10}_\d{2,4}_\d{3,5}_\d{2,4}', self.TextMatchType_Regex
        else:
            return r'(?i)^JL\d{2,4}(A|B)_[A-Z]{3}_\d{13,15}_\d{8,10}_\d{2,4}_\d{3,5}_\d{2,4}' \
                   r'.*_PAN[.]tif[f]?', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i)' + self.classified_object_name() + '.*PAN.*[_]meta[.]xml',
                '{0}_L1_PAN_meta.xml'.format(self.classified_object_name())
            )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    '(?i)'+self.classified_object_name()+'.*PAN[.]tif[f]?',
                    '{0}_L1_PAN.tif'.format(self.classified_object_name())
                ),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '影像文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            },
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    '(?i)' + self.classified_object_name() + '.*PAN[.]dbf',
                    '{0}_L1_PAN.dbf'.format(self.classified_object_name())
                ),
                self.Name_ID: 'shp_dbf',
                self.Name_Title: '矢量文件dbf',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    '(?i)' + self.classified_object_name() + '.*PAN[.]shp',
                    '{0}_L1_PAN.shp'.format(self.classified_object_name())
                ),
                self.Name_ID: 'shp_shp',
                self.Name_Title: '矢量文件shp',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn,
                self.Name_Format: self.DataFormat_Vector_File
            },
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    '(?i)' + self.classified_object_name() + '.*PAN[.]prj',
                    '{0}_L1_PAN.prj'.format(self.classified_object_name())
                ),
                self.Name_ID: 'shp_prj',
                self.Name_Title: '矢量文件prj',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    '(?i)' + self.classified_object_name() + '.*PAN[.]shx',
                    '{0}_L1_PAN.shx'.format(self.classified_object_name())
                ),
                self.Name_ID: 'shp_shx',
                self.Name_Title: '矢量文件shx',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/MetaData/ProductInfo/StartTime',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/MetaData/ProductInfo/StartTime',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/MetaData/ProductInfo/EndTime',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)'+self.classified_object_name()+'.*MSS.jpg',
                    '{0}_L1_MSS.jpg'.format(self.classified_object_name())
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)'+self.classified_object_name()+'.*MSS_thumb.jpg',
                    '{0}_L1_thumb.jpg'.format(self.classified_object_name())
                )
            }
        ]

    def get_metadata_bus_configuration_list(self) -> list:
        """
        固定的列表，重写时不可缺项
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # 卫星，必填，从元数据组织定义，必须是标准命名的卫星名称
                self.Name_XPath: '/MetaData/ProductInfo/SatelliteID'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/MetaData/ProductInfo/Sensor'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/MetaData/ProductInfo/CenterLatitude'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/MetaData/ProductInfo/CenterLongitude'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/MetaData/ProductInfo/UpperLeftLatitude'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/MetaData/ProductInfo/UpperLeftLongitude'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/MetaData/ProductInfo/UpperRightLatitude'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/MetaData/ProductInfo/UpperRightLongitude'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/MetaData/ProductInfo/LowerRightLatitude'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/MetaData/ProductInfo/LowerRightLongitude'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/MetaData/ProductInfo/LowerLeftLatitude'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/MetaData/ProductInfo/LowerLeftLongitude'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/MetaData/ProductInfo/StartTime'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/MetaData/ProductInfo/ImageRowGSD'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/MetaData/ProductInfo/RollSatelliteAngle'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/MetaData/ProductInfo/CloudPercent'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/MetaData/ProductInfo/OrbitID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/MetaData/ProductInfo/EndTime'
            },
            {
                self.Name_ID: 'remark',  # 备注 可空
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productname',  # 产品名称，有的能从卫星元数据里面取，没有就不取
                self.Name_XPath: '/MetaData/ProductInfo/SceneID'
            },
            {
                self.Name_ID: 'producttype',  # 产品类型 必填
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_ProductType, None)
            },
            {
                self.Name_ID: 'productattribute',  # 产品属性 必填
                self.Name_XPath: '/MetaData/ProductInfo/ProductLevel'
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: '/MetaData/ProductInfo/ProductID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，放文件全路径即可
                self.Name_XPath: None,
                self.Name_Value: None
            }
        ]