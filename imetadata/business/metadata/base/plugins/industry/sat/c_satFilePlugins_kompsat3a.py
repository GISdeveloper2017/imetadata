from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.sat.c_satFilePlugins_kompsat3 import CSatFilePlugins_kompsat3


class CSatFilePlugins_kompsat3a(CSatFilePlugins_kompsat3):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'KOMPSAT3a_PMS'
        information[self.Plugins_Info_Type_Title] = 'Kompsat-3a星PMS传感器'
        information[self.Plugins_Info_Group] = 'KOMPSAT3'
        information[self.Plugins_Info_Group_Title] = 'Kompsat-3'
        information[self.Plugins_Info_CopyRight] = 'KARI'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        北京二号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^K3A_.*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^K3A_.*_.*[.]tif$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file(
                '(?i)^K3A_.*_Aux[.]xml',
                '{0}_Aux.xml'.format(self.classified_object_name().replace('_Bundle', '', 1))
            )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)^K3A_.*_.*[.]tif$',
                    '{0}_B.tif'.format(self.classified_object_name().replace('_Bundle', '', 1))
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
                    r'(?i)K3A_.*_br[.]jpg',
                    '{0}_br.jpg'.format(self.classified_object_name().replace('_Bundle', '', 1))
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i)K3A_.*_th[.]jpg',
                    '{0}_th.jpg'.format(self.classified_object_name().replace('_Bundle', '', 1))
                )
            }
        ]