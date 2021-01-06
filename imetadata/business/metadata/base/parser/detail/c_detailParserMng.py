# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 14:11 
# @Author : 王西亚 
# @File : c_detailParserMng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.detail.c_detailParser import CDetailParser
from imetadata.business.metadata.base.parser.detail.c_detailParser_all_file_of_dir import CDetailParser_All_File_Of_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_all_file_of_same_dir import \
    CDetailParser_All_File_Of_Same_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_busdataset import CDetailParser_Busdataset
from imetadata.business.metadata.base.parser.detail.c_detailParser_directory_itself import \
    CDetailParser_Directory_Itself
from imetadata.business.metadata.base.parser.detail.c_detailParser_file_itself import CDetailParser_File_Itself
from imetadata.business.metadata.base.parser.detail.c_detailParser_file_of_dir import CDetailParser_File_Of_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_file_of_same_dir import \
    CDetailParser_File_Of_Same_Dir
from imetadata.business.metadata.base.parser.detail.c_detailParser_fuzzy_file_main_name import \
    CDetailParser_Fuzzy_File_Main_Name
from imetadata.business.metadata.base.parser.detail.c_detailParser_same_file_main_name import \
    CDetailParser_Same_File_Main_Name


class CDetailParserMng(CResource):
    @classmethod
    def give_me_parser(cls, parser_type, object_id: str, object_name: str, file_info: CDMFilePathInfoEx,
                       file_custom_list: list):
        input_parser_type = CUtils.any_2_str(parser_type)

        if CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_Same_File_Main_Name):
            return CDetailParser_Same_File_Main_Name(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_File_Itself):
            return CDetailParser_File_Itself(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_Directory_Itself):
            return CDetailParser_Directory_Itself(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_File_Of_Same_Dir):
            return CDetailParser_File_Of_Same_Dir(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_All_File_Of_Same_Dir):
            return CDetailParser_All_File_Of_Same_Dir(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_File_Of_Dir):
            return CDetailParser_File_Of_Dir(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_All_File_Of_Dir):
            return CDetailParser_All_File_Of_Dir(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_Fuzzy_File_Main_Name):
            return CDetailParser_Fuzzy_File_Main_Name(object_id, object_name, file_info, file_custom_list)
        elif CUtils.equal_ignore_case(input_parser_type, cls.DetailEngine_Busdataset):  # 用于入数据集的附属文件metadata.21at
            return CDetailParser_Busdataset(object_id, object_name, file_info, file_custom_list)
        else:
            # 注意, 这里改为基类了, 因为基类中将默认的处理清除已有附属文件的逻辑
            return CDetailParser(object_id, object_name, file_info, file_custom_list)
