# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 19:32
# @Author : 赵宇飞
# @File : distribution_dataset_custom.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_dataset import \
    distribution_guotu_dataset


class distribution_dataset_custom(distribution_guotu_dataset):
    """
    todo 李宪 数据检索分发模块对自定义数据集类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '自定义数据集'
        info['table_name'] = ''
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
