# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 15:30
# @Author : 赵宇飞
# @File : module_distribution_dom.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.dataaccess.modules.base.module_distribution_guotu_object import \
    module_distribution_guotu_object
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class module_distribution_dom(module_distribution_guotu_object):
    """
    数据检索分发模块对数DOM类型数据
    """

    def information(self) -> dict:
        info = dict()
        info[self.Name_Type] = 'dom'
        return info

    def _do_sync(self) -> str:
        """
        todo DOM类型的数据更新到即时服务系统库对象表ap3_product_rsp_sdom_detail中，不存在插入，存在则更新
        """

        return CResult.merge_result(
            self.Success,
            '对象[{0}]同步到第三方即时服务系统数据库成功! '.format(self._obj_name)
        )
