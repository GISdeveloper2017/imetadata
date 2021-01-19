from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_zy1e(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'ZY1E'
        information[self.Plugins_Info_Type_Title] = '资源一号E星'
        information[self.Plugins_Info_Group] = 'ZY1E'
        information[self.Plugins_Info_Group_Title] = '资源一号E星'
        information[self.Plugins_Info_CopyRight] = '资源中心'
        return information

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/ProductMetaData/ProduceTime',
                self.Name_Format: self.MetaDataFormat_XML

            },
            {
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/ProductMetaData/StartTime',
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/ProductMetaData/EndTime',
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def parser_detail_custom(self, object_name):
        match_str = '(?i){0}.*[.].*'.format(object_name[:])
        self.add_different_name_detail_by_match(match_str)
