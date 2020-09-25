# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:05 
# @Author : 王西亚 
# @File : c_tagsParser.py
from imetadata.business.metadata.base.parser.c_parser import CParser


class CTagsParser(CParser):
    """
    对标签进行处理
    """
    # 标签识别用的字符串
    __tags_parser_text__: str
    # 标签分隔符
    __tags_parser_split_list__: list = ['\\', '_', '/', '-', ' ']

    def process(self) -> str:
        """
        在这里处理将__file_info__中记录的对象所对应的文件或目录信息, 根据__tags_*变量的定义, 进行标签识别
        todo 负责人: 赵宇飞  内容:完成文件或子目录标签识别, 保存dm2_storage_object.dsoTags中
        :return:
        """
        return super().process()

    def custom_init(self):
        """
        自定义初始化
        对标签识别用的字符串进行设置
        :return:
        """
        super().custom_init()
        self.__tags_parser_text__ = ''
