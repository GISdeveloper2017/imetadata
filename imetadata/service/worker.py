# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 15:50 
# @Author : 王西亚 
# @File : worker.py

from multiprocessing import Process, Semaphore, Queue, Lock, Event
import time
from imetadata.base.logger import Logger
from imetadata.schedule.scheduleExecute import scheduleExecute
from imetadata.service import serviceConst


class CWorker(Process):
    __stop_event__: Event = None

    __params__: dict = None
    __cmd_id__: str
    __cmd_title__: str
    __cmd_algorithm__: str
    __cmd_trigger__: str
    __cmd_parallel_count__: int
    __cmd_max_parallel_count__: int

    __runner__: scheduleExecute

    def __init__(self, stop_event, params):
        super().__init__()
        self.__stop_event__ = stop_event
        self.__params__ = params

        self.__cmd_id__ = params[serviceConst.NAME_CMD_ID]
        self.__cmd_title__ = params[serviceConst.NAME_CMD_TITLE]
        self.__cmd_algorithm__ = params[serviceConst.NAME_CMD_ALGORITHM]
        self.__cmd_trigger__ = params[serviceConst.NAME_CMD_TRIGGER]
        self.__cmd_parallel_count__ = params[serviceConst.NAME_CMD_PARALLEL_COUNT]
        self.__cmd_max_parallel_count__ = params[serviceConst.NAME_CMD_MAX_PARALLEL_COUNT]

        # self.__runner__ = scheduleExecute(self.__cmd_id__, self.__cmd_algorithm__, self.__stop_event__)

    def run(self):
        # 在终止进程时，部分进程将得到信号，进入运行机制，但此之前，停止信号应该已经设置！！！进程将直接结束
        if not self.__stop_event__.is_set():
            # self.__runner__ = scheduleExecute(self.__cmd_id__, self.__cmd_algorithm__, self.__stop_event__)
            # self.__runner__.start()
            while True:
                time.sleep(5)
                if self.__stop_event__.is_set():
                    Logger().info('调度{0}.{1}的进程{2}收到关闭事件, 将退出'.format(self.__cmd_title__, self.__cmd_algorithm__, self.pid))
                    break
                else:
                    Logger().info('调度{0}.{1}的进程{2}收到关闭事件, 将再休眠一段时间'.format(self.__cmd_title__, self.__cmd_algorithm__, self.pid))
