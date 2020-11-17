# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:53
# @Author : 赵宇飞
# @File : distribution_dem_noframe.py

from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_dem_noframe(distribution_guotu_object):
    """
    todo 李宪 数据检索分发模块对DEM非分幅类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'DEM_非分幅'
        info['table_name'] = 'ap3_product_rsp_sdem_detail'
        return info