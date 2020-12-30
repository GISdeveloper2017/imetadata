# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:24 
# @Author : 王西亚 
# @File : c_satPlugins.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_time import CTime
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.content.c_virtualContent_Dir import CVirtualContentDir
from imetadata.business.metadata.base.content.c_virtualContent_Package import CVirtualContentPackage
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerCommon import CMDTransformerCommon
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CSatPlugins(CPlugins):
    """
    卫星数据插件
    . 如果卫星数据是文件, 则先检查文件名是否在指定的列表中, 之后再检查文件主名是否匹配指定特征串
    . 如果卫星数据是目录, 则直接检查目录是否匹配指定特征串
    """
    Sat_Object_Status_Zip = 'zip'
    Sat_Object_Status_Dir = 'dir'
    Sat_Object_Status_File = 'file'
    Sat_Object_Status_Unknown = 'unknown'

    def __init__(self, file_info: CDMFilePathInfoEx):
        super().__init__(file_info)
        self.__object_status__ = self.Sat_Object_Status_Unknown

    @property
    def object_status(self):
        return self.__object_status__

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '未知卫星'
        # information[self.Plugins_Info_Name] = 'UnknownSat'
        information[self.Plugins_Info_Type_Code] = None  # '000001'
        information[self.Plugins_Info_Group] = None  # self.DataGroup_Sat_raster
        information[
            self.Plugins_Info_Group_Title] = None  # self.data_group_title(information[self.Plugins_Info_Group_Name])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Sat  # '卫星数据'
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = self.Engine_Custom
        information[self.Plugins_Info_DetailEngine] = self.get_runtime_detail_engine()

        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_satellite_all'
        return information

    def create_file_content(self):
        if self.__object_status__ == self.Sat_Object_Status_Dir:
            self._file_content = CVirtualContentDir(self.file_info.file_name_with_full_path)
        elif self.__object_status__ == self.Sat_Object_Status_Zip:
            self._file_content = CVirtualContentPackage(self.file_info.file_name_with_full_path)
        else:
            self._file_content = CVirtualContentDir(self.file_info.file_path)

    def special_zip_file_ext_list(self) -> list:
        """
        设定卫星数据压缩包的扩展名
        :return:
        """
        return ['tar.gz', 'rar', 'zip', '7z', 'tar', 'tgz']

    def special_file_ext_list(self) -> list:
        """
        设定卫星数据实体的扩展名
        :return:
        """
        return ['tiff', 'tif']

    def classified(self):
        self.__object_status__ = self.Sat_Object_Status_Unknown
        self._object_name = None
        self._object_confirm = self.Object_Confirm_IUnKnown

        if self.file_info.file_type == self.FileType_File:
            if self.special_zip_file_ext_list().count(self.file_info.file_ext.lower()) > 0:
                sat_classified_character, sat_classified_character_type = self.get_classified_character_of_sat(
                    self.Sat_Object_Status_Zip)
                if (self.classified_with_character(self.file_info.file_main_name, sat_classified_character,
                                                   sat_classified_character_type)):
                    self.__object_status__ = self.Sat_Object_Status_Zip
                    self._object_confirm = self.Object_Confirm_IKnown
                    self._object_name = self.file_info.file_main_name
            else:
                sat_classified_character, sat_classified_character_type = self.get_classified_character_of_sat(
                    self.Sat_Object_Status_File)
                if (self.classified_with_character(self.file_info.file_name_without_path, sat_classified_character,
                                                   sat_classified_character_type)):
                    self.__object_status__ = self.Sat_Object_Status_File
                    self._object_confirm = self.Object_Confirm_IKnown
                    self._object_name = self.get_classified_object_name_of_sat(self.Sat_Object_Status_File)
        elif self.file_info.file_type == self.FileType_Dir:
            sat_classified_character, sat_classified_character_type = self.get_classified_character_of_sat(
                self.Sat_Object_Status_Dir)
            if (self.classified_with_character(self.file_info.file_name_without_path, sat_classified_character,
                                               sat_classified_character_type)):
                self.__object_status__ = self.Sat_Object_Status_Dir
                self._object_confirm = self.Object_Confirm_IKnown
                self._object_name = self.file_info.file_name_without_path

        return self._object_confirm, self._object_name

    def classified_with_character(self, text, sat_classified_character, sat_classified_character_type) -> bool:
        """
        根据给定的特征和类型, 对指定的文本进行检查
        :param text:
        :param sat_classified_character:
        :param sat_classified_character_type:
        :return: 是否匹配
        """
        if sat_classified_character_type == self.TextMatchType_Common:
            return CFile.file_match(text.lower(), sat_classified_character)
        elif sat_classified_character_type == self.TextMatchType_Regex:
            return CUtils.text_match_re(text.lower(), sat_classified_character)
        else:
            return False

    @abstractmethod
    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        . 如果是散落文件, 则是针对文件的全名
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
        return '', self.TextMatchType_Common

    @abstractmethod
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
        return self.file_info.file_main_name

    @abstractmethod
    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return self.file_info.file_main_name

    def get_runtime_detail_engine(self):
        """
        返回运行时的详情引擎
        :return:
        """
        if self.__object_status__ == self.Sat_Object_Status_Zip:
            return None
        elif self.__object_status__ == self.Sat_Object_Status_Dir:
            return self.DetailEngine_All_File_Of_Dir
        elif self.__object_status__ == self.Sat_Object_Status_File:
            return self.DetailEngine_Same_File_Main_Name
        else:
            return None

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
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

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        self.metadata_bus_transformer_type = self.Transformer_XML
        self.metadata_bus_src_filename_with_path = self.get_metadata_bus_filename_by_file()
        if not CFile.file_or_path_exist(self.metadata_bus_src_filename_with_path):
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'metadata_file_bus',
                    self.Name_Title: '业务元数据文件',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: self.metadata_bus_src_filename_with_path,
                    self.Name_ID: 'metadata_file_bus',
                    self.Name_Title: '业务元数据文件',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '业务元数据[{0}]存在'.format(self.metadata_bus_src_filename_with_path)
                }
            )

    def parser_metadata_spatial_after_qa(self, parser: CMetaDataParser):
        """
        继承本方法, 对详细的空间元数据信息进行处理
        :param parser:
        :return:
        """
        parser.metadata.metadata_spatial_obj().native_geom = parser.metadata.metadata_spatial_obj().native_box
        parser.metadata.metadata_spatial_obj().wgs84_bbox = parser.metadata.metadata_spatial_obj().native_box
        parser.metadata.metadata_spatial_obj().wgs84_geom = parser.metadata.metadata_spatial_obj().native_geom
        parser.metadata.metadata_spatial_obj().wgs84_center = parser.metadata.metadata_spatial_obj().native_center

        parser.metadata.metadata_spatial_obj().prj_wkt = '''
        GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433],
        AUTHORITY["EPSG","4326"]]
        '''
        parser.metadata.metadata_spatial_obj().prj_proj4 = '+proj=longlat +datum=WGS84 +no_defs'
        parser.metadata.metadata_spatial_obj().prj_project = None
        parser.metadata.metadata_spatial_obj().prj_coordinate = 'WGS 84'
        parser.metadata.metadata_spatial_obj().prj_degree = None
        parser.metadata.metadata_spatial_obj().prj_zone = None
        parser.metadata.metadata_spatial_obj().prj_source = self.Prj_Source_BusMetaData

        return super().parser_metadata_spatial_after_qa(parser)

    def parser_metadata_view_after_qa(self, parser: CMetaDataParser):
        """
        继承本方法, 对详细的可视元数据信息进行处理
        1. 提取元数据中的时间
        1. 根据时间及其他信息, 生成元数据的目录, 默认为:
            <卫星英文名称>/<传感器英文名称>/<四位年份>/<两位月份>/<对象名称>/<对象标识>
            注意: 后续在考虑自定义
        1.
        :param parser:
        :return:
        """
        data_date_time = parser.metadata.time_information.xpath_one(self.Name_Time, CTime.format_str(CTime.today()))
        data_date = CTime.from_datetime_str(data_date_time, CTime.today())
        data_year = CTime.format_str(data_date, '%Y')
        data_month = CTime.format_str(data_date, '%m')

        data_view_sub_path = CFile.join_file(
            CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Catalog, ''),
            CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Group, '')
        )
        data_view_sub_path = CFile.join_file(
            data_view_sub_path,
            CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Type, '')
        )
        data_view_sub_path = CFile.join_file(data_view_sub_path, data_year)
        data_view_sub_path = CFile.join_file(data_view_sub_path, data_month)
        data_view_sub_path = CFile.join_file(data_view_sub_path, self.classified_object_name())
        data_view_sub_path = CFile.join_file(data_view_sub_path, self.file_info.my_id)

        data_view_path = CFile.join_file(self.file_content.view_root_dir, data_view_sub_path)

        metadata_file_copy_list = self.parser_metadata_file_copy_list(parser)
        if len(metadata_file_copy_list) > 0:
            for metadata_file_copy_item in metadata_file_copy_list:
                CFile.copy_file_to(
                    CFile.join_file(
                        self.file_content.content_root_dir,
                        metadata_file_copy_item
                    ), data_view_path)

        self.parser_metadata_file_copy_custom(parser, data_view_path)

        metadata_view_list = self.parser_metadata_view_list(parser)
        if len(metadata_view_list) > 0:
            for metadata_view_item in metadata_view_list:
                parser.metadata.set_metadata_view(
                    self.DB_True,
                    '文件[{0}]的预览图成功加载! '.format(self.file_info.file_name_with_full_path),
                    CUtils.dict_value_by_name(metadata_view_item, self.Name_ID, self.View_MetaData_Type_Browse),
                    CFile.join_file(
                        data_view_sub_path,
                        CUtils.dict_value_by_name(metadata_view_item, self.Name_FileName, '')
                    )
                )

        self.parser_metadata_view_custom(parser, data_view_sub_path)

        return CResult.merge_result(
            self.Success,
            '数据文件[{0}]的可视化信息解析成功! '.format(self.file_info.file_name_with_full_path)
        )

    def parser_metadata_file_copy_list(self, parser: CMetaDataParser) -> list:
        """
        标准的文件拷贝列表
        系统将把您指定的数据中的部分文件, 直接拷贝到元数据目录下
        注意: 指定数据时, 无需指定目录, 仅仅指定数据目录下的文件即可
        示例:
        return [
            '{0}-PAN1_thumb.jpg'.format(self.classified_object_name()),
            '{0}-PAN1.jpg'.format(self.classified_object_name()),
            'cloud/other.txt'
        ]
        :param parser:
        :return:
        """
        return []

    def parser_metadata_file_copy_custom(self, parser: CMetaDataParser, target_path: str):
        """
        完全自定义的拷贝

        注意: 本方法禁止触发异常!!!

        :param target_path: 元数据拷贝的目标路径
        :param parser:
        :return:
        """
        pass

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        示例:
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: '/ProductMetaData/CenterTime'
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: '/ProductMetaData/StartTime'
            }
        ]
        :param parser:
        :return:
        """
        return []

    def parser_metadata_view_custom(self, parser: CMetaDataParser, target_sub_path: str):
        """
        完全自定义的设置快视图, 拇指图的信息的方法
        在标准模式无法解决问题时使用
        提供的相对路径, 是为了向数据库中放置快视图或拇指图的路径时使用. 由于数据库中登记的图片路径, 是用于第三方系统(比如查询检索系统), 它已经将
            数管系统的快视图的根目录注册到它的系统里, 使用快视图或拇指图时, 需要使用相对路径, 因此, 这里仅仅提供相对路径, 便于处理

        注意: 提供的路径为相对路径, 如需要自行处理快视图或拇指图存储到路径下, 需要按如下方式计算完整路径:
            CFile.join_file(self.file_content.view_root_dir, data_view_sub_path)

        注意: 本方法禁止触发异常!!!

        :param parser:
        :param target_sub_path: 相对路径
        :return:
        """
        pass

    def get_metadata_bus_configuration_list(self) -> list:
        """
        固定的列表，重写时不可缺项
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # 卫星，必填，从元数据组织定义，必须是标准命名的卫星名称
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: None,
                self.Name_Value: 0
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: None,
                self.Name_Value: 0
            },
            {
                self.Name_ID: 'dataum',  # 坐标系 默认为null
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'acquisition_id',  # 轨道号
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'copyright',  # 发布来源 从info取
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'publishdate',  # 发布时间 必填
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'remark',  # 备注 可空
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'producttype',  # 产品类型
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productattribute',  # 产品属性
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'starttime',  # 开始时间
                self.Name_XPath: None,
                self.Name_Value: None
            },
            {
                self.Name_ID: 'endtime',  # 结束时间
                self.Name_XPath: None,
                self.Name_Value: None
            }
        ]

    def metadata_bus_xml_to_dict(self, metadata_bus_xml: CXml) -> dict:
        metadata_bus_dict = super().metadata_bus_xml_to_dict(metadata_bus_xml)
        for metadata_bus_configuration in self.get_metadata_bus_configuration_list():
            metadata_bus_id = CUtils.dict_value_by_name(metadata_bus_configuration, self.Name_ID, 'None')
            metadata_bus_xpath = CUtils.dict_value_by_name(metadata_bus_configuration, self.Name_XPath, None)
            metadata_bus_value = CUtils.dict_value_by_name(metadata_bus_configuration, self.Name_Value, None)
            if metadata_bus_xpath is not None:
                metadata_bus_dict[metadata_bus_id] = \
                    metadata_bus_xml.get_element_text_by_xpath_one(metadata_bus_xpath)
            elif metadata_bus_value is not None:
                metadata_bus_dict[metadata_bus_id] = metadata_bus_value
            else:
                metadata_bus_dict[metadata_bus_id] = None
        return metadata_bus_dict

    def qa_sat_metadata_bus_list(self) -> list:
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'satelliteid',
                self.Name_Title: '卫星名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'sensorid',
                self.Name_Title: '传感器名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'centerlatitude',
                self.Name_Title: '中心维度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'centerlongitude',
                self.Name_Title: '中心经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'topleftlatitude',
                self.Name_Title: '左上角维度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'topleftlongitude',
                self.Name_Title: '左上角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'toprightlatitude',
                self.Name_Title: '右上角维度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'toprightlongitude',
                self.Name_Title: '右上角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'bottomrightlatitude',
                self.Name_Title: '右下角维度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'bottomrightlongitude',
                self.Name_Title: '右下角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'bottomleftlatitude',
                self.Name_Title: '左下角维度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'bottomleftlongitude',
                self.Name_Title: '左下角经度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'centertime',
                self.Name_Title: '影像获取时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_or_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'rollangle',
                self.Name_Title: '侧摆角',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'cloudpercent',
                self.Name_Title: '云量',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'publishdate',
                self.Name_Title: '发布时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_or_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'acquisition_id',
                self.Name_Title: '轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn,
                self.Name_NotNull: True
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'starttime',
                self.Name_Title: '开始时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_or_datetime
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_ID: 'endtime',
                self.Name_Title: '结束时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date_or_datetime
            }
        ]

    def qa_metadata_custom(self, parser: CMetaDataParser):
        """
        自定义的质检方法, 发生在元数据解析之后
        :param parser:
        :return:
        """
        metadata_bus_xml = parser.metadata.metadata_bus_xml()
        metadata_bus_dict = self.metadata_bus_xml_to_dict(metadata_bus_xml)
        parser.batch_qa_metadata_bus_dict(metadata_bus_dict, self.qa_sat_metadata_bus_list())

        # 把元数据copy到拇指图文件夹下
