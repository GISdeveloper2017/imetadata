from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.sat.base.c_satFilePlugins_zy3 import CSatFilePlugins_zy3


class CSatFilePlugins_zy3_zy3(CSatFilePlugins_zy3):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'ZY3_MUX'
        information[self.Plugins_Info_Type_Title] = '资源一号01星MUX传感器'
        information[self.Plugins_Info_CopyRight] = '高分中心'
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
            return r'(?i)^ZY3_(NAD|MUX)_E.*', self.TextMatchType_Regex
        else:
            return r'(?i)^ZY3_(NAD|MUX)_E.*[.]tiff$', self.TextMatchType_Regex

    def get_metadata_bus_filename_by_file(self) -> str:
        """
        卫星数据解压后, 哪个文件是业务元数据?
        :return:
        """
        return CFile.join_file(
            self.file_content.content_root_dir,
            self.get_fuzzy_metadata_file('ZY3(?!.*aux).*.xml', '{0}.xml'.format(self.classified_object_name())
                                         )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        return [
            {
                self.Name_FileName: self.get_fuzzy_metadata_file(r'(?i)^ZY3_(NAD|MUX)_E.*[.]tiff$',
                                                                 '{0}.tiff'.format(self.classified_object_name())),
                self.Name_ID: 'pan_tif',
                self.Name_Title: '全色文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_Format: self.DataFormat_Raster_File
            }
        ]

    def parser_metadata_view_list(self, parser: CMetaDataParser):
        """
        标准模式的反馈预览图和拇指图的名称
        :param parser:
        :return:
        """
        return [
            {
                self.Name_ID: self.View_MetaData_Type_Browse,
                self.Name_FileName: self.get_fuzzy_metadata_file('(?!.*thumb).*.jpg',
                                                                 '{0}.jpg'.format(
                                                                     self.file_info.file_main_name)
                                                                 )
            },
            {
                self.Name_ID: self.View_MetaData_Type_Thumb,
                self.Name_FileName: self.get_fuzzy_metadata_file('.*_thumb.jpg',
                                                                 '{0}_thumb.jpg'.format(
                                                                     self.file_info.file_main_name))
            }
        ]
