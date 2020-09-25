# -*- coding: utf-8 -*- 
# @Time : 2020/8/17 13:28 
# @Author : 王西亚 
# @File : c_controlCenter.py

import errno
import os
import signal as base_signal
import time
from multiprocessing import Process, Queue, Lock, Event, Manager

from imetadata.base.c_logger import CLogger
from imetadata.base.c_processUtils import CProcessUtils
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.service.c_process import CProcess
from imetadata.service.c_sentinel import CSentinel
from imetadata.service.c_worker import CWorker


class CControlCenter(CProcess):
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

    def wait_child(self, signum, frame):
        CLogger().info('收到SIGCHLD消息')
        try:
            while True:
                # -1 表示任意子进程
                # os.WNOHANG 表示如果没有可用的需要 wait 退出状态的子进程，立即返回不阻塞
                cpid, status = os.waitpid(-1, os.WNOHANG)
                if cpid == 0:
                    CLogger().info('没有子进程可以处理了.')
                    break
                exitcode = status >> 8
                CLogger().info('子进程{0}已退出, 退出码为{1}'.format(cpid, exitcode))
        except OSError as e:
            if e.errno == errno.ECHILD:
                CLogger().info('当前进程没有等待结束的子进程了.')
            else:
                raise
        CLogger().info('处理SIGCHLD消息结束...')

    def run(self):
        if not CUtils.equal_ignore_case(CSys.get_os_name(), self.OS_Windows):
            base_signal.signal(base_signal.SIGCHLD, self.wait_child)

        CLogger().info('控制中心进程[{0}]启动运行...'.format(self.pid))

        CLogger().info('控制中心进程[{0}]启动哨兵值守进程...'.format(self.pid))
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
            CLogger().info('控制中心进程[{0}]开始检查接收任务队列...'.format(self.pid))

            if self.process_queue_command() == self.const_command_queue_process_result_notify_terminal:
                break

            CLogger().info('控制中心进程[{0}]开始检查哨兵反馈的消息...'.format(self.pid))
            self.process_queue_sentinel()

            CLogger().info('控制中心进程[{0}]开始同步控制中心对外公布的数据...'.format(self.pid))
            # 同步一下控制中心的对外公布数据
            self.sync_shared_control_center_info()
            # 休息一下
            time.sleep(3)

        CLogger().info('控制中心进程[{0}]开始进行退出前的准备工作, 该过程会比较复杂漫长...'.format(self.pid))
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
                CLogger().info('控制中心进程[{0}]处理完所有命令队列, 将退出...'.format(self.pid))
                return self.const_command_queue_process_result_empty
            else:
                # 收到关闭消息后，退出循环
                if command is None:
                    CLogger().info('控制中心进程[{0}]接收到退出通知, 将退出...'.format(self.pid))
                    return self.const_command_queue_process_result_notify_terminal
                else:
                    # 收到正常消息，开始处理
                    CLogger().info('控制中心进程[{0}]接收到正常通知, 将开始处理通知...'.format(self.pid))
                    self.process_command(command)

    def process_queue_sentinel(self):
        """
        处理哨兵发来的消息队列中的任务
        :return:
        """
        while True:
            try:
                sentinel_message = self.__sentinel_queue__.get(False)
            except:
                CLogger().info('控制中心进程[{0}]处理完所有哨兵反馈的消息, 将退出...'.format(self.pid))
                return
            else:
                # 收到关闭消息后，退出循环
                if sentinel_message is not None:
                    # 收到正常消息，开始处理
                    CLogger().info('控制中心进程[{0}]开始检查哨兵反馈的消息, 将开始处理该消息...'.format(self.pid))
                    self.process_sentinel_message(sentinel_message)
                else:
                    CLogger().info('控制中心进程[{0}]发现哨兵反馈来停止的消息, 将退出...'.format(self.pid))
                    return

    def process_command(self, command):
        CLogger().info('控制中心进程[{0}]开始处理指令{1}...'.format(self.pid, command))
        cmd_type = command.get(self.NAME_CMD_COMMAND, self.CMD_START)
        cmd_title = command.get(self.NAME_CMD_TITLE, '')

        if CUtils.equal_ignore_case(cmd_type, self.CMD_START):
            CLogger().info('控制中心进程[{0}]收到了启动调度的指令...'.format(self.pid))
            self.command_start(command)
        elif CUtils.equal_ignore_case(cmd_type, self.CMD_STOP):
            CLogger().info('控制中心进程[{0}]收到了停止调度的指令...'.format(self.pid))
            self.command_stop(command)
        elif CUtils.equal_ignore_case(cmd_type, self.CMD_FORCE_STOP):
            CLogger().info('控制中心进程[{0}]收到了强制停止调度的指令...'.format(self.pid))
            self.command_force_stop(command)

    def process_sentinel_message(self, sentinel_message):
        """
        处理子进程哨兵进程反馈的消息
        :param sentinel_message:
        :return:
        """
        cmd_id = sentinel_message.get(self.NAME_CMD_ID)
        cmd_title = sentinel_message.get(self.NAME_CMD_TITLE)
        if cmd_id is None:
            return

        CLogger().info('哨兵进程发现调度{0}.{1}的某一个进程无故销毁! '.format(cmd_id, cmd_title))

    def sync_shared_control_center_info(self):
        pass

    def command_start(self, command):
        cmd_id = command.get(self.NAME_CMD_ID, '')
        cmd_title = command.get(self.NAME_CMD_TITLE, '')
        cmd_algorithm = command.get(self.NAME_CMD_ALGORITHM, '')
        cmd_trigger = command.get(self.NAME_CMD_TRIGGER, '')
        cmd_params = command.get(self.NAME_CMD_PARAMS, '')
        CLogger().info('调度{0}.{1}.{2}的调度参数为[{3}]...'.format(cmd_id, cmd_title, cmd_algorithm, cmd_params))

        cmd_parallel_count = super().params_value_by_name(cmd_params, self.Name_Parallel_Count, 1)
        CLogger().info('调度{0}.{1}.{2}的调度并行个数为{3}...'.format(cmd_id, cmd_title, cmd_algorithm, cmd_parallel_count))

        if cmd_parallel_count <= 0:
            CLogger().info('调度{0}.{1}.{2}的目标并行数量为0, 系统直接进行调度的停止操作...'.format(cmd_id, cmd_title, cmd_algorithm))
            self.command_stop(command)
            return

        control_center_object = self.__control_center_objects__.get(cmd_id)
        if control_center_object is not None:
            CLogger().info('调度{0}.{1}.{2}进程池已经启动, 系统不再继续...'.format(cmd_id, cmd_title, cmd_algorithm))
            return

        CLogger().info('调度{0}.{1}.{2}将改为{3}个并行进程...'.format(cmd_id, cmd_title, cmd_algorithm, cmd_parallel_count))

        params = self.__control_center_manager__.dict()

        params[self.NAME_CMD_ID] = cmd_id
        params[self.NAME_CMD_TITLE] = cmd_title
        params[self.NAME_CMD_ALGORITHM] = cmd_algorithm
        params[self.NAME_CMD_TRIGGER] = cmd_trigger
        params[self.NAME_CMD_PARAMS] = cmd_params

        stop_event = self.__control_center_manager__.Event()
        subprocess_list = self.__control_center_manager__.list()
        control_center_object = dict()
        control_center_object[self.NAME_PARAMS] = params
        control_center_object[self.NAME_STOP_EVENT] = stop_event
        control_center_object[self.NAME_SUBPROCESS_LIST] = subprocess_list

        for i in range(cmd_parallel_count):
            proc = CWorker(stop_event, params)
            proc.start()
            subprocess_list.append(proc.pid)
            CLogger().info('调度{0}.{1}.{2}成功启动了子进程{3}...'.format(cmd_id, cmd_title, cmd_algorithm, proc.pid))

        # 加入对象dict中记录！
        self.__control_center_objects__[cmd_id] = control_center_object

        CLogger().info('调度{0}.{1}.{2}成功启动了{3}个并行进程...'.format(cmd_id, cmd_title, cmd_algorithm, cmd_parallel_count))

    def command_stop(self, command):
        """
        处理发来的停止命令

        :param command:
        :return:
        """
        cmd_id = command.get(self.NAME_CMD_ID, '')
        cmd_title = command.get(self.NAME_CMD_TITLE, '')

        CLogger().info('控制中心开始停止调度[{0}.{1}]...'.format(cmd_id, cmd_title))

        if self.__control_center_objects__ is None:
            CLogger().info('控制中心对象为None...')
            return

        if len(self.__control_center_objects__) == 0:
            CLogger().info('控制中心对象里没有任何池记录...')
            return
        try:
            self.__control_center_objects_locker__.acquire()

            control_center_object = self.__control_center_objects__.get(cmd_id)
            if control_center_object is None:
                CLogger().warning('调度{0}进程池已经不存在, 无需停止...'.format(cmd_id))
                return

            # 给池里的所有进程，发送关闭信号！
            stop_event = control_center_object.get(self.NAME_STOP_EVENT, None)
            if stop_event is not None:
                stop_event.set()
                CLogger().info('调度{0}.{1}的进程池中所有进程退出的信号已发出, 进程池的检查和关闭, 将在哨兵进程中处理...'.format(cmd_id, cmd_title))
            else:
                CLogger().info('调度{0}.{1}的进程池退出信号灯已经无效, 进程池的检查和关闭, 将在哨兵进程中处理...'.format(cmd_id, cmd_title))
        finally:
            self.__control_center_objects_locker__.release()
            CLogger().info('控制中心已经停止调度[{0}.{1}]'.format(cmd_id, cmd_title))

    def before_stop(self):
        CLogger().info('控制中心开始进行调度的清理工作...')

        CLogger().info('首先停止哨兵值守进程检查调度...')
        self.__sentinel_stop_event__.set()

        CLogger().info('等待哨兵值守进程退出...')
        self.__sentinel_process__.join()
        CLogger().info('哨兵值守进程已经停止...')

        if self.__control_center_objects__ is None:
            CLogger().info('控制中心对象为None...')
            return

        if len(self.__control_center_objects__) == 0:
            CLogger().info('控制中心对象里没有任何池记录...')
            return

        CLogger().info('开始处理{0}个调度对象的进程池...'.format(len(self.__control_center_objects__)))

        try:
            self.__control_center_objects_locker__.acquire()

            control_center_object_key_list = self.__control_center_objects__.keys()
            for control_center_object_key in control_center_object_key_list:
                CLogger().info('已经提取出{0}进程池...'.format(control_center_object_key))
                control_center_object = self.__control_center_objects__.get(control_center_object_key)
                if control_center_object is None:
                    CLogger().info('参数对象为None...')
                    self.__control_center_objects__.pop(control_center_object_key)
                    continue

                command = control_center_object.get(self.NAME_PARAMS, None)
                CLogger().info('已经提取出参数对象...')

                if command is None:
                    CLogger().info('参数对象为None...')
                    self.__control_center_objects__.pop(control_center_object_key)
                    continue

                cmd_id = command.get(self.NAME_CMD_ID, '')
                cmd_title = command.get(self.NAME_CMD_TITLE, '')

                CLogger().info('控制中心开始清理调度[{0}.{1}]的所有进程...'.format(cmd_id, cmd_title))

                if cmd_id == '':
                    continue

                # 给池里的所有进程，发送关闭信号！
                stop_event = control_center_object.get(self.NAME_STOP_EVENT, None)
                if stop_event is None:
                    continue

                stop_event.set()
                CLogger().info('调度{0}.{1}的进程池中所有进程退出的信号已发出...'.format(cmd_id, cmd_title))

                # 等待进程池全部退出
                while True:
                    CLogger().info('检查调度{0}.{1}的进程池中所有进程是否都已经退出...'.format(cmd_id, cmd_title))
                    all_subprocess_closed = True
                    subprocess_list = control_center_object.get(self.NAME_SUBPROCESS_LIST)
                    if subprocess_list is None:
                        break

                    for subproc_id in subprocess_list:
                        if CProcessUtils.process_id_exist(subproc_id):
                            CLogger().info('检查调度{0}.{1}的进程池中进程{2}仍然在运行...'.format(cmd_id, cmd_title, subproc_id))
                            all_subprocess_closed = False

                    if all_subprocess_closed:
                        CLogger().info('检查调度{0}.{1}的进程池中所有进程都已经不在...'.format(cmd_id, cmd_title))
                        break
                    else:
                        time.sleep(1)
                        CLogger().info('检查调度{0}.{1}的进程池中还有进程正在运行, 等待中...'.format(cmd_id, cmd_title))

                CLogger().info('调度{0}.{1}的进程池中所有进程均已退出...'.format(cmd_id, cmd_title))
                self.__control_center_objects__.pop(control_center_object_key)
        finally:
            self.__control_center_objects_locker__.release()
            CLogger().info('控制中心的所有调度清理工作已完成，控制中心进程将关闭...')

    def command_force_stop(self, command):
        """
        处理发来的强制停止命令

        :param command:
        :return:
        """
        cmd_id = command.get(self.NAME_CMD_ID, '')
        cmd_title = command.get(self.NAME_CMD_TITLE, '')

        CLogger().info('控制中心开始停止调度[{0}.{1}]...'.format(cmd_id, cmd_title))

        if self.__control_center_objects__ is None:
            CLogger().info('控制中心对象为None...')
            return

        if len(self.__control_center_objects__) == 0:
            CLogger().info('控制中心对象里没有任何池记录...')
            return
        try:
            self.__control_center_objects_locker__.acquire()

            control_center_object = self.__control_center_objects__.get(cmd_id)
            if control_center_object is None:
                CLogger().warning('调度{0}进程池已经不存在, 无需停止...'.format(cmd_id))
                return

            # 给池里的所有进程，发送关闭信号！
            stop_event = control_center_object.get(self.NAME_STOP_EVENT, None)
            if stop_event is not None:
                stop_event.set()
                CLogger().info('调度{0}.{1}的进程池中所有进程退出的信号已发出...'.format(cmd_id, cmd_title))

            # 直接杀死进程池中的全部子进程
            subprocess_list = control_center_object.get(self.NAME_SUBPROCESS_LIST)
            if subprocess_list is not None:
                for subproc_id in subprocess_list:
                    CProcessUtils.process_kill(subproc_id)

            CLogger().info('调度{0}.{1}的进程池中所有进程均已退出...'.format(cmd_id, cmd_title))
            self.__control_center_objects__.pop(cmd_id)
        finally:
            self.__control_center_objects_locker__.release()
            CLogger().info('控制中心已经停止调度[{0}.{1}]'.format(cmd_id, cmd_title))
