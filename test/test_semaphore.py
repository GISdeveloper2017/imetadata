# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 16:24 
# @Author : 王西亚 
# @File : test_semaphore.py

import os
import time
from multiprocessing import Manager, Process, Semaphore


def work(semaphore: Semaphore):
    print("sub process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    semaphore.acquire()
    print("sub process id: {0}-{1} processing".format(os.getpid(), os.getppid()))
    semaphore.release()
    print("sub process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))


if __name__ == '__main__':
    print("main process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    semaphore = Semaphore(1)
    semaphore.acquire()
    p = Process(target=work, args=(semaphore,))
    p.start()
    time.sleep(2)
    semaphore.release()
    print("semaphore.released")
    p.join()
    print("main process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))

