# -*- coding: utf-8 -*- 
# @Time : 2020/8/17 13:28 
# @Author : 王西亚 
# @File : controlCenter.py

from imetadata.base.c_process import CProcess
from imetadata.base.core import const
from imetadata.base.core.const import *
from multiprocessing import Process, Semaphore, Queue, Lock, Event, Pool, Manager
import time
from imetadata.base.logger import Logger
from imetadata.base.utils import MetaDataUtils
from imetadata.service.sentinel import CSentinel
from imetadata.service.worker import CWorker


class CControlCenter(Process):
    const_command_queue_process_result_empty = 1
    const_command_queue_process_result_notify_terminal = 2

    __shared_control_center_info_locker__: Lock = None
    __shared_control_center_info__: dict = None
    __command_queue__: Queue = None

    __control_center_manager__: Manager = None
    __control_center_objects__: dict = None
    __control_center_objects_locker__: Lock = None

    __sentinel_manager__: Manager = None
    __sentinel_process__: Process = None
    __sentinel_queue__: Queue = None
    __sentinel_stop_event__: Event = None

    def __init__(self, cmd_queue, shared_control_center_info_locker, shared_control_center_info):
        super().__init__()
        self.__command_queue__ = cmd_queue
        self.__shared_control_center_info_locker__ = shared_control_center_info_locker
        self.__shared_control_center_info__ = shared_control_center_info

    def run(self):
        Logger().info('控制中心进程[{0}]启动运行...'.format(self.pid))

        Logger().info('控制中心进程[{0}]启动哨兵值守进程...'.format(self.pid))
        self.__control_center_manager__ = Manager()
        self.__control_center_objects__ = self.__control_center_manager__.dict()
        self.__control_center_objects_locker__ = self.__control_center_manager__.Lock()

        self.__sentinel_manager__ = Manager()
        self.__sentinel_queue__ = self.__sentinel_manager__.Queue()
        self.__sentinel_stop_event__ = self.__sentinel_manager__.Event()
        self.__sentinel_process__ = CSentinel(self.__control_center_objects_locker__, self.__control_center_objects__,
                                              self.__sentinel_stop_event__, self.__sentinel_queue__)
        self.__sentinel_process__.daemon = True
        self.__sentinel_process__.start()

        while True:
            Logger().info('控制中心进程[{0}]开始检查接收任务队列...'.format(self.pid))

            if self.process_queue_command() == self.const_command_queue_process_result_notify_terminal:
                break

            Logger().info('控制中心进程[{0}]开始检查哨兵反馈的消息...'.format(self.pid))
            self.process_queue_sentinel()

            Logger().info('控制中心进程[{0}]开始同步控制中心对外公布的数据...'.format(self.pid))
            # 同步一下控制中心的对外公布数据
            self.sync_shared_control_center_info()
            # 休息一下
            time.sleep(3)

        Logger().info('控制中心进程[{0}]开始进行退出前的准备工作, 该过程会比较复杂漫长...'.format(self.pid))
        # 开始处理退出工作
        self.before_stop()

    def process_queue_command(self) -> int:
        """
        处理命令队列中的所有任务
        :return:
        const_command_queue_process_result_empty: 队列已经处理完毕, 队列清空
        const_command_queue_process_result_notify_terminal: 队列处理中发现了关闭退出的命令, 执行该命令
        """
        while True:
            try:
                command = self.__command_queue__.get(False)
            except:
                Logger().info('控制中心进程[{0}]处理完所有命令队列, 将退出...'.format(self.pid))
                return self.const_command_queue_process_result_empty
            else:
                # 收到关闭消息后，退出循环
                if command is None:
                    Logger().info('控制中心进程[{0}]接收到退出通知, 将退出...'.format(self.pid))
                    return self.const_command_queue_process_result_notify_terminal
                else:
                    # 收到正常消息，开始处理
                    Logger().info('控制中心进程[{0}]接收到正常通知, 将开始处理通知...'.format(self.pid))
                    self.process_command(command)

    def process_queue_sentinel(self):
        """
        处理哨兵发来的消息队列中的任务
        :return:
        """
        while True:
            try:
                sentinel_message = self.__sentinel_process__.get(False)
            except:
                Logger().info('控制中心进程[{0}]处理完所有哨兵反馈的消息, 将退出...'.format(self.pid))
                return
            else:
                # 收到关闭消息后，退出循环
                if sentinel_message is not None:
                    # 收到正常消息，开始处理
                    Logger().info('控制中心进程[{0}]开始检查哨兵反馈的消息, 将开始处理该消息...'.format(self.pid))
                    self.process_sentinel_message(sentinel_message)
                else:
                    Logger().info('控制中心进程[{0}]发现哨兵反馈来停止的消息, 将退出...'.format(self.pid))
                    return

    def process_command(self, command):
        Logger().info('控制中心进程[{0}]开始处理指令{1}...'.format(self.pid, command))
        cmd_type = command.get(const.NAME_CMD_COMMAND, const.CMD_START)
        cmd_title = command.get(const.NAME_CMD_TITLE, '')

        if MetaDataUtils.equal_ignore_case(cmd_type, const.CMD_START):
            Logger().info('控制中心进程[{0}]收到了启动调度的指令...'.format(self.pid))
            self.command_start(command)
        elif MetaDataUtils.equal_ignore_case(cmd_type, const.CMD_STOP):
            Logger().info('控制中心进程[{0}]收到了停止调度的指令...'.format(self.pid))
            self.command_stop(command)
        elif MetaDataUtils.equal_ignore_case(cmd_type, const.CMD_SPEED_UP):
            Logger().info('控制中心进程[{0}]收到了加速调度的指令...'.format(self.pid))
            time.sleep(3)
            print('service: {0} speed up'.format(cmd_title))
        elif MetaDataUtils.equal_ignore_case(cmd_type, const.CMD_SPEED_DOWN):
            Logger().info('控制中心进程[{0}]收到了减速调度的指令...'.format(self.pid))
            time.sleep(3)
            print('service: {0} speed down'.format(cmd_title))

    def process_sentinel_message(self, sentinel_message):
        """
        处理子进程哨兵进程反馈的消息
        :param sentinel_message:
        :return:
        """
        cmd_id = sentinel_message[const.NAME_CMD_ID]
        cmd_title = sentinel_message[const.NAME_CMD_TITLE]
        if cmd_id is None:
            return

        Logger().info('哨兵进程发现调度{0}.{1}的某一个进程无故销毁! '.format(cmd_id, cmd_title))

    def sync_shared_control_center_info(self):
        pass

    def command_start(self, command):
        cmd_id = command.get(const.NAME_CMD_ID, '')
        cmd_title = command.get(const.NAME_CMD_TITLE, '')
        cmd_algorithm = command.get(const.NAME_CMD_ALGORITHM, '')
        cmd_trigger = command.get(const.NAME_CMD_TRIGGER, '')
        cmd_parallel_count = command.get(const.NAME_CMD_PARALLEL_COUNT, 0)
        cmd_max_parallel_count = command.get(const.NAME_CMD_MAX_PARALLEL_COUNT, 0)

        Logger().info('调度{0}.{1}.{2}将启动{3}个并行进程...'.format(cmd_id, cmd_title, cmd_algorithm, cmd_parallel_count))

        params = self.__control_center_manager__.dict()

        params[const.NAME_CMD_ID] = cmd_id
        params[const.NAME_CMD_TITLE] = cmd_title
        params[const.NAME_CMD_ALGORITHM] = cmd_algorithm
        params[const.NAME_CMD_TRIGGER] = cmd_trigger
        params[const.NAME_CMD_PARALLEL_COUNT] = cmd_parallel_count
        params[const.NAME_CMD_MAX_PARALLEL_COUNT] = cmd_max_parallel_count

        control_center_object = self.__control_center_objects__.get(cmd_id, None)
        if control_center_object is not None:
            Logger().warning('调度{0}.{1}.{2}进程池已经启动...'.format(cmd_id, cmd_title, cmd_algorithm))
            return

        stop_event = self.__control_center_manager__.Event()
        subprocess_list = self.__control_center_manager__.list()
        control_center_object = dict()
        control_center_object[const.NAME_PARAMS] = params
        control_center_object[const.NAME_STOP_EVENT] = stop_event
        control_center_object[const.NAME_SUBPROCESS_LIST] = subprocess_list

        for i in range(cmd_parallel_count):
            proc = CWorker(stop_event, params)
            proc.start()
            subprocess_list.append(proc.pid)
            Logger().info('调度{0}.{1}.{2}成功启动了子进程{3}...'.format(cmd_id, cmd_title, cmd_algorithm, proc.pid))

        # 加入对象dict中记录！
        self.__control_center_objects__[cmd_id] = control_center_object

        print(self.__control_center_objects__)

        Logger().info('调度{0}.{1}.{2}成功启动了{3}个并行进程...'.format(cmd_id, cmd_title, cmd_algorithm, cmd_parallel_count))

    def before_stop(self):
        Logger().info('控制中心开始进行调度的清理工作...')

        Logger().info('首先停止哨兵值守进程检查调度...')
        self.__sentinel_stop_event__.set()

        Logger().info('等待哨兵值守进程退出...')
        self.__sentinel_process__.join()
        Logger().info('哨兵值守进程已经停止...')

        if self.__control_center_objects__ is None:
            Logger().info('控制中心对象为None...')
            return

        if len(self.__control_center_objects__) == 0:
            Logger().info('控制中心对象里没有任何池记录...')
            return

        Logger().info('开始处理{0}个调度对象的进程池...'.format(len(self.__control_center_objects__)))
        print(self.__control_center_objects__)

        try:
            self.__control_center_objects_locker__.acquire()

            for control_center_object_key in self.__control_center_objects__:
                Logger().info('已经提取出{0}进程池...'.format(control_center_object_key))
                control_center_object = self.__control_center_objects__.get(control_center_object_key)
                if control_center_object is None:
                    Logger().info('参数对象为None...')
                    self.__control_center_objects__.pop(control_center_object)
                    continue

                command = control_center_object.get(const.NAME_PARAMS, None)
                Logger().info('已经提取出参数对象...')

                if command is None:
                    Logger().info('参数对象为None...')
                    self.__control_center_objects__.pop(control_center_object)
                    continue

                cmd_id = command.get(const.NAME_CMD_ID, '')
                cmd_title = command.get(const.NAME_CMD_TITLE, '')

                Logger().info('控制中心开始清理调度[{0}.{1}]的所有进程...'.format(cmd_id, cmd_title))

                if cmd_id == '':
                    continue

                # 给池里的所有进程，发送关闭信号！
                stop_event = control_center_object.get(const.NAME_STOP_EVENT, None)
                if stop_event is None:
                    continue

                stop_event.set()
                Logger().info('调度{0}.{1}的进程池中所有进程退出的信号已发出...'.format(cmd_id, cmd_title))

                # 等待进程池全部退出
                while True:
                    Logger().info('检查调度{0}.{1}的进程池中所有进程是否都已经退出...'.format(cmd_id, cmd_title))
                    all_subprocess_closed = True
                    subprocess_list = control_center_object.get(const.NAME_SUBPROCESS_LIST)
                    if subprocess_list is None:
                        break

                    for subproc_id in subprocess_list:
                        if CProcess.process_id_exist(subproc_id):
                            Logger().info('检查调度{0}.{1}的进程池中进程{2}仍然在运行...'.format(cmd_id, cmd_title, subproc_id))
                            all_subprocess_closed = False

                    if all_subprocess_closed:
                        Logger().info('检查调度{0}.{1}的进程池中所有进程都已经不在...'.format(cmd_id, cmd_title))
                        break
                    else:
                        time.sleep(1)
                        Logger().info('检查调度{0}.{1}的进程池中还有进程正在运行, 等待中...'.format(cmd_id, cmd_title))

                Logger().info('调度{0}.{1}的进程池中所有进程均已退出...'.format(cmd_id, cmd_title))
                self.__control_center_objects__.pop(control_center_object)
        finally:
            self.__control_center_objects_locker__.release()
            Logger().info('控制中心的所有调度清理工作已完成，控制中心进程将关闭...')

    def command_stop(self, command):
        cmd_id = command[const.NAME_CMD_ID]

        control_center_object = self.__control_center_objects__[cmd_id]
        if control_center_object is None:
            Logger().warning('调度{0}进程池已经不存在, 无需停止...'.format(cmd_id))
            return

        params = control_center_object.params
        cmd_title = params[const.NAME_CMD_TITLE]
        cmd_algorithm = params[const.NAME_CMD_ALGORITHM]

        Logger().info('调度{0}.{1}.{2}将停止...'.format(cmd_id, cmd_title, cmd_algorithm))

        if control_center_object.stop_event is not None:
            control_center_object.stop_event.set()

        if control_center_object.subprocess_list is not None:
            # 这里将等待每一个worker进程关闭, 等待10秒
            for proc in control_center_object.subprocess_list:
                proc.join(30)

            for proc in control_center_object.subprocess_list:
                if proc.is_alive():
                    proc.terminate()

            for proc in control_center_object.subprocess_list:
                if proc.is_alive():
                    proc.join()

            for proc in control_center_object.subprocess_list:
                control_center_object.subprocess_list.remove(proc)

        # 清除对象dict中记录！
        self.__control_center_objects__[cmd_id] = None

        Logger().info('调度{0}.{1}.{2}成功终止..'.format(cmd_id, cmd_title, cmd_algorithm))

