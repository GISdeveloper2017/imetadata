# -*- coding: utf-8 -*- 
# @Time : 2020/8/19 17:40 
# @Author : 王西亚 
# @File : test_subsubproc-2.py

import os
import time
from multiprocessing import Process, Event


class subsubprocess(Process):
    def __init__(self, event_obj):
        Process.__init__(self)
        self.__event_obj__ = event_obj

    def run(self):
        print("subsub process id: {0}-{1} started".format(os.getpid(), os.getppid()))
        while not self.__event_obj__.is_set():
            print('wait event...')
            self.__event_obj__.wait(2)
        print("subsub process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))


class subprocess(Process):
    def __init__(self, event_obj):
        Process.__init__(self)
        self.__event_obj__ = event_obj

    def run(self):
        print("sub process id: {0} started".format(self.pid))
        subsub = subsubprocess(self.__event_obj__)
        subsub.start()
        subsub.join()
        print("sub process id: {0} stoped".format(self.getpid))


if __name__ == '__main__':
    print("main process id: {0}-{1} started".format(os.getpid(), os.getppid()))
    event = Event()
    p = subprocess(event)
    p.start()
    time.sleep(15)
    event.set()
    print("event.seted")
    p.join()
    print("main process id: {0}-{1} stoped".format(os.getpid(), os.getppid()))