# -*- coding: utf-8 -*- 
# @Time : 2020/8/19 13:56 
# @Author : 王西亚 
# @File : c_sentinel.py

import time
from multiprocessing import Queue, Lock, Event

from imetadata import settings
from imetadata.base.c_logger import CLogger
from imetadata.base.c_processUtils import CProcessUtils
from imetadata.base.c_utils import CUtils
from imetadata.service.c_process import CProcess


class CSentinel(CProcess):
    """
    哨兵进程
    .负责监控队列运行的情况, 当发现有异常死亡的值守进程时, 通过队列, 通知控制中心进程处理
    """
    __control_center_objects__: dict = None
    __control_center_objects_locker__: Lock = None
    __sentinel_callback_queue__: Queue = None
    __stop_event__: Event = None
    __control_center_params: dict = None

    def __init__(self, control_center_objects_locker, control_center_objects, stop_event, sentinel_callback_queue,
                 control_center_params):
        super().__init__()
        self.__control_center_objects__ = control_center_objects
        self.__control_center_objects_locker__ = control_center_objects_locker
        self.__stop_event__ = stop_event
        self.__sentinel_callback_queue__ = sentinel_callback_queue
        self.__control_center_params = control_center_params

    def run(self):
        # 此时, 才在sentinel的进程中
        host_settings_dict = CUtils.dict_value_by_name(
            self.__control_center_params,
            self.NAME_CMD_SETTINGS,
            None
        )
        settings.application.load_obj(host_settings_dict)
        settings.application.init_sys_path()

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

                command = control_center_object.get(self.NAME_PARAMS, None)

                cmd_id = command.get(self.NAME_CMD_ID, '')
                cmd_title = command.get(self.NAME_CMD_TITLE, '')

                CLogger().info('哨兵进程{0}开始检查调度[{1}.{2}]的子进程...'.format(self.pid, cmd_id, cmd_title))

                stop_event = control_center_object.get(self.NAME_STOP_EVENT, None)
                # 如果该调度的停止信号已经发出, 则不必检查该调度的进程状态了.
                if stop_event.is_set():
                    CLogger().info(
                        '哨兵进程{0}发现调度[{1}.{2}]已经设置为退出, 将在本轮检查所有进程退出, 当所有进程退出后, 将把进程池删除...'.format(self.pid, cmd_id,
                                                                                                 cmd_title))

                    # 检查进程池中的进程是否全部退出, 本次未全部退出也没关系, 下次再检查
                    CLogger().info('检查调度{0}.{1}的进程池中所有进程是否都已经退出...'.format(cmd_id, cmd_title))
                    all_subprocess_closed = True
                    subprocess_list = control_center_object.get(self.NAME_SUBPROCESS_LIST)
                    if subprocess_list is not None:
                        for subproc_id in subprocess_list:
                            if CProcessUtils.process_id_exist(subproc_id):
                                CLogger().info('检查调度{0}.{1}的进程池中进程{2}仍然在运行...'.format(cmd_id, cmd_title, subproc_id))
                                all_subprocess_closed = False
                                break

                    if all_subprocess_closed:
                        CLogger().info('调度{0}.{1}的进程池中所有进程均已退出, 进程池将被删除...'.format(cmd_id, cmd_title))
                        self.__control_center_objects__.pop(cmd_id)
                else:
                    CLogger().info('哨兵进程{0}发现调度[{1}.{2}]仍然为正常运行, 系统将检查进程是否异常退出...'.format(self.pid, cmd_id, cmd_title))
                    # 检查进程列表中的进程是否都可用
                    subproc_dead_unfortunately = False
                    subprocess_list = control_center_object.get(self.NAME_SUBPROCESS_LIST)
                    for subprocess_index in range(len(subprocess_list), 0, -1):
                        subproc_id = subprocess_list[subprocess_index - 1]
                        # 如果子进程已经不可用
                        if not CProcessUtils.process_id_exist(subproc_id):
                            CLogger().info(
                                '哨兵进程{0}发现调度[{1}.{2}]的子进程{3}已经不存在...'.format(self.pid, cmd_id, cmd_title, subproc_id))
                            subprocess_list.pop(subprocess_index - 1)
                            subproc_dead_unfortunately = True
                        else:
                            CLogger().info(
                                '哨兵进程{0}发现调度[{1}.{2}]的子进程{3}正常运行...'.format(self.pid, cmd_id, cmd_title, subproc_id))

                    # 如果有子进程不幸身亡, 则发送哨兵消息
                    if subproc_dead_unfortunately:
                        CLogger().info(
                            '哨兵进程{0}发现调度[{1}.{2}]中的子进程有中途崩溃情况, 首先更新进程共享对象...'.format(self.pid, cmd_id, cmd_title))
                        self.__control_center_objects__[cmd_id] = control_center_object

                        CLogger().info(
                            '哨兵进程{0}发现调度[{1}.{2}]中的子进程有中途崩溃情况, 将发信息给控制进程...'.format(self.pid, cmd_id, cmd_title))
                        queue_item = {self.NAME_CMD_ID: cmd_id, self.NAME_CMD_TITLE: cmd_title}
                        self.__sentinel_callback_queue__.put(queue_item)
        finally:
            self.__control_center_objects_locker__.release()
