from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf4 import CSatFilePlugins_gf4


class CSatFilePlugins_gf4_irs(CSatFilePlugins_gf4):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF4_IRS'
        information[self.Plugins_Info_Type_Title] = '高分四号IRS传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)GF4.*IRS.*_.*', self.TextMatchType_Regex
        else:
            # 散列文件的识别方式后续有待开发，目前暂不测试
            return r'(?i)GF4.*IRS.*_.*[.]tiff', self.TextMatchType_Regex

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)GF4.*IRS.*_.*[.]tiff',
                                                                 '{0}.tiff'.format(self.classified_object_name())),
                self.Name_ID: 'pms_tif',
                self.Name_Title: '影像文件pms',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]
