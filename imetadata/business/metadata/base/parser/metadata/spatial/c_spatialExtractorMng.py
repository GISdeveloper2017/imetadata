# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:37 
# @Author : 王西亚 
# @File : c_mdExtractorMng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractorAttachedFile import \
    CSpatialExtractorAttachedFile
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractorRaster import CSpatialExtractorRaster
from imetadata.business.metadata.base.parser.metadata.spatial.c_spatialExtractorVector import CSpatialExtractorVector


class CSpatialExtractorMng(CResource):
    @classmethod
    def give_me_extractor(cls, extract_type, object_id: str, object_name: str, file_info: CDMFilePathInfoEx,
                          file_content: CVirtualContent, metadata: CMetaData):
        input_parser_type = CUtils.any_2_str(extract_type)

        if CUtils.equal_ignore_case(input_parser_type, cls.MetaDataEngine_Raster):
            return CSpatialExtractorRaster(object_id, object_name, file_info, file_content, metadata)
        elif CUtils.equal_ignore_case(input_parser_type, cls.MetaDataEngine_Vector):
            return CSpatialExtractorVector(object_id, object_name, file_info, file_content, metadata)
        elif CUtils.equal_ignore_case(input_parser_type, cls.MetaDataEngine_Attached_File):
            return CSpatialExtractorAttachedFile(object_id, object_name, file_info, file_content, metadata)
        else:
            return CParserCustom(object_id, object_name, file_info)
