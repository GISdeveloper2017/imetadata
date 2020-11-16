# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:25
# @Author : 赵宇飞
# @File : distribution_dom_dataset.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.dataaccess.modules.distribution.base import \
    distribution_guotu_dataset


class distribution_dom_dataset(distribution_guotu_dataset):
    """
    数据检索分发模块对数DOM数据集类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Type] = 'business_data_set_dom'
        return info

    def get_sync_dict(self) -> dict:
        """
        本方法的写法为强规则，字典key为字段名，字典value为对应的值或者sql语句，在写时需要加语句号，子查询语句加(),值加‘’
        子查询：sync_dict['字段名']=“(select 字段 from 表 where id=‘1’)”
        值：sync_dict['字段名']=“‘值’”
        同时，配置插件方法时请在information()方法中添加info['table_name'] = '表名'的字段
        """
        sync_dict = dict()
        return sync_dict
