#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Li'guang


from multiprocessing import Process, Queue,Pipe
import os
import time


class Processer(Process):
    def __init__(self, que):
        Process.__init__(self)
        self.queue = que
        self.running = True
        self.queue2 = Queue()
        self.arg = "Origin"

    def run(self) -> None:
        ppid = os.getppid()
        ppid = os.getpid()
        print('父进程ID：', ppid, '子进程ID：', ppid)
        print('start processing')
        # for i in range(1, 11):
        #     print('processing:', i * 10, '%')
        #     time.sleep(2)
        while self.running:
            # msg = self.queue.get()
            # print("msg")
            # print(msg)
            #
            # if msg == '0':
            #     self.running = False


            msg2 = self.queue2.get()
            print("msg2")
            print(msg2)
            print(self.arg)

            # time.sleep(1)


class Processer2(Process):
    def __init__(self, pip_conn):
        Process.__init__(self)
        self.pipe = pip_conn
        self.running = True

    def run(self) -> None:
        ppid = os.getppid()
        ppid = os.getpid()
        print('父进程ID：', ppid, '子进程ID：', ppid)
        print('start processing')
        while self.running:
            msg = self.pipe.recv()
            print("pipe")
            print(msg)

            time.sleep(1)


if __name__ == "__main__":

    q = Queue()
    p = Processer(q)
    p.start()
    # p.join()
    for i in range(10, -1, -1):
        # q.put(str(i))
        # print(q.qsize())
        p.queue2.put(str(i)+": Queue2")
        p.arg = "23234234"
        time.sleep(5)

    # pip = Pipe()
    # p = Processer2(pip[1])
    # p.start()
    # # p.join()
    # for i in range(10, -1, -1):
    #     pip[0].send(str(i))
    #     time.sleep(5)
    pass
