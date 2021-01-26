from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_landsat import CSatFilePlugins_landsat


class CSatFilePlugins_landsat7(CSatFilePlugins_landsat):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'LandSat7'
        information[self.Plugins_Info_Type_Title] = 'LandSat-7星'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^LE(07|7).*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^LE(07|7).*[.]tif$', self.TextMatchType_Regex
