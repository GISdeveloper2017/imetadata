from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf4 import CSatFilePlugins_gf4


class CSatFilePlugins_gf4_pmi(CSatFilePlugins_gf4):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF4_PMI'
        information[self.Plugins_Info_Type_Title] = '高分四号PMI传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)GF4.*PMI.*_.*', self.TextMatchType_Regex
        else:
            # GF4_PMS_E115.0_N36.6_20160803_L1A0000125813.tiff
            # 暂定 gf4_pms_*_l1a*.tiff为主对象文件
            # 散列文件的识别方式后续有待开发，目前暂不测试
            return 'gf4_pms_*_l1a*.tiff', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            '{0}.xml'.format(self.classified_object_name().replace('PMI', 'PMS'))
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: '{0}.tiff'.format(self.classified_object_name().replace('PMI', 'PMS')),
                self.Name_ID: 'pms_tif',
                self.Name_Title: '影像文件pms',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: '{0}.jpg'.format(self.classified_object_name().replace('PMI', 'PMS'))

            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: '{0}_thumb.jpg'.format(self.classified_object_name().replace('PMI', 'PMS'))
            }
        ]
