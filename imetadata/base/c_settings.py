# -*- coding: utf-8 -*- 
# @Time : 2020/10/24 10:16 
# @Author : 王西亚 
# @File : c_settings.py
from imetadata.base.c_json import CJson


class CSettings(CJson):
    def __init__(self, obj):
        super().__init__()
        self.load_obj(obj)
