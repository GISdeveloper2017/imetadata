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
        'work': '/Users/wangxiya/Documents/交换/9.数管/9.工作目录'
    },
    'metadata': {
        'directory': {
            'view': '/Users/wangxiya/Documents/交换/9.数管/0.编目'
        },
        'plugins': {
            'dir': [
                {'plugin': ['plugins_1000_dom_10', 'plugins_1002_dom_12'], 'keyword': 'dom'},
                {'plugin': ['plugins_1010_dem_10', 'plugins_1010_dem_12'], 'keyword': 'dem'}
            ]
        }
    }
}
