#!/usr/bin/python3
# -*- coding:utf-8 -*-

import logging
import argparse
from imetadata.schedule.controlCenterExecute import controlCenterExecute
from imetadata.base.logger import Logger


def run_schedule(schedule_id, schedule_algorithm):
    runner = controlCenterExecute(schedule_id, schedule_algorithm)
    runner.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""
调度执行进程
作者：王西亚
日期：2020-08-03

说明：
.id:调度标识, 是数据库中记录的调度
.index:调度的进程索引号, 如果完成指定调度使用多个进程并行处理, 则第一个进程索引号为0,后面依次递增.
  注意: 当进行并行减速时, 将从索引号最高的开始停止服务!!!
.log:日志文件路径, 可选参数, 不提供将直接打印日志到标准输出
    """)
    parser.add_argument('-id', '--id', required=True, help='调度标识', dest='id')
    parser.add_argument('-alg', '--algorithm', required=True, help='算法名称', dest='algorithm')
    parser.add_argument('-log', '--log_filepath', required=False, help='Log文件名', dest='log_filepath')

    args = parser.parse_args()

    if args.log_filepath is not None:
        logging.basicConfig(filename=args.log_filepath + '/schedule.log', level=logging.WARNING,
                            format="%(levelname)s - %(asctime)s - %(message)s",
                            datefmt="%m/%d/%Y %H:%M:%S %p")

    Logger().info('start run_schedule')
    run_schedule(args.id, args.algorithm)
