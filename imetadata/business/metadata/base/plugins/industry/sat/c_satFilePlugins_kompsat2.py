from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerSat_k2 import CMDTransformerSat_k2
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_kompsat2(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'KOMPSAT2'
        information[self.Plugins_Info_Type_Title] = 'Kompsat-2星'
        information[self.Plugins_Info_Group] = 'KOMPSAT2'
        information[self.Plugins_Info_Group_Title] = 'Kompsat-2'
        information[self.Plugins_Info_CopyRight] = '2007 KARI, All rights reserved'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^MSC_.*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^MSC_.*_.*[.]tif$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                r'(?i)^MSC.*_[0-9A-Z]{12}_\d[A-Z][.]txt',
                '{0}.txt'.format(self.classified_object_name().replace('_Bundle', '', 1))
            )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)^MSC_.*_.*[.]tif$',
                    '{0}.tif'.format(self.classified_object_name().replace('_Bundle', '', 1))
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
                    r'(?i)MSC.*_br.jpg',
                    '{0}_br.jpg'.format(self.classified_object_name().replace('_Bundle', '', 1))
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)MSC.*_tn.jpg',
                    '{0}_th.jpg'.format(self.classified_object_name().replace('_Bundle', '', 1))
                )
            }
        ]

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            return CResult.merge_result(
                self.Failure,
                '数据{0}无业务元数据文件，请检查数据业务元数据文件是否存在!'.format(self.file_info.file_main_name)
            )

        transformer = CMDTransformerSat_k2(
            parser.object_id,
            parser.object_name,
            parser.file_info,
            parser.file_content,
            parser.metadata,
            self.metadata_bus_transformer_type,
            self.metadata_bus_src_filename_with_path
        )
        return transformer.process()

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '//item[@name="AUX_STRIP_ACQ_DATE_UT"]//value',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '//item[@name="AUX_STRIP_ACQ_DATE_UT"]//value',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '//item[@name="AUX_STRIP_ACQ_DATE_UT"]//value',
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
                self.Name_XPath: '//item[@name="AUX_SATELLITE_NAME"]//value'
            },
            {
                self.Name_ID: 'sensorid',  # 传感器 必填,从元数据组织定义，必须是标准命名的传感器名称
                self.Name_XPath: '//item[@name="AUX_SATELLITE_SENSOR"]//value'
            },
            {
                self.Name_ID: 'centerlatitude',  # 中心维度
                self.Name_XPath: '//item[@name="AUX_IMAGE_CENTER_LATLONG_DEG"]//value[1]'
            },
            {
                self.Name_ID: 'centerlongitude',  # 中心经度
                self.Name_XPath: '//item[@name="AUX_IMAGE_CENTER_LATLONG_DEG"]//value[2]'
            },
            {
                self.Name_ID: 'topleftlatitude',  # 左上角维度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_TL_LATLONG_DEG"]//value[1]'
            },
            {
                self.Name_ID: 'topleftlongitude',  # 左上角经度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_TL_LATLONG_DEG"]//value[2]'
            },
            {
                self.Name_ID: 'toprightlatitude',  # 右上角维度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_TR_LATLONG_DEG"]//value[1]'
            },
            {
                self.Name_ID: 'toprightlongitude',  # 右上角经度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_TR_LATLONG_DEG"]//value[2]'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # 右下角维度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_BL_LATLONG_DEG"]//value[1]'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # 右下角经度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_BL_LATLONG_DEG"]//value[2]'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # 左下角维度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_BR_LATLONG_DEG"]//value[1]'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # 左下角经度 必填
                self.Name_XPath: '//item[@name="AUX_IMAGE_BR_LATLONG_DEG"]//value[2]'
            },
            {
                self.Name_ID: 'transformimg',  # 斜视图,可空,不用质检
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # 影像获取时间 必填
                self.Name_Custom_Item: {
                    self.Name_Time_Date: '//item[@name="AUX_STRIP_ACQ_DATE_UT"]//value',
                    self.Name_Time_Time: '//item[@name="AUX_STRIP_ACQ_CENTER_UT"]//value'
                }
            },
            {
                self.Name_ID: 'resolution',  # 分辨率(米) 对应卫星的默认值，从info里取
                self.Name_Value: 1
            },
            {
                self.Name_ID: 'rollangle',  # 侧摆角
                self.Name_XPath: '//item[@name="AUX_TILT_ANGLE_ROLL_DEG"]//value'
            },
            {
                self.Name_ID: 'cloudpercent',  # 云量
                self.Name_XPath: '//item[@name="AUX_CLOUD_STATUS"]//value'
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
                self.Name_XPath: '//item[@name="AUX_IMAGE_L1R_PROCESSED_UT"]//value'
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
                self.Name_XPath: '//item[@name="AUX_IMAGE_LEVEL"]//value'
            },
            {
                self.Name_ID: 'productid',  # 产品id 默认取主文件全名
                self.Name_XPath: '//item[@name="AUX_STRIP_ID"]//value'
            },
            {
                self.Name_ID: 'otherxml',  # 预留字段，可空，配置正则
                self.Name_Value: None
            }
        ]

    def metadata_bus_dict_process_custom(self, metadata_bus_dict):
        """
        对部分需要进行运算的数据进行处理
        """
        super().metadata_bus_dict_process_custom(metadata_bus_dict)

        productattribute = CUtils.dict_value_by_name(metadata_bus_dict, 'productattribute', None)
        metadata_bus_dict['productattribute'] = productattribute[:2]