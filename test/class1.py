# -*- coding: utf-8 -*- 
# @Time : 2020/8/14 14:21 
# @Author : 王西亚 
# @File : example1.py

from multiprocessing import Process


class MyProcess(Process):  # 自定义的类要继承Process类
    def __init__(self, n, name):
        super().__init__()  # 如果自己想要传参name, 那么要首先用super()执行父类的init方法
        self.n = n
        self.name = name

    def run(self):
        print("子进程的名字是>>>", self.name)
        print("n的值是>>>", self.n)


if __name__ == '__main__':
    p1 = MyProcess(123, name="子进程01")
    p1.start()  # 给操作系统发送创建进程的指令,子进程创建好之后,要被执行,执行的时候就会执行run方法
    p1.join()
    print("p1.name是>>>", p1.name)
    print("主进程结束")
