# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:23
# @Author : 赵宇飞
# @File : module_distribution_guotu_dataset.py
from imetadata.business.metadata.dataaccess.modules.base.module_distribution_guotu import \
    module_distribution_guotu


class module_distribution_guotu_dataset(module_distribution_guotu):
    """"
    数据集对象处理基类（即时服务）
    """
    def _before_access(self):
        pass

    def _before_sync(self):
        """
        查询数据库，设置通常的字段值到self._dict_sync中，用于子类个性化构建sql字段值用
        """
        pass