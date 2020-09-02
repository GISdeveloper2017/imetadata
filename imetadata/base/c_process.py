# -*- coding: utf-8 -*- 
# @Time : 2020/9/1 15:43 
# @Author : 王西亚 
# @File : c_process.py


import psutil
from imetadata.base.logger import Logger


class CProcess:

    def __init__(self):
        pass

    @classmethod
    def process_name_exist(cls, process_name: str) -> bool:
        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                return True
        else:
            return False

    @classmethod
    def process_id_exist(cls, process_id: int) -> bool:
        real_process_id = int(process_id)
        for p in psutil.process_iter():
            if p.pid == real_process_id:
                return True

        return False


if __name__ == "__main__":
    print("*"*10)
    for p in psutil.process_iter():
        print("{0}.{1} is running".format(p.pid, p.name))