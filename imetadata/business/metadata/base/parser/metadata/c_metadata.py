# -*- coding: utf-8 -*- 
# @Time : 2020/9/27 16:02 
# @Author : 王西亚 
# @File : c_metadata.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.quality.c_quality import CQuality


class CMetaData(CResource):
    def __init__(self):
        self.__quality__ = CQuality()

        self.__metadata_text__ = None
        self.__metadata_xml__ = CXml()
        self.__metadata_json__ = CJson()
        self.__metadata_type__ = self.MetaDataFormat_Text

        self.__metadata_bus_text__ = None
        self.__metadata_bus_xml__ = CXml()
        self.__metadata_bus_json__ = CJson()
        self.__metadata_bus_type__ = self.MetaDataFormat_Text

        self.__thumb_img_file_name__ = ''
        self.__browse_img_file_name__ = ''

        self.__time_information__ = CJson()

    @property
    def quality(self):
        return self.__quality__

    @property
    def thumb_img_file_name(self):
        return self.__thumb_img_file_name__

    @thumb_img_file_name.setter
    def thumb_img_file_name(self, value):
        self.__thumb_img_file_name__ = value

    @property
    def browse_img_file_name(self):
        return self.__browse_img_file_name__

    @browse_img_file_name.setter
    def browse_img_file_name(self, value):
        self.__browse_img_file_name__ = value

    @property
    def time_information(self):
        return self.__time_information__

    def metadata(self):
        if self.__metadata_type__ == self.MetaDataFormat_Json:
            return self.__metadata_type__, self.__metadata_json__.to_json()
        elif self.__metadata_type__ == self.MetaDataFormat_XML:
            return self.__metadata_type__, self.__metadata_xml__.to_xml()
        else:
            return self.__metadata_type__, self.__metadata_text__

    def metadata_xml(self) -> CXml:
        return self.__metadata_xml__

    def metadata_json(self) -> CJson:
        return self.__metadata_json__

    def metadata_bus_xml(self) -> CXml:
        return self.__metadata_bus_xml__

    def metadata_bus_json(self) -> CJson:
        return self.__metadata_bus_json__

    def set_metadata(self, metadata_type, metadata_text):
        self.__metadata_type__ = metadata_type
        if self.__metadata_type__ == self.MetaDataFormat_Json:
            self.__metadata_text__ = ''
            self.__metadata_xml__ = CXml()
            self.__metadata_json__.load_json_text(metadata_text)
        elif self.__metadata_type__ == self.MetaDataFormat_XML:
            self.__metadata_text__ = ''
            self.__metadata_xml__.load_xml(metadata_text)
            self.__metadata_json__ = CJson()
        else:
            self.__metadata_text__ = metadata_text
            self.__metadata_xml__ = CXml()
            self.__metadata_json__ = CJson()

    def set_metadata_file(self, metadata_type, file_name):
        self.__metadata_type__ = metadata_type
        if self.__metadata_type__ == self.MetaDataFormat_Json:
            self.__metadata_text__ = ''
            self.__metadata_xml__ = CXml()
            self.__metadata_json__.load_file(file_name)
        elif self.__metadata_type__ == self.MetaDataFormat_XML:
            self.__metadata_text__ = ''
            self.__metadata_xml__.load_file(file_name)
            self.__metadata_json__ = CJson()
        else:
            self.__metadata_text__ = CFile.file_2_str(file_name)
            self.__metadata_xml__ = CXml()
            self.__metadata_json__ = CJson()

    def metadata_bus(self):
        if self.__metadata_bus_type__ == self.MetaDataFormat_Json:
            return self.__metadata_bus_type__, self.__metadata_bus_json__.to_json()
        elif self.__metadata_bus_type__ == self.MetaDataFormat_XML:
            return self.__metadata_bus_type__, self.__metadata_bus_xml__.to_xml()
        else:
            return self.__metadata_bus_type__, self.__metadata_bus_text__

    def set_metadata_bus(self, metadata_bus_type, metadata_bus_text):
        self.__metadata_bus_type__ = metadata_bus_type
        if self.__metadata_bus_type__ == self.MetaDataFormat_Json:
            self.__metadata_bus_text__ = ''
            self.__metadata_bus_xml__ = CXml()
            self.__metadata_bus_json__.load_json_text(metadata_bus_text)
        elif self.__metadata_bus_type__ == self.MetaDataFormat_XML:
            self.__metadata_bus_text__ = ''
            self.__metadata_bus_xml__.load_xml(metadata_bus_text)
            self.__metadata_bus_json__ = CJson()
        else:
            self.__metadata_bus_text__ = metadata_bus_text
            self.__metadata_bus_xml__ = CXml()
            self.__metadata_bus_json__ = CJson()

    def set_metadata_file(self, metadata_type, file_name):
        self.__metadata_bus_type__ = metadata_type
        if self.__metadata_bus_type__ == self.MetaDataFormat_Json:
            self.__metadata_bus_text__ = ''
            self.__metadata_bus_xml__ = CXml()
            self.__metadata_bus_json__.load_file(file_name)
        elif self.__metadata_bus_type__ == self.MetaDataFormat_XML:
            self.__metadata_bus_text__ = ''
            self.__metadata_bus_xml__.load_file(file_name)
            self.__metadata_bus_json__ = CJson()
        else:
            self.__metadata_bus_text__ = CFile.file_2_str(file_name)
            self.__metadata_bus_xml__ = CXml()
            self.__metadata_bus_json__ = CJson()