from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_gf1_pmsA import CSatFilePlugins_gf1_pmsA


class CSatFilePlugins_gf1_C(CSatFilePlugins_gf1_pmsA):

    def get_information(self) -> dict:
        information = super().get_information()
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

    def get_classified_object_name_of_sat(self, sat_file_status) -> str:
        return super().get_classified_object_name_of_sat(sat_file_status)

    def get_metadata_bus_filename_by_file(self) -> str:
        return super().get_metadata_bus_filename_by_file()

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:

        return super().init_qa_file_list(parser)

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:

        return super().parser_metadata_time_list(parser)

    def parser_metadata_spatial_after_qa(self, parser: CMetaDataParser):

        return super().parser_metadata_spatial_after_qa(parser)

    def parser_metadata_view_list(self, parser: CMetaDataParser):

        return super().parser_metadata_view_list(parser)
