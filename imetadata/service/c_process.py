# -*- coding: utf-8 -*- 
# @Time : 2020/9/5 15:17 
# @Author : 王西亚 
# @File : c_processUtils.py

from multiprocessing import Process

from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource


class CProcess(Process, CResource):

    def params_value_by_name(self, params: str, attr_name: str, default_value):
        """
        通过解析传入参数, 直接获取任务执行方面的参数, 该参数都存储在job对象下
        :param params:
        :param attr_name:
        :param default_value:
        :return:
        """
        return CJson().json_attr_value(params, '{0}.{1}'.format(self.Name_Process, attr_name), default_value)
