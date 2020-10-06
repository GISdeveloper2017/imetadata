# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 10:46 
# @Author : 王西亚 
# @File : c_time.py
import datetime


class CTime:
    @classmethod
    def now(cls):
        return datetime.datetime.now()