#!/usr/bin/python3
# -*- coding:utf-8 -*-


# 单例装饰器
def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton
