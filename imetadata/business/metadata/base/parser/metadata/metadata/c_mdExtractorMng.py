# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:37 
# @Author : 王西亚 
# @File : c_mdExtractorMng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractorDocument import CMDExtractorDocument
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractorRaster import CMDExtractorRaster
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractorVector import CMDExtractorVector


class CMDExtractorMng(CResource):
    @classmethod
    def give_me_extractor(cls, extract_type, object_id: str, object_name: str, file_info: CDMFilePathInfoEx,
                          file_content: CVirtualContent):
        input_parser_type = CUtils.any_2_str(extract_type)

        if CUtils.equal_ignore_case(input_parser_type, cls.MetaDataEngine_Raster):
            return CMDExtractorRaster(object_id, object_name, file_info, file_content)
        elif CUtils.equal_ignore_case(input_parser_type, cls.MetaDataEngine_Vector):
            return CMDExtractorVector(object_id, object_name, file_info, file_content)
        elif CUtils.equal_ignore_case(input_parser_type, cls.MetaDataEngine_Document):
            return CMDExtractorDocument(object_id, object_name, file_info, file_content)
        else:
            return CParserCustom(object_id, object_name, file_info)
