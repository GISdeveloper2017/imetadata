# -*- coding: utf-8 -*- 
# @Time : 2020/9/1 15:43 
# @Author : 王西亚 
# @File : c_processUtils.py


import multiprocessing
import os

import psutil


class CProcessUtils:

    def __init__(self):
        pass

    @classmethod
    def process_id_exist(cls, process_id: int, include_zombie: bool = False) -> bool:
        """
        检查指定进程标识是否在运行
        注意: 有可能在循环检查process的过程中, process正在退出, 导致process.status()方法出现异常
        :param process_id: 进程id=pid
        :param include_zombie: 是否包含僵尸进程
        :return:
        """
        real_process_id = int(process_id)
        for process in psutil.process_iter():
            try:
                if process.pid == real_process_id:
                    if include_zombie:
                        return True
                    elif process.is_running():
                        return process.status() == 'running'
                    else:
                        return False
            except:
                continue

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

    @classmethod
    def processing_method(cls, method_name, parameter):
        """
        王学谦 多进程调用,注意，进程调用只能在if __name__ == '__main__'中使用，不然会出异常
        @param method_name:调用方法名
        @param parameter:调用方法的参数，目前写法仅为单个参数
        @return:调用方法返回的参数
        示例：ret = CGdalUtils.processing_method(CGdalUtils.is_raster_file_can_read, file_src)
        ret即is_raster_file_can_read的返回值
        """
        pool = multiprocessing.Pool(1)
        res = pool.map(method_name, (parameter,))
        pool.close()
        pool.join()
        return res[0]

    # @classmethod
    # def processing_method_params(cls, method_name, parameter_list):
    #     '''
    #     多参数调用模式
    #     '''
    #     str_sign = ','
    #     params_str = str_sign.join(parameter_list)
    #     return cls.processing_method(method_name, params_str)


if __name__ == "__main__":
    str = ','
    list = []
    list.append('a')
    list.append('b')
    list.append('c')
    join_str = str.join(list)
    print(join_str)

    # for p in psutil.process_iter():
    #     print("{0}.{1} is running, status is {2}".format(p.pid, p.name, p.status()))

    # subprocess_list = ['physics', 'chemistry', '1997', '2000']
    # print(subprocess_list)
    # for subprocess_index in range(len(subprocess_list), 0, -1):
    #     print(subprocess_list[subprocess_index - 1])
    #     subprocess_list.pop(subprocess_index - 1)
    # print(subprocess_list)
    pass
