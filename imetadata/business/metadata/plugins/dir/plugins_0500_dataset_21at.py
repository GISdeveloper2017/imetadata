# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_1000_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.plugins.c_pathPlugins import CPathPlugins


class plugins_0500_dataset_21at(CPathPlugins):
    __classified_object_type__ = None

    def get_id(self) -> str:
        if self.__classified_object_type__ is not None:
            return CMetaDataUtils.any_2_str(self.__classified_object_type__)
        else:
            return super().get_id()

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        self.__object_name__ = None

        current_path = self.__file_info__.__file_name_with_full_path__
        metadata_file_name = CFile.join_file(current_path, 'metadata.21at')
        if CFile.file_or_path_exist(metadata_file_name):
            xml_obj = CXml()
            try:
                xml_obj.load_file(metadata_file_name)
                self.__classified_object_type__ = CXml.get_element_text(xml_obj.xpath_one('/root/ProductType'))
                self.__object_confirm__ = self.Object_Confirm_IKnown
                self.__object_name__ = CXml.get_element_text(xml_obj.xpath_one('/root/DSName'))
            except:
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
