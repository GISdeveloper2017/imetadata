# -*- coding: utf-8 -*- 
# @Time : 2020/11/20 18:27
# @Author : 赵宇飞
# @File : distribution_object_vector.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import distribution_guotu


class distribution_object_vector(distribution_guotu):
    """
    todo 王学谦 数据检索分发模块对shp类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'shp矢量'
        info['table_name'] = ''
        return info