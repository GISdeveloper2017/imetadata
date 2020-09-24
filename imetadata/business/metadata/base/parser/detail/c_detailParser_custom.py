# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 10:36 
# @Author : 王西亚 
# @File : c_detailParser_same_file_main_name.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.detail.c_detailParser import CDetailParser


class CDetailParser_Custom(CDetailParser):
    """
    本类不处理业务, 仅仅将该类需要存储的属性保存好即可
    """
    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        pass
