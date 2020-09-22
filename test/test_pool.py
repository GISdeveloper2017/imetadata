# -*- coding: utf-8 -*- 
# @Time : 2020/8/15 18:51 
# @Author : 王西亚 
# @File : test_pool.py

import os
import time
from multiprocessing import Process, Event


def work(event):
    print('worker %s started' % os.getpid())
    while True:
        print('worker %s will sleep' % os.getpid())
        time.sleep(2)
        if event.is_set():
            print('worker %s accept should_stop event' % os.getpid())
            break
        else:
            print('worker %s can not accept should_stop event' % os.getpid())

    print('worker %s stoped' % os.getpid())


if __name__ == '__main__':
    print('main %s started' % os.getpid())
    event = Event()
    processes = list()
    for i in range(3):
        p = Process(target=work, args=(event,))
        p.start()
        processes.append(p)

    print('main %s will sleep' % os.getpid())
    time.sleep(10)
    print('main %s will send should_stop event' % os.getpid())
    event.set()

    for proc in processes:
        proc.join()
    print('main %s stoped' % os.getpid())
