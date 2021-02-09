from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_landsat import CSatFilePlugins_landsat


class CSatFilePlugins_landsat5(CSatFilePlugins_landsat):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'LandSat5'
        information[self.Plugins_Info_Type_Title] = 'LandSat-5星'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^(LT5|LT05).*-.*', self.TextMatchType_Regex
        else:
            return r'(?i)^(LT5|LT05).*[.]tif$', self.TextMatchType_Regex

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*VER.jpg',
                    '{0}_VER.jpg'.format(self.classified_object_name())
                ),
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file(
                    r'(?i).*VER.jpg',
                    '{0}_VER.jpg'.format(self.classified_object_name())
                )
            }
        ]
