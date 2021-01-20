from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_zy3 import CSatFilePlugins_zy3


class CSatFilePlugins_zy3_zy3_01a(CSatFilePlugins_zy3):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'ZY3_FWD'
        information[self.Plugins_Info_Type_Title] = '资源一号01星FWD传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^ZY3_0(1|2)a.*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^ZY3_0(1|2)a.*_.*[.]tiff$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file('.*ZY3_0(1|2)a.*-meta.*.xml', '{0}-meta.xml'.format(self.classified_object_name())
                                         )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)^ZY3_0(1|2)a.*_.*[.]tiff$',
                                                                 '{0}.tiff'.format(self.classified_object_name())),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '全色文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file('.*ZY3_0(1|2)a.*_pre.jpg',
                                                                 '{0}_pre.jpg'.format(
                                                                     self.file_info.file_main_name)
                                                                 )
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file('.*ZY3_0(1|2)a.*_ico.jpg',
                                                                 '{0}_ico.jpg'.format(
                                                                     self.file_info.file_main_name))
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
                self.Name_XPath: '/root/data/satelliteId'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/root/data/sensorId'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/root/data/sceneCenterLat'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/root/data/sceneCenterLong'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/root/data/dataUpperLeftLat'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/root/data/dataUpperLeftLong'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/root/data/dataUpperRightLat'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/root/data/dataUpperRightLong'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/root/data/dataLowerRightLat'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/root/data/dataLowerRightLong'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/root/data/dataLowerLeftLat'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/root/data/dataLowerLeftLong'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/root/data/sceneDate'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/root/data/ImageGSD'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/root/data/RollViewingAngle'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '/root/data/cloudAmount'
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
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
                self.Name_XPath: '/root/data/productDate'
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
                self.Name_XPath: None
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
                self.Name_XPath: '/root/data/sceneDate',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/root/data/imagingStartTime',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/root/data/imagingStopTime',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]