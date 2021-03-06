from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_pleiades_pms(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'Pleiades_PMS'
        information[self.Plugins_Info_Type_Title] = 'Pleiades星PMS传感器'
        information[self.Plugins_Info_Group] = 'Pleiades'
        information[self.Plugins_Info_Group_Title] = 'Pleiades'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i).*(PHR|PD|pd\d{10}).*', self.TextMatchType_Regex
        else:
            return r'(?i).*(PHR|PD|pd\d{10}).*[.]tif$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i).*DIM.*_P_.*[.]XML',
                'DIM_P.xml',
                True
            )
        )

    def parser_detail_custom(self, object_name):
        match_str_1 = r'(?i).*(PHR|PD|pd\d{10}).*'
        self.add_different_name_detail_by_match(match_str_1)

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*_P.*[.]tif$',
                    '{0}_P.tif'.format(self.classified_object_name()), True
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
                    r'(?i).*PREVIEW.*_MS_.*.JPG',
                    'PREVIEW_MS.JPG', True
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*ICON.*_MS_.*.JPG',
                    'ICON_MS.JPG', True
                )
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/Dimap_Document/Dataset_Sources/Source_Identification/Strip_Source/IMAGING_DATE',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/Dimap_Document/Geometric_Data/Refined_Model/Time/Time_Range/START',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/Dimap_Document/Geometric_Data/Refined_Model/Time/Time_Range/END',
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
                self.Name_Value: 'Pleiades'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_Value: 'PMS'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Center/LAT'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Center/LON'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[1]/LAT'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[1]/LON'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[2]/LAT'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[2]/LON'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[3]/LAT'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[3]/LON'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[4]/LAT'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Content/Dataset_Extent/Vertex[4]/LON'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_Custom_Item: {
                    self.Name_Time_Date: '/Dimap_Document/Dataset_Sources/Source_Identification/Strip_Source'
                                         '/IMAGING_DATE',
                    self.Name_Time_Time: '/Dimap_Document/Dataset_Sources/Source_Identification/Strip_Source'
                                         '/IMAGING_TIME'
                }
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/Dimap_Document/Processing_Information/Product_Settings/Sampling_Settings'
                                 '/RESAMPLING_SPACING '
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: "/Dimap_Document/Geometric_Data/Use_Area/"
                                 "Located_Geometric_Values[LOCATION_TYPE='Center']/Acquisition_Angles/VIEWING_ANGLE"
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/Dimap_Document/Dataset_Content/CLOUD_COVERAGE'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/SceneMetaData/MetaData/Acquisition_ID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_XPath: '/Dimap_Document/Dataset_Identification/Legal_Constraints/COPYRIGHT'
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/Dimap_Document/Dataset_Sources/Source_Identification/Strip_Source/IMAGING_DATE'
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
                self.Name_Value: 'L1'
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: '/Dimap_Document/Product_Information/Delivery_Identification/JOB_ID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，配置正则
                self.Name_Value: '(?i).*DIM.*_MS_.*[.]XML'
            }
        ]
