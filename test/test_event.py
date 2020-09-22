# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 17:55 
# @Author : 王西亚 
# @File : test_event.py

import os
import time
from multiprocessing import Process, Event


def work(ev):
    print("sub process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    while not ev.is_set():
        print('wait event...')
        ev.wait(2)
    print("sub process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))


if __name__ == '__main__':
    print("main process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    event = Event()
    p = Process(target=work, args=(event,))
    p.start()
    time.sleep(5)
    event.set()
    print("event.seted")
    p.join()
    print("main process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))
