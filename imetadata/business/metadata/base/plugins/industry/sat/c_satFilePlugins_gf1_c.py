from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf1 import CSatFilePlugins_gf1


class CSatFilePlugins_gf1_c(CSatFilePlugins_gf1):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'GF1_PMS'
        information[self.Plugins_Info_Type_Title] = '高分一号C星PMS传感器'
        return information

    def get_classified_character_of_sat(self, sat_file_status):
        """
        设置识别的特征
        . 如果是压缩包, 则是针对压缩包的文件主名
        . 如果是子目录, 则是针对目录的名称
        :param sat_file_status 卫星数据类型
            . Sat_Object_Status_Zip = 'zip'
            . Sat_Object_Status_Dir = 'dir'
            . Sat_Object_Status_File = 'file'
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        if (sat_file_status == self.Sat_Object_Status_Zip) or (sat_file_status == self.Sat_Object_Status_Dir):
            return r'(?i)gf1c_pms.*[_].*', self.TextMatchType_Regex
        else:
            return r'(?i)gf1c_pms.*[_].*-pan.tiff', self.TextMatchType_Regex
