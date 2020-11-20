# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:23
# @Author : 赵宇飞
# @File : distribution_guotu_dataset.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import \
    distribution_guotu
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_json import CJson
from imetadata.base.c_xml import CXml
import datetime


class distribution_guotu_dataset(distribution_guotu):
    """"
    数据集对象处理基类（即时服务）
    """

    def information(self) -> dict:
        info = super().information()
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        return self.get_sync_predefined_dict_list(insert_or_updata)

    def get_sync_predefined_dict_list(self, insert_or_updata) -> list:
        """
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = list()
        return sync_dict_list
