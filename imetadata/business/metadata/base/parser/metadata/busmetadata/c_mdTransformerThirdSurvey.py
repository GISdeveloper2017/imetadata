# -*- coding: utf-8 -*- 
# @Time : 2020/10/27 14:39
# @Author : 赵宇飞
# @File : c_mdTransformerThirdSurvey.py
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformer import CMDTransformer


class CMDTransformerThirdSurvey(CMDTransformer):
    """
    todo 王学谦  三调mdb里多表 转 业务元数据xml文件
    """

    def process(self) -> str:
        """
        :return:
        """
        super().process()
        pass