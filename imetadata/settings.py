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
                {'plugin': ['plugins_1000_dom_10', 'plugins_1001_dom_10_dom', 'plugins_1002_dom_12',
                            'plugins_1003_dom_12_dom', 'plugins_1004_dom_part_2'], 'keyword': 'dom'},
                {'plugin': ['plugins_1010_dem_10', 'plugins_1011_dem_10_dem', 'plugins_1012_dem_12',
                            'plugins_1013_dem_12_dem', 'plugins_1014_dem_part_2', 'plugins_1015_dem_noframe'],
                 'keyword': 'dem'},
                {'plugin': ['plugins_1020_ortho'], 'keyword': '单景正射'},
                {'plugin': ['plugins_1030_mosaic'], 'keyword': '镶嵌影像'},
                {'plugin': ['plugins_1040_third_survey_block', 'plugins_1041_third_survey_noblock'], 'keyword': '三调影像'}
            ]
        }
    }
}
