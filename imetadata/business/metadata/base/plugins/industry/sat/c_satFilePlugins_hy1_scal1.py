from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_hy1 import CSatFilePlugins_hy1


class CSatFilePlugins_hy1_scal1(CSatFilePlugins_hy1):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'HY1_SCAL1'
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
            return r'(?i)^H1C_OPER_(?!AIS).*_L1.*', self.TextMatchType_Regex
        else:
            return r'(?i)^H1C_OPER_(?!AIS).*_L1.*[.]tiff$', self.TextMatchType_Regex

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)^H1C_OPER_(?!AIS).*_L1.*[.]tiff$',
                                                                 '{0}.tiff'.format(self.classified_object_name())),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '全色文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]
