# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:05 
# @Author : 王西亚 
# @File : c_tagsParser_GD_InMainName.py
from imetadata.business.metadata.base.parser.tags.c_tagsParser import CTagsParser


class CTagsParser_GF_InRelationPath(CTagsParser):

    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        super().custom_init()
        self.__tags_parser_text__ = self.file_info.file_path_with_rel_path
