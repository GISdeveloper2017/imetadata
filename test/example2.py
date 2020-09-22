# -*- coding: utf-8 -*- 
# @Time : 2020/8/14 14:21 
# @Author : 王西亚 
# @File : example1.py

import os
import time
from multiprocessing import Process


def func(a, b, c):
    print("子进程开始执行!")
    print("*" * 10)
    time.sleep(1)
    print("params: ", a, b, c)
    print("sub process id: ", os.getpid())
    print("parent process id: ", os.getppid())
    print("~" * 10)
    print("子进程执行完毕!")


if __name__ == '__main__':
    print("主进程开始执行!")
    p = Process(target=func, kwargs={"a": "参数一", "b": "参数二", "c": "参数三"})
    p.start()
    print("@" * 10)
    print("sub process id: ", os.getpid())
    print("parent process id: ", os.getppid())
    print("#" * 10)
    print("主进程执行完毕!")
