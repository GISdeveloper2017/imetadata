# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:07
# @Author : 赵宇飞
# @File : distribution_ortho.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_ortho(distribution_guotu_object):
    """
    todo 王学谦 数据检索分发模块对单景正射类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '单景正射'
        info[self.Name_Type] = 'ortho'
        info['table_name'] = ''
        return info