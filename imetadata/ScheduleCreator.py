#!/usr/bin/python3
# -*- coding:utf-8 -*-

import logging
import argparse
from imetadata.schedule.c_controlCenterExecute import CControlCenterExecute
from imetadata.base.c_logger import CLogger


def start_schedule_creator():
    runner = CControlCenterExecute('0', CControlCenterExecute.TRIGGER_TYPE_DB_QUEUE, 'job_command_runner')
    runner.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""
调度管理进程
作者：王西亚
日期：2020-08-03

说明：
.log:日志文件路径, 可选参数, 不提供将直接打印日志到标准输出

算法:
.系统值守调度管理数据表, 发生调度状态变化时, 系统将根据当前进程的个数, 与目标进程的个数进行对比, 对于要求加速的调度, 将自行启动ScheduleRunner
 命令, 启动增加的调度
.需要减速或者停止(停止调度就是将调度的个数标识为0)的调度, 由ScheduleRunner自行处理

    """)
    parser.add_argument('-log', '--log_filepath', required=False, help='Log文件名', dest='log_filepath')

    args = parser.parse_args()

    if args.log_filepath is not None:
        logging.basicConfig(filename=args.log_filepath + '/schedule.log', level=logging.ERROR,
                            format="%(levelname)s - %(asctime)s - %(message)s",
                            datefmt="%m/%d/%Y %H:%M:%S %p")

    CLogger().info('start run_schedule')
    start_schedule_creator()
    CLogger().info('end run_schedule')
