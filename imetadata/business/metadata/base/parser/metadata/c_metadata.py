# -*- coding: utf-8 -*- 
# @Time : 2020/9/27 16:02 
# @Author : 王西亚 
# @File : c_metadata.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.parser.metadata.quality.c_quality import CQuality
from imetadata.business.metadata.base.parser.metadata.spatial.c_mdSpatial import CMDSpatial


class CMetaData(CResource):
    def __init__(self):
        self.__quality__ = CQuality()

        self.__metadata_extract_result__ = self.DB_False
        self.__metadata_extract_memo__ = ''
        self.__metadata_text__ = None
        self.__metadata_xml__ = CXml()
        self.__metadata_json__ = CJson()
        self.__metadata_type__ = self.MetaDataFormat_Text

        self.__metadata_bus_extract_result__ = self.DB_False
        self.__metadata_bus_extract_memo__ = ''
        self.__metadata_bus_text__ = None
        self.__metadata_bus_xml__ = CXml()
        self.__metadata_bus_json__ = CJson()
        self.__metadata_bus_type__ = self.MetaDataFormat_Text

        self.__thumb_img_file_name__ = ''
        self.__browse_img_file_name__ = ''
        self.__metadata_view_extract_result__ = self.DB_False
        self.__metadata_view_extract_memo__ = ''

        self.__time_information__ = CJson()
        self.__metadata_time_extract_result__ = self.DB_False
        self.__metadata_time_extract_memo__ = ''

        self.__metadata_spatial_extract_result__ = self.DB_False
        self.__metadata_spatial_extract_memo__ = ''
        self.__metadata_spatial__ = CMDSpatial()

    def metadata_time(self):
        if self.__metadata_time_extract_result__ == self.DB_True:
            return self.__metadata_time_extract_result__, self.__metadata_time_extract_memo__, self.__time_information__.to_json()
        else:
            return self.__metadata_time_extract_result__, self.__metadata_time_extract_memo__, ''

    def metadata_view(self):
        if self.__metadata_view_extract_result__ == self.DB_True:
            return self.__metadata_view_extract_result__, self.__metadata_view_extract_memo__, self.__thumb_img_file_name__, self.__browse_img_file_name__
        else:
            return self.__metadata_view_extract_result__, self.__metadata_view_extract_memo__, '', ''

    def metadata_spatial(self):
        if self.__metadata_spatial_extract_result__ == self.DB_True:
            return self.__metadata_spatial_extract_result__, self.__metadata_spatial_extract_memo__, self.__metadata_spatial__
        else:
            return self.__metadata_spatial_extract_result__, self.__metadata_spatial_extract_memo__, self.__metadata_spatial__

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
    def time_information(self) -> CJson:
        return self.__time_information__

    def metadata(self):
        if self.__metadata_type__ == self.MetaDataFormat_Json:
            return self.__metadata_extract_result__, self.__metadata_extract_memo__, self.__metadata_type__, self.__metadata_json__.to_json()
        elif self.__metadata_type__ == self.MetaDataFormat_XML:
            return self.__metadata_extract_result__, self.__metadata_extract_memo__, self.__metadata_type__, self.__metadata_xml__.to_xml()
        else:
            return self.__metadata_extract_result__, self.__metadata_extract_memo__, self.__metadata_type__, self.__metadata_text__

    @property
    def metadata_type(self):
        return self.__metadata_type__

    @property
    def metadata_bus_type(self):
        return self.__metadata_bus_type__

    def metadata_xml(self) -> CXml:
        return self.__metadata_xml__

    def metadata_json(self) -> CJson:
        return self.__metadata_json__

    def metadata_bus_xml(self) -> CXml:
        return self.__metadata_bus_xml__

    def metadata_bus_json(self) -> CJson:
        return self.__metadata_bus_json__

    def metadata_spatial_obj(self) -> CMDSpatial:
        return self.__metadata_spatial__

    def set_metadata_spatial(self, result: int, memo: str, spatial_metadata_type=None, spatial_metadata=None):
        self.__metadata_spatial_extract_result__ = result
        self.__metadata_spatial_extract_memo__ = memo
        if spatial_metadata_type is None:
            return

        if spatial_metadata_type == CResource.Spatial_MetaData_Type_Native_Center:
            self.__metadata_spatial__.native_center = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Native_BBox:
            self.__metadata_spatial__.native_box = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Native_Geom:
            self.__metadata_spatial__.native_geom = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Wgs84_Center:
            self.__metadata_spatial__.wgs84_center = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Wgs84_BBox:
            self.__metadata_spatial__.wgs84_bbox = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Wgs84_Geom:
            self.__metadata_spatial__.wgs84_geom = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Wkt:
            self.__metadata_spatial__.prj_wkt = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Proj4:
            self.__metadata_spatial__.prj_proj4 = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Project:
            self.__metadata_spatial__.prj_project = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Coordinate:
            self.__metadata_spatial__.prj_coordinate = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Degree:
            self.__metadata_spatial__.prj_degree = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Zone:
            self.__metadata_spatial__.prj_zone = spatial_metadata
        elif spatial_metadata_type == CResource.Spatial_MetaData_Type_Prj_Source:
            self.__metadata_spatial__.prj_source = spatial_metadata
        else:
            pass

    def set_metadata_view(self, result: int, memo: str, view_metadata_type=None, view_metadata=None):
        self.__metadata_view_extract_result__ = result
        self.__metadata_view_extract_memo__ = memo
        if view_metadata_type is None:
            return

        if view_metadata_type == CResource.View_MetaData_Type_Browse:
            self.__browse_img_file_name__ = view_metadata
        elif view_metadata_type == CResource.View_MetaData_Type_Thumb:
            self.__thumb_img_file_name__ = view_metadata
        else:
            pass

    def set_metadata_time(self, result: int, memo: str, time_attr_name=None, time_attr_value=None):
        self.__metadata_time_extract_result__ = result
        self.__metadata_time_extract_memo__ = memo
        if time_attr_name is not None:
            self.__time_information__.set_value_of_name(CUtils.any_2_str(time_attr_name), time_attr_value)

    def set_metadata(self, metadata_extract_result: int, metadata_extract_memo: str, metadata_type: int, metadata_text):
        self.__metadata_extract_result__ = metadata_extract_result
        self.__metadata_extract_memo__ = metadata_extract_memo
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

    def set_metadata_file(self, metadata_extract_result: int, metadata_extract_memo: str, metadata_type: int,
                          file_name):
        self.__metadata_extract_result__ = metadata_extract_result
        self.__metadata_extract_memo__ = metadata_extract_memo
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
            return self.__metadata_bus_extract_result__, self.__metadata_bus_extract_memo__, self.__metadata_bus_type__, self.__metadata_bus_json__.to_json()
        elif self.__metadata_bus_type__ == self.MetaDataFormat_XML:
            return self.__metadata_bus_extract_result__, self.__metadata_bus_extract_memo__, self.__metadata_bus_type__, self.__metadata_bus_xml__.to_xml()
        else:
            return self.__metadata_bus_extract_result__, self.__metadata_bus_extract_memo__, self.__metadata_bus_type__, self.__metadata_bus_text__

    def set_metadata_bus(self, metadata_bus_extract_result: int, metadata_bus_extract_memo: str, metadata_bus_type: int,
                         metadata_bus_text):
        self.__metadata_bus_extract_result__ = metadata_bus_extract_result
        self.__metadata_bus_extract_memo__ = metadata_bus_extract_memo
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

    def set_metadata_bus_file(self, metadata_bus_extract_result: int, metadata_bus_extract_memo: str,
                              metadata_type: int, file_name):
        self.__metadata_bus_extract_result__ = metadata_bus_extract_result
        self.__metadata_bus_extract_memo__ = metadata_bus_extract_memo
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
