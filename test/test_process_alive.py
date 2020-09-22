# -*- coding: utf-8 -*- 
# @Time : 2020/8/19 13:41 
# @Author : 王西亚 
# @File : test_process_alive.py

import random
import time
from multiprocessing import Process


class Myprocess(Process):
    def __init__(self, person):
        self.name = person
        super().__init__()

    def run(self):
        print('子进程开始!')
        while True:
            time.sleep(random.randrange(1, 2))
            print('%s还在和网红脸聊天' % self.name)


if __name__ == '__main__':
    p1 = Myprocess('哪吒')
    p1.start()

    print('子进程{0}开始!'.format(p1.pid))
    # p1.terminate()  # 关闭进程,不会立即关闭,所以is_alive立刻查看的结果可能还是存活
    print(p1.is_alive())  # 结果为True
    time.sleep(20)
    print('开始')
    print(p1.is_alive())  # 结果为False
