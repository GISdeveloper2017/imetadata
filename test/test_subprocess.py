#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Li'guang

from subprocess import PIPE, Popen

if __name__ == "__main__":
    pth_path = r"C:\Users\Anaconda3\envs\test\python.exe -u"
    exe_path = r"E:\Workspace\Python\test\simulator.py"

    # 输出管道重定向
    process = Popen(pth_path + " " + exe_path, stdin=None, stdout=PIPE, stderr=None, shell=False, bufsize=0)
    print(process.pid)
    for line in process.stdout:
        print(line)
    print(process.returncode)
    # process.terminate()
