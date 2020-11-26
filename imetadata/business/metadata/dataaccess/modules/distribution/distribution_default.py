# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 17:14
# @Author : 赵宇飞
# @File : distribution_default.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base


class distribution_default(distribution_base):
    """
    数据检索分发模块对国土中不包含的类型的默认处理，预留
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '默认'
        info['table_name'] = 'ap3_product_rsp'
        return info
