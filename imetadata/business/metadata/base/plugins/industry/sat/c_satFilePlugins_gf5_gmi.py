import re
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf5 import CSatFilePlugins_gf5
from imetadata.database.c_factory import CFactory


class CSatFilePlugins_gf5_gmi(CSatFilePlugins_gf5):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF5_GMI'
        information[self.Plugins_Info_Type_Title] = '高分五号GMI传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^GF5.*GMI.*_.*', self.TextMatchType_Regex
        else:
            # 散列文件的识别方式后续有待开发，目前暂不测试
            return r'(?i)^GF5.*GMI.*[.]h5$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file('GF5.*.(xml|XML)',
                                         '{0}.xml'.format(self.classified_object_name()))
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                # 主文件质检有待调整
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF5.*GMI.*[.]h5',
                                                                 '{0}.h5'.format(self.classified_object_name())),
                self.Name_ID: 'h5',
                self.Name_Title: 'h5文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

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
                self.Name_XPath: '/ProductMetaData/SatelliteID'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/ProductMetaData/SensorID'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/ProductMetaData/CenterLat'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/ProductMetaData/CenterLong'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/ProductMetaData/TopLeftLatitude'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/ProductMetaData/TopLeftLongitude'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/ProductMetaData/TopRightLatitude'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/ProductMetaData/TopRightLongitude'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/ProductMetaData/BottomRightLatitude'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/ProductMetaData/BottomRightLongitude'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/ProductMetaData/BottomLeftLatitude'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/ProductMetaData/BottomLeftLongitude'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/ProductMetaData/EndTime'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_Value: 0
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_Value: 0
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_Value: 0
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/ProductMetaData/POrbitID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/ProductMetaData/ProduceTime',
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
                self.Name_XPath: '/ProductMetaData/ProductLevel',
                self.Name_Map: {  # 映射，当取到的值为key时，将值转换为value
                    'LEVEL1A': 'L1',
                    'LEVEL2A': 'L2',
                    'LEVEL4A': 'L4',
                    'LEVEL1': 'L1'
                    # self.Name_Default: None # 没有对应的的映射使用默认值
                }
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: '/ProductMetaData/ProductID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，放文件全路径即可
                self.Name_XPath: None,
                self.Name_Value: None
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                # 按照xsl文件配置，测试数据中没有.jpg
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF5.GMI.*.jpg',
                                                                 '{0}.jpg'.format(
                                                                     self.classified_object_name()))
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF5.GMI.*.jpg',
                                                                 '{0}.jpg'.format(self.classified_object_name()))
            }
        ]

    def parser_detail_custom(self, object_name):
        match_str = '(?i){0}.*[.].*'.format(self.classified_object_name())
        self.add_different_name_detail_by_match(match_str)

    def process_custom(self, metadata_bus_dict, metadata_bus_xml):
        """
        对部分需要进行运算的数据进行处理
        """
        super().process_custom(metadata_bus_dict, metadata_bus_xml)
        centerlatitude = CUtils.dict_value_by_name(metadata_bus_dict, 'centerlatitude', None)
        centerlongitude = CUtils.dict_value_by_name(metadata_bus_dict, 'centerlongitude', None)
        if (not CUtils.equal_ignore_case(centerlatitude, '')) and (not CUtils.equal_ignore_case(centerlongitude, '')):
            try:
                db_id = self.file_info.db_server_id
                if CUtils.equal_ignore_case(db_id, ''):
                    db_id = self.DB_Server_ID_Distribution
                db = CFactory().give_me_db(db_id)
                wkt = db.one_row(
                    '''
                    select st_astext(st_envelope(st_geomfromewkt(st_astext(st_buffer(st_geographyfromtext(
                    'POINT({0} {1})'), 5000))))) as wkt
                    '''.format(centerlatitude, centerlongitude)).value_by_name(0, 'wkt', None)
                wkt = wkt.replace('POLYGON((', '').replace('))', '').strip()
                coordinates_list = re.split(r'[,]|\s+', wkt)
                metadata_bus_dict['bottomleftlatitude'] = coordinates_list[0]
                metadata_bus_dict['bottomleftlongitude'] = coordinates_list[1]
                metadata_bus_dict['topleftlatitude'] = coordinates_list[2]
                metadata_bus_dict['topleftlongitude'] = coordinates_list[3]
                metadata_bus_dict['toprightlatitude'] = coordinates_list[4]
                metadata_bus_dict['toprightlongitude'] = coordinates_list[5]
                metadata_bus_dict['bottomrightlatitude'] = coordinates_list[6]
                metadata_bus_dict['bottomrightlongitude'] = coordinates_list[7]
            except:
                pass
