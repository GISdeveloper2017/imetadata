# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:59
# @Author : 赵宇飞
# @File : distribution_mosaic.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_mosaic(distribution_guotu_object):
    """
    todo 王学谦 数据检索分发模块对镶嵌类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '镶嵌影像'
        info[self.Name_Type] = 'mosaic'
        info['table_name'] = ''
        return info