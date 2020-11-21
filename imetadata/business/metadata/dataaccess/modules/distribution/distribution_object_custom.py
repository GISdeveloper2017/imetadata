# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:10
# @Author : 赵宇飞
# @File : distribution_object_custom.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_custom(distribution_guotu_object):
    """
    todo 李宪 数据检索分发模块对自定义影像类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '自定义影像'
        info['table_name'] = ''
        return info