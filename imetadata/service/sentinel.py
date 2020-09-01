# -*- coding: utf-8 -*- 
# @Time : 2020/8/19 13:56 
# @Author : 王西亚 
# @File : sentinel.py

from multiprocessing import Process, Semaphore, Queue, Lock, Event
import time
from imetadata.base.c_process import CProcess
from imetadata.base.logger import Logger
from imetadata.base.core import const


class CSentinel(Process):
    """
    哨兵进程
    .负责监控队列运行的情况, 当发现有异常死亡的值守进程时, 通过队列, 通知控制中心进程处理
    """

    __control_center_objects__: dict = None
    __control_center_objects_locker__: Lock = None
    __sentinel_callback_queue__: Queue = None
    __stop_event__: Event = None

    def __init__(self, control_center_objects_locker, control_center_objects, stop_event, sentinel_callback_queue):
        super().__init__()
        self.__control_center_objects__ = control_center_objects
        self.__control_center_objects_locker__ = control_center_objects_locker
        self.__stop_event__ = stop_event
        self.__sentinel_callback_queue__ = sentinel_callback_queue

    def run(self):
        while True:
            # 在终止进程时，部分进程将得到信号，进入运行机制，但此之前，停止信号应该已经设置！！！进程将直接结束
            if not self.__stop_event__.is_set():
                break

            # self.check_process_alive()
            time.sleep(15)

    def check_process_alive(self):
        self.__control_center_objects_locker__.acquire()
        try:
            for control_center_object in self.__control_center_objects__:
                subproc_dead_unfortunately = False
                command = control_center_object.params

                cmd_id = command.get(const.NAME_CMD_ID, '')
                cmd_title = command.get(const.NAME_CMD_TITLE, '')

                # 检查进程列表中的进程是否都可用
                for subproc_id in control_center_object.subprocess_list:
                    # 如果子进程已经不可用
                    if not CProcess.process_id_exist(subproc_id):
                        control_center_object.subprocess_list.remove(subproc_id)
                        subproc_dead_unfortunately = True

                # 如果有子进程不幸身亡, 则发送哨兵消息
                if subproc_dead_unfortunately:
                    queue_item = {const.NAME_CMD_ID: cmd_id, const.NAME_CMD_TITLE: cmd_title}
                    self.__sentinel_callback_queue__.put(queue_item)
        finally:
            self.__control_center_objects_locker__.release()
