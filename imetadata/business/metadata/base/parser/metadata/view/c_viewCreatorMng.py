# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:37 
# @Author : 王西亚 
# @File : c_mdExtractorMng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreatorDocument import CViewCreatorDocument
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreatorRaster import CViewCreatorRaster
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreatorVector import CViewCreatorVector


class CViewCreatorMng(CResource):
    @classmethod
    def give_me_creator(cls, extract_type, object_id: str, object_name: str, file_info: CDMFilePathInfoEx,
                        file_content: CVirtualContent):
        input_parser_type = CUtils.any_2_str(extract_type)

        if CUtils.equal_ignore_case(input_parser_type, cls.BrowseEngine_Raster):
            return CViewCreatorRaster(object_id, object_name, file_info, file_content)
        elif CUtils.equal_ignore_case(input_parser_type, cls.BrowseEngine_Vector):
            return CViewCreatorVector(object_id, object_name, file_info, file_content)
        elif CUtils.equal_ignore_case(input_parser_type, cls.BrowseEngine_Document):
            return CViewCreatorDocument(object_id, object_name, file_info, file_content)
        else:
            return CParserCustom(object_id, object_name, file_info)
