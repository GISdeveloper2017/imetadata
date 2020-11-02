# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_2000_mbtiles.py

from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class plugins_2000_mbtiles(CFilePlugins):
    __metadata_xml_file_name__ = None

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '二十一世纪公司切片'
        information[self.Plugins_Info_Name] = '21at_mbtiles'
        information[self.Plugins_Info_Code] = None
        information[self.Plugins_Info_Catalog] = '切片'
        information[self.Plugins_Info_Type] = 'tiles'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        information[self.Plugins_Info_Group_Name] = self.DataGroup_Raster
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group_Name])

        return information

    def classified(self):
        self._object_confirm = self.Object_Confirm_IUnKnown
        self._object_name = None

        current_path = self.file_info.file_name_with_full_path
        list_mb_tiles_file = CFile.file_or_subpath_of_path(current_path, '*_0.mbtiles')
        list_mb_tiles_metadata_file = CFile.file_or_subpath_of_path(current_path, '*.xml')
        if (len(list_mb_tiles_file) > 0) and (len(list_mb_tiles_metadata_file) > 0):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = self.file_info.file_main_name
            self.__metadata_xml_file_name__ = list_mb_tiles_metadata_file[0]
        return self._object_confirm, self._object_name

    def init_metadata(self, parser: CMetaDataParser):
        """
        提取xml格式的元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        if not CFile.file_or_path_exist(self.__metadata_xml_file_name__):
            parser.metadata.set_metadata(
                self.DB_False,
                '元数据文件[{0}]未找到, 无法处理! '.format(self.__metadata_xml_file_name__),
                self.MetaDataFormat_Text,
                '')
            return CResult.merge_result(self.Failure, '元数据文件[{0}]未找到, 无法处理! '.format(self.__metadata_xml_file_name__))

        try:
            parser.metadata.set_metadata_file(self.DB_True, '元数据文件[{0}]成功加载! '.format(self.__metadata_xml_file_name__),
                                              self.MetaDataFormat_XML, self.__metadata_xml_file_name__)
            return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(self.__metadata_xml_file_name__))
        except Exception as error:
            parser.metadata.set_metadata(
                self.DB_False,
                '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(self.__metadata_xml_file_name__, error.__str__()),
                self.MetaDataFormat_Text,
                '')
            return CResult.merge_result(self.Exception,
                                        '元数据文件[{0}]不是合法的XML格式, 无法处理! '.format(self.__metadata_xml_file_name__))
