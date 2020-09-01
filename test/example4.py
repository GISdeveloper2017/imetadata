# -*- coding: utf-8 -*- 
# @Time : 2020/8/14 14:21 
# @Author : 王西亚 
# @File : example1.py

import time
import os
from multiprocessing import Process


def func(n):
    print("sub process id: {0}-{1}".format(os.getpid(), os.getppid()))
    print(n)


if __name__ == '__main__':
    pro_list = []
    for i in range(10):
        p = Process(target=func, args=(i,))
        p.start()
        pro_list.append(p)
    for p in pro_list:
        p.join()
    print("主进程结束!")