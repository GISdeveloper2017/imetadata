# -*- coding: utf-8 -*- 
# @Time : 2020/8/14 14:21 
# @Author : 王西亚 
# @File : example1.py

import os
from multiprocessing import Manager, Process, Lock


def work(d, lock):
    with lock:  # 不加锁而操作共享的数据,肯定会出现数据错乱
        print("sub process id: {0}-{1}-{2}".format(os.getpid(), os.getppid(), d['count']))
        d['count'] -= 1


if __name__ == '__main__':
    lock = Lock()
    with Manager() as m:
        dic = m.dict({'count': 100})
        p_l = []
        for i in range(100):
            p = Process(target=work, args=(dic, lock))
            p_l.append(p)
            p.start()
        for p in p_l:
            p.join()
        print(dic)
