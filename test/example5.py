# -*- coding: utf-8 -*- 
# @Time : 2020/8/14 14:21 
# @Author : 王西亚 
# @File : example1.py

import time
from multiprocessing import Process


def func():
    print("子进程开始执行!")
    time.sleep(2)
    print("子进程执行完毕!")


if __name__ == '__main__':
    p = Process(target=func, )
    p.start()
    time.sleep(3)
    p.terminate()  # 给操作系统发送一个关闭进程p1的信号,让操作系统去关闭它
    time.sleep(1)
    """由于操作系统关闭子进程的过程需要做许多事情(如回收资源),这是需要耗费一定时间的,
    如果在给操作系统发出关闭信号后(p1.terminate())立刻判断子进程是否还活着,结果是不准
    确的,此时操作系统正在关闭子进程,所以我们要等待一定时间才可以得到正确的判断结果."""
    print("子进程是否还活着>>>", p.is_alive())
    print("主进程执行完毕!")
