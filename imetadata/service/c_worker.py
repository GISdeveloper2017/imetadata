# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 15:50 
# @Author : 王西亚 
# @File : c_worker.py

from multiprocessing import Event

import settings
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CUtils
from imetadata.schedule.c_cronWorkerExecute import CCronWorkerExecute
from imetadata.schedule.c_dateWorkerExecute import CDateWorkerExecute
from imetadata.schedule.c_dbQueueWorkerExecute import CDBQueueWorkerExecute
from imetadata.schedule.c_intervalWorkerExecute import CIntervalWorkerExecute
from imetadata.schedule.execute.c_scheduleExecute import CScheduleExecute
from imetadata.service.c_process import CProcess


class CWorker(CProcess):
    __stop_event__: Event = None
    __params__: dict = None

    __cmd_id__: str
    __cmd_title__: str
    __cmd_algorithm__: str
    __cmd_trigger__: str
    __cmd_params__: str

    __runner__: None

    def __init__(self, stop_event, params):
        super().__init__()
        self.__stop_event__ = stop_event
        self.__params__ = params

        self.__cmd_id__ = params.get(self.NAME_CMD_ID, '')
        self.__cmd_title__ = params.get(self.NAME_CMD_TITLE)
        self.__cmd_algorithm__ = params.get(self.NAME_CMD_ALGORITHM, '')
        self.__cmd_trigger__ = params.get(self.NAME_CMD_TRIGGER, '')
        self.__cmd_params__ = params.get(self.NAME_CMD_PARAMS, '')

    def accept_stop_message(self) -> bool:
        try:
            return self.__stop_event__.is_set()
        except BrokenPipeError as error:
            return True

    def run(self):
        # 此时, 才在worker的进程中
        host_settings_dict = CUtils.dict_value_by_name(self.__params__, self.NAME_CMD_SETTINGS, None)
        settings.application.load_obj(host_settings_dict)
        settings.application.init_sys_path()

        # 在终止进程时，部分进程将得到信号，进入运行机制，但此之前，停止信号应该已经设置！！！进程将直接结束
        if not self.accept_stop_message():
            self.__runner__ = self.get_or_create_worker_execute(self.__cmd_id__, self.__cmd_trigger__,
                                                                self.__cmd_algorithm__, self.__cmd_params__,
                                                                self.__stop_event__)
            if self.__runner__ is not None:
                self.__runner__.start()

    def get_or_create_worker_execute(self, work_id, work_trigger, work_algorithm, work_params, stop_event):
        CLogger().info(
            '工人进程[{0}]将创建执行器[{1}.{2}.{3}], 参数为[{4}]...'.format(self.pid, work_id, work_trigger, work_algorithm,
                                                               work_params))
        if work_trigger == CScheduleExecute.TRIGGER_TYPE_DB_QUEUE:
            return CDBQueueWorkerExecute(work_id, work_trigger, work_algorithm, work_params, stop_event)
        elif work_trigger == CScheduleExecute.TRIGGER_TYPE_DATE:
            return CDateWorkerExecute(work_id, work_trigger, work_algorithm, work_params, stop_event)
        elif work_trigger == CScheduleExecute.TRIGGER_TYPE_INTERVAL:
            return CIntervalWorkerExecute(work_id, work_trigger, work_algorithm, work_params, stop_event)
        elif work_trigger == CScheduleExecute.TRIGGER_TYPE_CRON:
            return CCronWorkerExecute(work_id, work_trigger, work_algorithm, work_params, stop_event)
        else:
            return None
