# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:11
# @Author : 赵宇飞
# @File : distribution_object_guoqing_frame.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_guoqing_frame(distribution_guotu_object):
    """
    todo 王学谦 数据检索分发模块对国情影像-分幅影像类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '国情影像-分幅影像'
        info['table_name'] = 'ap3_product_rsp_gqdom_detail'
        return info
