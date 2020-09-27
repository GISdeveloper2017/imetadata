# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_2000_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class C21ATBusDataSetPlugins(CDirPlugins):
    __classified_object_type__ = None
    __metadata_xml_obj__ = None

    Path_21AT_MD_Content_ProductType = '/root/ProductType'
    Path_21AT_MD_Content_ProductName = '/root/DNName'

    def get_information(self) -> dict:
        information = super().get_information()
        if self.__metadata_xml_obj__ is not None:
            information[self.Plugins_Info_Title] = CXml.get_element_text(
                self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductName))
            information[self.Plugins_Info_Name] = None
        information[self.Plugins_Info_Code] = '110001'
        information[self.Plugins_Info_Catalog] = '业务数据集'
        information[self.Plugins_Info_Type_Title] = '业务数据集'
        information[self.Plugins_Info_Type] = 'business_data_set'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = 'global_dim'
        information[self.Plugins_Info_DetailEngine] = 'same_file_mainname'
        information[self.Plugins_Info_QCEngine] = None

        return information

    def get_id(self) -> str:
        if self.__classified_object_type__ is not None:
            return CUtils.any_2_str(self.__classified_object_type__)
        else:
            return super().get_id()

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        self.__object_name__ = None

        current_path = self.file_info.__file_name_with_full_path__
        metadata_file_name = CFile.join_file(current_path, 'metadata.21at')
        if CFile.file_or_path_exist(metadata_file_name):
            self.__metadata_xml_obj__ = CXml()
            try:
                self.__metadata_xml_obj__.load_file(metadata_file_name)
                self.__classified_object_type__ = CXml.get_element_text(
                    self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductType))
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = CXml.get_element_text(self.__metadata_xml_obj__.xpath_one(self.Path_21AT_MD_Content_ProductName))
            except:
                self.__metadata_xml_obj__ = None
                CLogger().warning('发现文件{0}符合二十一世纪业务数据集标准, 但该文件格式有误, 无法打开! ')

        return self.__object_confirm__, self.__object_name__

    def parser_metadata(self):
        pass

    def parser_bus_metadata(self):
        pass

    def parser_spatial_metadata(self) -> str:
        pass

    def parser_tags_metadata(self) -> list:
        pass

    def parser_time_metadata(self) -> str:
        pass
