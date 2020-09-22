# -*- coding: utf-8 -*-
# @Time : 2020/9/15 17:00
# @Author : 赵宇飞
# @File : method.py
from imetadata.base.c_file import CFile


def aa():
    dir = 'D:/data/0生态审计/少量数据测试_修改后'
    # file_ralationpath = '\\工业园区规划范围'
    file_ralationpath = '/工业园区规划范围'
    file_fullpath = CFile.join_file(dir, file_ralationpath)
    print(file_fullpath)


if __name__ == "__main__":
    aa()
