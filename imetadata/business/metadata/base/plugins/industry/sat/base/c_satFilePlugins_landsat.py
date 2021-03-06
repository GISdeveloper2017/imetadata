from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerSat_LandSat import \
    CMDTransformerSat_LandSat
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_landsat(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'LandSat'
        information[self.Plugins_Info_Type_Title] = 'LandSat'
        information[self.Plugins_Info_Group] = 'LandSat'
        information[self.Plugins_Info_Group_Title] = 'LandSat'
        information[self.Plugins_Info_CopyRight] = 'NASA'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^(LS8_C_|LC8|LC08).*_.*|(?i)^LE(07|7).*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^(LS8_C_|LC8|LC08).*[.]tif$|(?i)^LE(07|7).*[.]tif$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                r'(?i).*_MTL[.]txt',
                '{0}_MTL.txt'.format(self.classified_object_name())
            )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)^(LS8_C_|LC8|LC08).*[.]tif$|(?i)^LE(07|7).*[.]tif$',
                    '{0}.tif'.format(self.classified_object_name())
                ),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '????????????',
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
                    r'(?i).*BQA.TIF',
                    '{0}BQA.TIF'.format(self.classified_object_name())
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*BQA.TIF',
                    '{0}BQA.TIF'.format(self.classified_object_name())
                )
            }
        ]

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        ??????xml????????????????????????, ?????????parser???metadata?????????
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            return CResult.merge_result(
                self.Failure,
                '??????{0}???????????????????????????????????????????????????????????????????????????!'.format(self.file_info.file_main_name)
            )

        transformer = CMDTransformerSat_LandSat(
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
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="DATE_ACQUIRED"]',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="DATE_ACQUIRED"]',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="DATE_ACQUIRED"]',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def get_metadata_bus_configuration_list(self) -> list:
        """
        ???????????????????????????????????????
        """
        return [
            {
                self.Name_ID: 'satelliteid',  # ?????????????????????????????????????????????????????????????????????????????????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="SPACECRAFT_ID"]'
            },
            {
                self.Name_ID: 'sensorid',  # ????????? ??????,??????????????????????????????????????????????????????????????????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="SENSOR_ID"]'
            },
            {
                self.Name_ID: 'centerlatitude',  # ????????????
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'centerlongitude',  # ????????????
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'topleftlatitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_UL_LAT_PRODUCT"]'
            },
            {
                self.Name_ID: 'topleftlongitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_UL_LON_PRODUCT"]'
            },
            {
                self.Name_ID: 'toprightlatitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_UR_LAT_PRODUCT"]'
            },
            {
                self.Name_ID: 'toprightlongitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_UR_LON_PRODUCT"]'
            },
            {
                self.Name_ID: 'bottomrightlatitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_LL_LAT_PRODUCT"]'
            },
            {
                self.Name_ID: 'bottomrightlongitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_LL_LON_PRODUCT"]'
            },
            {
                self.Name_ID: 'bottomleftlatitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_LR_LAT_PRODUCT"]'
            },
            {
                self.Name_ID: 'bottomleftlongitude',  # ??????????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="CORNER_LR_LON_PRODUCT"]'
            },
            {
                self.Name_ID: 'transformimg',  # ?????????,??????,????????????
                self.Name_Value: None
            },
            {
                self.Name_ID: 'centertime',  # ?????????????????? ??????
                self.Name_Custom_Item: {
                    self.Name_Time_Date: '//item[@name="PRODUCT_METADATA"]//item[@name="DATE_ACQUIRED"]',
                    self.Name_Time_Time: '//item[@name="PRODUCT_METADATA"]//item[@name="SCENE_CENTER_TIME"]'
                }
            },
            {
                self.Name_ID: 'resolution',  # ?????????(???) ??????????????????????????????info??????
                self.Name_XPath: '//item[@name="PROJECTION_PARAMETERS"]//item[@name="GRID_CELL_SIZE_PANCHROMATIC"]'
            },
            {
                self.Name_ID: 'rollangle',  # ?????????
                self.Name_XPath: '//item[@name="IMAGE_ATTRIBUTES"]//item[@name="ROLL_ANGLE"]'
            },
            {
                self.Name_ID: 'cloudpercent',  # ??????
                self.Name_XPath: '//item[@name="IMAGE_ATTRIBUTES"]//item[@name="CLOUD_COVER"]'
            },
            {
                self.Name_ID: 'dataum',  # ????????? ?????????null
                self.Name_Value: 'WGS_1984'
            },
            {
                self.Name_ID: 'acquisition_id',  # ?????????
                self.Name_Value: None
            },
            {
                self.Name_ID: 'copyright',  # ???????????? ???info???
                self.Name_XPath: '//item[@name="METADATA_FILE_INFO"]//item[@name="ORIGIN"]'
            },
            {
                self.Name_ID: 'publishdate',  # ???????????? ??????
                self.Name_XPath: '//item[@name="METADATA_FILE_INFO"]//item[@name="FILE_DATE"]'
            },
            {
                self.Name_ID: 'remark',  # ?????? ??????
                self.Name_Value: None
            },
            {
                self.Name_ID: 'productname',  # ?????????????????????????????????????????????????????????????????????
                self.Name_XPath: None
            },
            {
                self.Name_ID: 'producttype',  # ???????????? ??????
                self.Name_Value: CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_ProductType, None)
            },
            {
                self.Name_ID: 'productattribute',  # ???????????? ??????
                self.Name_XPath: '//item[@name="PRODUCT_METADATA"]//item[@name="DATA_TYPE"]'
            },
            {
                self.Name_ID: 'productid',  # ??????id ????????????????????????
                self.Name_XPath: '//item[@name="METADATA_FILE_INFO"]//item[@name="LANDSAT_SCENE_ID"]'
            },
            {
                self.Name_ID: 'otherxml',  # ????????????????????????????????????
                self.Name_Value: None
            }
        ]

    def metadata_bus_dict_process_custom(self, metadata_bus_dict):
        """
        ????????????????????????????????????????????????
        """
        super().metadata_bus_dict_process_custom(metadata_bus_dict)
        productattribute = CUtils.dict_value_by_name(metadata_bus_dict, 'productattribute', None)
        if not CUtils.equal_ignore_case(productattribute, ''):
            if len(productattribute) > 2:
                metadata_bus_dict['productattribute'] = productattribute[:2]
