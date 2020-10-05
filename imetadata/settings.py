# -*- coding: utf-8 -*-
# @Time : 2020/9/15 12:54
# @Author : 王西亚
# @File : settings.py

"""
应用程序配置:
. databases: 数据库配置
    . 类型: 数组
    . 项目: 数据库的配置
. directory: 目录
    . work: 工作目录, 也是临时目录
. metadata: 数管.元数据管理
    . directory: 目录
        . view: 数管的快视图存储的目录
"""

application = {
    'databases': [
        {'id': '0', 'type': 'postgresql',
         'host': '127.0.0.1', 'port': '5432', 'database': 'test', 'username': 'postgres', 'password': 'postgres'}
    ],
    'directory': {
        'work': ''
    },
    'metadata': {
        'directory': {
            'view': ''
        }
    }
}
