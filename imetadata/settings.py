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
. data2service: 服务发布配置
. metadata: 数管.元数据管理
    . directory: 目录
        . view: 数管的快视图存储的目录
"""
from imetadata.base.c_settings import CSettings

application = CSettings(
    {
        'application': {
            'debug': -1,
            'directory': '',
            'name': ''
        },
        'databases': [
            {
                'id': '0',
                'type': 'postgresql',
                'host': '127.0.0.1',
                'port': '5432',
                'database': 'atplatform4',
                'username': 'postgres',
                'password': 'postgres'
            }
        ],
        'spatial': {
            'srid': 4326
        },
        'directory': {
            'work': '/Users/wangxiya/Documents/我的测试数据/90.工作',
            'test': {
                'data': '/Users/wangxiya/Documents/我的测试数据/31.混合存储/数据测试'
            }
        },
        'data2service': {
            'local_dir': '/home/geocube/local',
            "update_cache": "mapproxy-seed  -f  $yaml_file$  -s  $seed_yaml$  -c  20 -q",
            "tindex_dir": "F:/work/debug/tileIndex",
            "map_dir": "F:/work/debug/tileIndex",
            "yaml_dir": "F:/work/debug/tileIndex",
            "seed_dir": "F:/work/debug/tileIndex",
            "wsgi_dir": "F:/work/debug/tileIndex",
            "conf_dir": "F:/work/debug/tileIndex",
            "service_yaml": {
                "server_bin": "F:/work/debug/tileIndex",
                "server_dir": "F:/work/debug/tileIndex",
                "cache_dir": "F:/work/debug/tileIndex/service_cache_$orderid$"
            },
            "seed_yaml": {
                "min_level": "1",
                "max_level": "18",
                "refresh_time": "2030-9-25T22:55:00",
                "coverages": "  $kid$:\n    bbox: [$seed_bbox$]\n    srs: \"EPSG:4326\"\n"
            },
            "qld_conf": {
                "conf_path": "F:/work/debug/tileIndex/geocube.conf",
                "wsgi_script": "WSGIScriptAlias /$aliasname$ $wsgi_file$"
            },
            "multiapp": "true"
        },
        'metadata': {
            'title': '数管配置',
            'directory': {
                'title': '数管常规目录设置, 包括元数据存储目录',
                'view': '/Users/wangxiya/Documents/我的测试数据/80.快视图'
            },
            'tags': {
                'rule': [
                    {
                        'catalog': 'select gdtid AS id, gdttitle AS title, gdtquickcode AS quickcode FROM ro_global_dim_time where gdtparentid <> \'-1\'',
                        'tag': 'id',
                        'keyword': ['title', 'quickcode'],
                        'data_sample': 'relation_main_name',
                        'separator': ['\\', '_', '/', '-', ' ', '+']
                    },
                    {
                        'catalog': 'SELECT gdsid AS ID, gdstitle AS title, gdsquickcode AS quickcode FROM ro_global_dim_space',
                        'tag': 'id',
                        'keyword': ['title', 'quickcode'],
                        'data_sample': 'relation_main_name',
                        'separator': ['\\', '_', '/', '-', ' ', '+'],
                        'enable': False
                    },
                    {
                        'catalog': 'SELECT gdcbid AS ID, gdcbtitle AS title, gdcbquickcode as quickcode FROM ro_global_dim_custom_bus',
                        'tag': 'id',
                        'keyword': ['title', 'quickcode'],
                        'data_sample': 'relation_main_name',
                        'separator': ['\\', '_', '/', '-', ' ', '+']
                    },
                    {
                        'catalog': 'SELECT gdcid AS ID, gdctitle AS title FROM ro_global_dim_custom',
                        'tag': 'id',
                        'keyword': ['title'],
                        'data_sample': 'relation_main_name',
                        'separator': ['\\', '_', '/', '-', ' ', '+']
                    }
                ]
            },
            'plugins': {
                'title': '特殊目录下的文件识别配置',
                'dir': [
                    {
                        'plugin': [
                            'plugins_9001_busdataset_dom',
                            'plugins_8000_dom_10',
                            'plugins_8001_dom_10_dom',
                            'plugins_8002_dom_12',
                            'plugins_8003_dom_12_dom',
                            'plugins_8004_dom_part_2'
                        ],
                        'keyword': 'dom'
                    },
                    {
                        'plugin': [
                            'plugins_9002_busdataset_dem',
                            'plugins_8010_dem_10',
                            'plugins_8011_dem_10_dem',
                            'plugins_8012_dem_12',
                            'plugins_8013_dem_12_dem',
                            'plugins_8014_dem_part_2',
                            'plugins_8015_dem_noframe'
                        ],
                        'keyword': 'dem'
                    },
                    {
                        'plugin': [
                            'plugins_9003_busdataset_ortho',
                            'plugins_8020_ortho'
                        ],
                        'keyword': '单景正射'
                    },
                    {
                        'plugin': [
                            'plugins_9004_busdataset_mosaic',
                            'plugins_8030_mosaic'
                        ],
                        'keyword': '镶嵌影像'
                    },
                    {
                        'plugin': [
                            'plugins_9005_busdataset_third_survey',
                            'plugins_8040_third_survey_block',
                            'plugins_8041_third_survey_noblock'
                        ],
                        'keyword': '三调影像'
                    },
                    {
                        'plugin': [
                            'plugins_9006_busdataset_guoqing',
                            'plugins_8050_guoqing_scene_noblock',
                            'plugins_8051_guoqing_scene_block',
                            'plugins_8052_guoqing_frame'
                        ],
                        'keyword': '国情影像'
                    },
                    {
                        'plugin': [
                            'plugins_9007_busdataset_custom',
                            'plugins_8060_custom'
                        ],
                        'keyword': '自定义影像'
                    }
                ]
            },
            'qi': {
                'title': 'quality inspection 质量检验',
                'switch': {
                    'title': '开关配置',
                    'title_inbound_after_qi_immediately': '开关-提交质检后, 系统不论质检是否有无有问题的数据, 都自动入库',
                    'inbound_after_qi_immediately': 'off'
                }
            },
            'inbound': {
                'title': '入库配置',
                'schema': {
                    'special': [
                        {'id': 'dem', 'title': 'DOM数据集', 'storage': {'type': 'set', 'id': '01'}, 'path': '/${batch_id}'}
                    ],
                    'default': {
                        'id': 'other', 'title': '零散数据', 'storage': {'type': 'auto'}, 'path': '/${batch_id}'
                    }
                },
                'ignore': {
                    'title': '入库需要忽略的文件或目录',
                    'file': ['.DS_Store', 'ready.21at', 'metadata.21at'],
                    'dir': ['.git']
                },
                'switch': {
                    'title': '开关配置',
                    'title_use_ready_flag_file_name': '开关-使用ready.21at标识文件判断一个目录是否可以入库',
                    'use_ready_flag_file_name': 'off'
                }
            },
            'outbound': {
                'title': '出库配置'
            },
            'stocktaking': {
                'title': '盘点配置'
            }
        },
        'dependence': {
            'arcpy': {
                'title': '依赖arcpy, 系统可以对元数据进行更加详细的提取, 支持对gdb,mdb等空间数据图层的别名的解析, 并进行业务标签的自动归类, enable设置为False, 表示无法依赖该工具, 系统将仅仅支持图层名称的解析, 不支持别名',
                'enable': False,
                'python_dir': None,
                'version': 10.1
            },
            'tika': {
                'title': '依赖tika, 系统可以对常用的文档进行元数据解析, enable设置为False, 表示无法依赖该工具, 文档的元数据将无法提取, 保持为空',
                'enable': True,
                'mode': 'server',
                'mode_title': '模式可以设置为client/server, server表示使用tika的rest server进行解析, client表示使用客户端app进行解析, 使用何种方式, 必须进一步配置server和client属性',
                'server': {
                    'url': 'http://localhost:9998/tika'
                },
                'client': {
                    'application': '/usr/local/Cellar/tika/1.24.1_1/libexec/tika-app-1.24.1.jar'
                }
            }
        }
    }
)
