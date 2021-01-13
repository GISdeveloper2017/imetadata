# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 17:35 
# @Author : 王西亚 
# @File : c_satFilePlugins_gf1_pms_and_wfv.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_satPlugins import CSatPlugins


class CSatFilePlugins_gf3(CSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF3_SAR'
        information[self.Plugins_Info_Type_Title] = '高分三号SAR传感器'
        information[self.Plugins_Info_Group] = 'GF3'
        information[self.Plugins_Info_Group_Title] = '高分三号'
        information[self.Plugins_Info_CopyRight] = '高分中心'
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

        return super().get_classified_character_of_sat(sat_file_status)

    def get_classified_object_name_of_sat(self, sat_file_status) -> str:
        """
        当卫星数据是解压后的散落文件时, 如何从解压后的文件名中, 解析出卫星数据的原名
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        . 如果是散落文件, 则是针对文件的全名
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        """
        return super().get_classified_object_name_of_sat(sat_file_status)

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            '{0}.meta.xml'.format(self.classified_object_name())
        )

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
                self.Name_XPath: '/product/satellite'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '/product/sensor/imagingMode'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '/product/imageinfo/center/latitude'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '/product/imageinfo/center/longitude'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '/product/imageinfo/corner/topLeft/latitude'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '/product/imageinfo/corner/topLeft/longitude'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '/product/imageinfo/corner/topRight/latitude'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '/product/imageinfo/corner/topRight/longitude'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '/product/imageinfo/corner/bottomRight/latitude'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '/product/imageinfo/corner/bottomRight/longitude'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '/product/imageinfo/corner/bottomLeft/latitude'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '/product/imageinfo/corner/bottomLeft/longitude'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: '/product/platform/CenterTime'
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: '/product/productinfo/NominalResolution'
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '/product/platform/RollAngle'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_Value: -1
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: '/product/orbitID'
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_CopyRight, None)
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: '/product/productinfo/productGentime',
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
                self.Name_XPath: '/product/productID'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，放文件全路径即可
                self.Name_XPath: None,
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
                self.Name_ID: self.Name_Time,  # 获取时间
                self.Name_XPath: '/product/platform/CenterTime',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_Start_Time,  # 开始时间
                self.Name_XPath: '/product/sensor/satelliteTime/start',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,  # 结束时间
                self.Name_XPath: '/product/sensor/satelliteTime/end',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def parser_metadata_with_qa(self, parser: CMetaDataParser):
        """
        进行质量检验, 保证数据实体的可读性, 并处理好元数据和业务元数据, 保证后续的其他元数据解析的通畅和无误!!!
        :param parser:
        :return:
        """
        parser.batch_qa_file_list(self.init_qa_file_list(parser))
        # 自定义的文件完整性质检
        self.qa_file_custom(parser)

        # 这里将结果信息丢弃不用, 因为在提取元数据的方法中, 已经将异常信息记录到质检数据中
        result = self.init_metadata(parser)
        if CResult.result_success(result):
            if parser.metadata.metadata_type == self.MetaDataFormat_XML:
                parser.batch_qa_metadata_xml(self.init_qa_metadata_xml_list(parser))
            elif parser.metadata.metadata_type == self.MetaDataFormat_Json:
                parser.batch_qa_metadata_json_item(self.init_qa_metadata_json_list(parser))
        else:
            parser.metadata.set_metadata(
                self.DB_False, CResult.result_message(result), self.MetaDataFormat_Text, '')

        # 这里将结果信息丢弃不用, 因为在提取业务元数据的方法中, 已经将异常信息记录到质检数据中
        result = self.init_metadata_bus(parser)
        if CResult.result_success(result):
            if parser.metadata.metadata_bus_type == self.MetaDataFormat_XML:
                parser.batch_qa_metadata_bus_xml_item(self.init_qa_metadata_bus_xml_list(parser))
            elif parser.metadata.metadata_bus_type == self.MetaDataFormat_Json:
                parser.batch_qa_metadata_bus_json_item(self.init_qa_metadata_bus_json_list(parser))
        else:
            parser.metadata.set_metadata_bus(
                self.DB_False, CResult.result_message(result), self.MetaDataFormat_Text, '')
        # 自定义的元数据质检
        self.qa_metadata_custom(parser)
