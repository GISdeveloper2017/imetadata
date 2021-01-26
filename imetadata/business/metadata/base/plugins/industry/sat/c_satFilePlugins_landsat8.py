from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_landsat import CSatFilePlugins_landsat


class CSatFilePlugins_landsat8(CSatFilePlugins_landsat):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'LandSat8'
        information[self.Plugins_Info_Type_Title] = 'LandSat-8星'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^(LS8_C_|LC8|LC08).*_.*', self.TextMatchType_Regex
        else:
            return r'(?i)^(LS8_C_|LC8|LC08).*[.]tif$', self.TextMatchType_Regex
