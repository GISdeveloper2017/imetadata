# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:03 
# @Author : 王西亚 
# @File : c_tagsParserMng.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.tags.c_tagsParser_GD_InMainName import CTagsParser_GF_InMainName
from imetadata.business.metadata.base.parser.tags.c_tagsParser_GD_InRelationPath import CTagsParser_GF_InRelationPath


class CTagsParserMng(CResource):
    @classmethod
    def give_me_parser(cls, parser_type, db_server_id: str, object_id: str, file_info: CFileInfoEx):
        input_parser_type = CUtils.any_2_str(parser_type)

        if CUtils.equal_ignore_case(input_parser_type, cls.TagEngine_Global_Dim_In_MainName):
            return CTagsParser_GF_InMainName(db_server_id, object_id, file_info)
        elif CUtils.equal_ignore_case(input_parser_type, cls.TagEngine_Global_Dim_In_RelationPath):
            return CTagsParser_GF_InRelationPath(db_server_id, object_id, file_info)
        else:
            return CParserCustom(db_server_id, object_id, file_info)
