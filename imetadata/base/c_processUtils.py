# -*- coding: utf-8 -*- 
# @Time : 2020/9/1 15:43 
# @Author : 王西亚 
# @File : c_processUtils.py


import psutil
import os
from imetadata.base.c_logger import CLogger


class CProcessUtils:

    def __init__(self):
        pass

    @classmethod
    def process_id_exist(cls, process_id: int, include_zombie: bool = False) -> bool:
        """
        检查指定进程标识是否在运行
        :param process_id: 进程id=pid
        :param include_zombie: 是否包含僵尸进程
        :return:
        """
        real_process_id = int(process_id)
        for process in psutil.process_iter():
            if process.pid == real_process_id:
                if include_zombie:
                    return True
                elif process.status() == 'running':
                    return True
                else:
                    return False

        return False

    @classmethod
    def process_kill(cls, process_id: int):
        """
        检查指定进程标识是否在运行
        :param process_id: 进程id=pid
        :param include_zombie: 是否包含僵尸进程
        :return:
        """
        real_process_id = int(process_id)
        for process in psutil.process_iter():
            if process.pid == real_process_id:
                for child in process.children():
                    os.kill(child.pid, -1)
                os.kill(process.pid, -1)


if __name__ == "__main__":
    # for p in psutil.process_iter():
    #     print("{0}.{1} is running, status is {2}".format(p.pid, p.name, p.status()))

    subprocess_list = ['physics', 'chemistry', '1997', '2000']
    print(subprocess_list)
    for subprocess_index in range(len(subprocess_list), 0, -1):
        print(subprocess_list[subprocess_index-1])
        subprocess_list.pop(subprocess_index-1)
    print(subprocess_list)
