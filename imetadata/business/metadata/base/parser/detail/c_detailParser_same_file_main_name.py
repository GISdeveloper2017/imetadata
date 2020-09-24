# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 10:36 
# @Author : 王西亚 
# @File : c_detailParser_same_file_main_name.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.detail.c_detailParser import CDetailParser


class CDetailParser_Same_File_Main_Name(CDetailParser):
    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        self.__detail_file_path__ = self.__file_info__.__file_path__
        self.__detail_file_recurse__ = False
        self.__detail_file_match_type__ = CFile.MatchType_Common
        self.__detail_file_match_text__ = '{0}.*'.format(self.__file_info__.__file_main_name__)