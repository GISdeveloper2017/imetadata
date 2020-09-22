# -*- coding: utf-8 -*- 
# @Time : 2020/8/14 14:21 
# @Author : 王西亚 
# @File : example1.py

import os
import time
from multiprocessing import Process


def func():
    print("*" * 10)
    time.sleep(1)
    print("sub process id: ", os.getpid())
    print("parent process id: ", os.getppid())
    print("~" * 10)


if __name__ == '__main__':
    p = Process(target=func)
    p.start()
    print("@" * 10)
    print("sub process id: ", os.getpid())
    print("parent process id: ", os.getppid())
    print("#" * 10)
