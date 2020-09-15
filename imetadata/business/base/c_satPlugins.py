# -*- coding: utf-8 -*- 
# @Time : 2020/9/15 09:09 
# @Author : 王西亚 
# @File : c_satPlugins.py

from imetadata.business.base.c_plugins import CPlugins
from abc import abstractmethod, ABC
from imetadata.base.c_logger import CLogger


class CSatPlugins(CPlugins):
    def get_group_name(self) -> str:
        return 'sat'