from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_hj import CSatFilePlugins_hj


class CSatFilePlugins_hj1c_ccd1(CSatFilePlugins_hj):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'HJ-1C_CCD1'
        information[self.Plugins_Info_Type_Title] = '环境一号C星CCD1传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        环境一号卫星识别
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)^HJ1C-CCD1.*-.*', self.TextMatchType_Regex
        else:
            return r'(?i)^HJ1C-CCD1.*-.*[-]1[.]tif$', self.TextMatchType_Regex
