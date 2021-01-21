from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.base.c_opticalSatPlugins import COpticalSatPlugins


class CSatFilePlugins_sj9a(COpticalSatPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'SJ9A'
        information[self.Plugins_Info_Type_Title] = '实践九号'
        information[self.Plugins_Info_Group] = 'SJ9A'
        information[self.Plugins_Info_Group_Title] = '实践九号'
        information[self.Plugins_Info_CopyRight] = '实践中心'
        return information

    def parser_detail_custom(self, object_name):
        match_str = '(?i){0}.*[.].*'.format(object_name[:])
        self.add_different_name_detail_by_match(match_str)
