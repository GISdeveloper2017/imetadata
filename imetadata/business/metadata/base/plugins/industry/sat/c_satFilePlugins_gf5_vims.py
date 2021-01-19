import re

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf5 import CSatFilePlugins_gf5


class CSatFilePlugins_gf5_vims(CSatFilePlugins_gf5):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF5_VIMS'
        information[self.Plugins_Info_Type_Title] = '高分五号VIMS传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^GF5.*VIMS.*_.*', self.TextMatchType_Regex
        else:
            # 散列文件的识别方式后续有待开发，目前暂不测试
            # GF5_VIMS_N29.3_E112.4_20190321_010277_L10000129147_20mOGP.tiff
            return r'(?i)^GF5.*VIMS.*_20mOGP[.]tiff$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file('GF5.*.(xml|XML)',
                                         '{0}.xml'.format(self.classified_object_name()))
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF5.*VIMS.*_20mOGP.tiff',
                                                                 '{0}_20mOGP.tiff'.format(
                                                                     self.classified_object_name())),
                self.Name_ID: 'tiff',
                self.Name_Title: '影像文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            },
            {
                self.Name_FileName: '{0}.shp'.format(self.classified_object_name()),
                self.Name_ID: 'shp_shp',
                self.Name_Title: '矢量文件shp',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn,
                self.Name_Format: self.DataFormat_Vector_File
            },
            {
                self.Name_FileName: '{0}.dbf'.format(self.classified_object_name()),
                self.Name_ID: 'shp_dbf',
                self.Name_Title: '矢量文件dbf',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_FileName: '{0}.shx'.format(self.classified_object_name()),
                self.Name_ID: 'shp_shx',
                self.Name_Title: '矢量文件shx',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_FileName: '{0}.prj'.format(self.classified_object_name()),
                self.Name_ID: 'shp_prj',
                self.Name_Title: '矢量文件prj',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,  # .*Browse.jpg
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF5.VIMS.*.jpg',
                                                                 '{0}.jpg'.format(
                                                                     self.classified_object_name()))
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF5.VIMS.*.jpg',
                                                                 '{0}.jpg'.format(self.classified_object_name()))
            }
        ]

    def parser_detail_custom(self, object_name):
        match_str = '(?i)GF5.*VIMS.*[.].*'
        self.add_different_name_detail_by_match(match_str)

    def process_custom(self, metadata_bus_dict, metadata_bus_xml):
        """
        对部分需要进行运算的数据进行处理
        """
        super().process_custom(metadata_bus_dict, metadata_bus_xml)
        try:
            resolution = CUtils.dict_value_by_name(metadata_bus_dict, 'resolution', None)
            resolution_list = re.split(r'[,]|\s+', resolution.strip())
            if len(resolution_list) > 0:
                metadata_bus_dict['resolution'] = min(resolution_list)
        except:
            pass
