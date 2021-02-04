from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_kompsat3(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'KOMPSAT3_PMS'
        information[self.Plugins_Info_Type_Title] = 'Kompsat-3星PMS传感器'
        information[self.Plugins_Info_Group] = 'KOMPSAT3'
        information[self.Plugins_Info_Group_Title] = 'Kompsat-3'
        information[self.Plugins_Info_CopyRight] = 'KARI'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^K3_.*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^K3_.*_.*[.]tif$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i)^K3_.*_Aux[.]xml',
                '{0}_Aux.xml'.format(self.classified_object_name().replace('_Bundle', '', 1))
            )
        )

    def parser_detail_custom(self, object_name):
        match_str_1 = '(?i)' + object_name.replace('_Bundle', '', 1) + '.*[.].*'
        self.add_different_name_detail_by_match(match_str_1)

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)^K3_.*_.*[.]tif$',
                    '{0}_B.tif'.format(self.classified_object_name().replace('_Bundle', '', 1))
                ),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '影像文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingTime/ImagingCenterTime/UTC',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingTime/ImagingStartTime/UTC',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingTime/ImagingEndTime/UTC',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)K3_.*_br[.]jpg',
                    '{0}_br.jpg'.format(self.classified_object_name().replace('_Bundle', '', 1))
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)K3_.*_th[.]jpg',
                    '{0}_th.jpg'.format(self.classified_object_name().replace('_Bundle', '', 1))
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
                self.Name_XPath: '/Auxiliary/General/Satellite'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_Value: 'PMS'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogCenter/Latitude'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogCenter/Longitude'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogTL/Latitude'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogTL/Longitude'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogTR/Latitude'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogTR/Longitude'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogBR/Latitude'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogBR/Longitude'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogBL/Latitude'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingCoordinates/ImageGeogBL/Longitude'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/Auxiliary/Image/PAN/ImagingTime/ImagingCenterTime/UTC'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_Value: '0.7/1'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/Auxiliary/Image/PAN/Angle/Roll'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/Auxiliary/Image/PAN/CloudCover/Average'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_Value: None
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/Auxiliary/General/CreateDate'
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
                self.Name_XPath: '/Auxiliary/General/ProductLevel',
                self.Name_Map: {  # 映射，当取到的值为key时，将值转换为value
                    'Level1R': 'L1',
                    'Level2R': 'L2',
                    'Level4R': 'L4'
                }
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

    def metadata_bus_dict_process_custom(self, metadata_bus_dict):
        super().metadata_bus_dict_process_custom(metadata_bus_dict)
        centertime = CUtils.dict_value_by_name(metadata_bus_dict, 'centertime', None)
        publishdate = CUtils.dict_value_by_name(metadata_bus_dict, 'publishdate', None)
        if not CUtils.equal_ignore_case(centertime, ''):
            centertime = centertime[0:8] + ' ' + centertime[8:]
            metadata_bus_dict['centertime'] = centertime
        if not CUtils.equal_ignore_case(publishdate, ''):
            publishdate = publishdate[0:8] + ' ' + publishdate[8:]
            metadata_bus_dict['publishdate'] = publishdate
