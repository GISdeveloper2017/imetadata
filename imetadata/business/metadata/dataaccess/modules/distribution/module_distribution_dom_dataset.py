# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:25
# @Author : 赵宇飞
# @File : module_distribution_dom_dataset.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.dataaccess.modules.base.module_distribution_guotu_dataset import \
    module_distribution_guotu_dataset


class module_distribution_dom_dataset(module_distribution_guotu_dataset):
    """
    数据检索分发模块对数DOM数据集类型数据
    """

    def information(self) -> dict:
        info = dict()
        info[self.Name_Type] = 'business_data_set_dom'
        return info

    def _do_access(self) -> str:
        pass

    def _do_sync(self) -> str:
        """
        todo DOM类型的数据更新到即时服务系统库数据集表ap3_Product_RSP_SDom_whole中，不存在插入，存在则更新
        """
        return CResult.merge_result(
            self.Success,
            '数据集对象[{0}]同步到第三方即时服务系统数据库成功! '.format(self._obj_name)
        )