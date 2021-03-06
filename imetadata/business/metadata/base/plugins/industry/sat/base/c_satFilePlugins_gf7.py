from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_gf7(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF7'
        information[self.Plugins_Info_Type_Title] = '高分七号'
        information[self.Plugins_Info_Group] = 'GF7'
        information[self.Plugins_Info_Group_Title] = '高分七号'
        information[self.Plugins_Info_CopyRight] = '高分中心'
        return information

    def get_metadata_bus_configuration_list(self) -> list:
        """
        固定的列表，重写时不可缺项
        self.Name_ID：字段的名称 例：self.Name_ID: 'satelliteid'
        self.Name_XPath：需要从xml中取值时的xpath 例：self.Name_XPath: '/ProductMetaData/SatelliteID'
        self.Name_Other_XPath：当有多个xpath时的配置 ,注意值为list
        例：self.Name_Other_XPath: ['/ProductMetaData/ImageGSDLine','/ProductMetaData/ImageGSD']
        self.Name_Value：不在xml取得默认值与当XPath取不到值时取的值 例 self.Name_Value: 1
        self.Name_Map：映射，当取到的值为key的值时将值转换为value
        例 self.Name_Map: {  # 映射，当取到的值为key时，将值转换为value
                                    'LEVEL1A': 'L1',
                                    'LEVEL2A': 'L2',
                                    'LEVEL4A': 'L4'
                                    # self.Name_Default: None # 没有对应的的映射使用的默认值}
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # 卫星，必填，从元数据组织定义，必须是标准命名的卫星名称
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/SatelliteID'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/SensorID'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/CenterPoint/Latitude'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/CenterPoint/Longtitude'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/LeftTopPoint/Latitude'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/LeftTopPoint/Longtitude'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/RightTopPoint/Latitude'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/RightTopPoint/Longtitude'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/RightBottomPoint/Latitude'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/RightBottomPoint/Longtitude'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/LeftBottomPoint/Latitude'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ProductGeographicRange/LeftBottomPoint/Longtitude'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/AcquisitionTime'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/ImageGSD/Line'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/sensor_corrected_metadata/sensor_corrected_metadata/productInfo/RollViewingAngle'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/CloudPercent'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/OrbitID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/TimeStamp/CenterTime',
            },
            {
                self.Name_ID: 'remark',  # 备注 可空
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productname',  # 产品名称，有的能从卫星元数据里面取，没有就不取
                self.Name_Value: None
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
                self.Name_XPath: '/sensor_corrected_metadata/processInfo/ProduceID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，配置正则
                self.Name_Value: None
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
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/AcquisitionTime',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/TimeStamp/StartTime',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/sensor_corrected_metadata/productInfo/TimeStamp/EndTime',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def parser_detail_custom(self, object_name):
        match_str = '(?i){0}.*[.].*'.format(object_name[:])
        self.add_different_name_detail_by_match(match_str)
