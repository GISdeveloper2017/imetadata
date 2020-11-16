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
        info['table_name'] = 'ap3_product_rsp_sdom_detail'
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
