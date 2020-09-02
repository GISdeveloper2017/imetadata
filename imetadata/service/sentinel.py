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
    const_NAME_CMD_ID = 'cmd_id'
    const_NAME_CMD_TITLE = 'cmd_title'
    const_NAME_CMD_TRIGGER = 'cmd_trigger'
    const_NAME_CMD_ALGORITHM = 'cmd_algorithm'
    const_NAME_CMD_PARALLEL_COUNT = 'cmd_parallel_count'
    const_NAME_CMD_MAX_PARALLEL_COUNT = 'cmd_max_parallel_count'

    const_NAME_PARAMS = 'params'
    const_NAME_STOP_EVENT = 'stop_event'
    const_NAME_SUBPROCESS_LIST = 'subprocess_list'

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
            if self.__stop_event__.is_set():
                return

            self.check_process_alive()
            time.sleep(10)

    def check_process_alive(self):
        self.__control_center_objects_locker__.acquire()
        try:
            control_center_object_key_list = self.__control_center_objects__.keys()
            for control_center_object_key in control_center_object_key_list:
                control_center_object = self.__control_center_objects__.get(control_center_object_key)

                command = control_center_object.get(self.const_NAME_PARAMS, None)

                cmd_id = command.get(self.const_NAME_CMD_ID, '')
                cmd_title = command.get(self.const_NAME_CMD_TITLE, '')

                Logger().info('哨兵进程{0}开始检查调度[{1}.{2}]的子进程...'.format(self.pid, cmd_id, cmd_title))

                stop_event = control_center_object.get(self.const_NAME_STOP_EVENT, None)
                # 如果该调度的停止信号已经发出, 则不必检查该调度的进程状态了.
                if stop_event.is_set():
                    Logger().info('哨兵进程{0}发现调度[{1}.{2}]已经设置为退出, 将忽略检查...'.format(self.pid, cmd_id, cmd_title))
                    continue

                # 检查进程列表中的进程是否都可用
                subproc_dead_unfortunately = False
                subprocess_list = control_center_object.get(self.const_NAME_SUBPROCESS_LIST)
                for subprocess_index in range(len(subprocess_list), 0, -1):
                    subproc_id = subprocess_list[subprocess_index - 1]
                    # 如果子进程已经不可用
                    if not CProcess.process_id_exist(subproc_id):
                        Logger().info(
                            '哨兵进程{0}发现调度[{1}.{2}]的子进程{3}已经不存在...'.format(self.pid, cmd_id, cmd_title, subproc_id))
                        subprocess_list.pop(subprocess_index - 1)
                        subproc_dead_unfortunately = True
                    else:
                        Logger().info(
                            '哨兵进程{0}发现调度[{1}.{2}]的子进程{3}正常运行...'.format(self.pid, cmd_id, cmd_title, subproc_id))

                # 如果有子进程不幸身亡, 则发送哨兵消息
                if subproc_dead_unfortunately:
                    Logger().info('哨兵进程{0}发现调度[{1}.{2}]中的子进程有中途崩溃情况, 首先更新进程共享对象...'.format(self.pid, cmd_id, cmd_title))
                    self.__control_center_objects__[cmd_id] = control_center_object

                    Logger().info('哨兵进程{0}发现调度[{1}.{2}]中的子进程有中途崩溃情况, 将发信息给控制进程...'.format(self.pid, cmd_id, cmd_title))
                    queue_item = {self.const_NAME_CMD_ID: cmd_id, self.const_NAME_CMD_TITLE: cmd_title}
                    self.__sentinel_callback_queue__.put(queue_item)
        finally:
            self.__control_center_objects_locker__.release()
