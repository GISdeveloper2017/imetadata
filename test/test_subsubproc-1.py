# -*- coding: utf-8 -*- 
# @Time : 2020/8/19 17:40 
# @Author : 王西亚 
# @File : test_subsubproc-1.py

import os
import time
from multiprocessing import Process, Event


def subsubproc(ev):
    print("subsub process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    while not ev.is_set():
        print('wait event...')
        ev.wait(2)
    print("subsub process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))


def subproc(ev):
    print("sub process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    subsub = Process(target=subsubproc, args=(ev,))
    subsub.start()
    subsub.join()
    print("sub process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))


if __name__ == '__main__':
    print("main process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    event = Event()
    p = Process(target=subproc, args=(event,))
    p.start()
    time.sleep(15)
    event.set()
    print("event.seted")
    p.join()
    print("main process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))
