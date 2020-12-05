#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/13 14:09 
# @Author : 王西亚 
# @File : c_object.py

import importlib
import os

from imetadata.base.c_file import CFile
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.exceptions import BusinessNotExistException
# from imetadata.business.metadata.base.plugins.c_plugins import CPlugins   # 在其他模块容易引起（most likely due to a circular import）
from imetadata.database.c_factory import CFactory


class CObject:
    def __init__(self):
        pass

    @classmethod
    def create_job_instance(cls, package_directory, package_root_name, package_subdir, package_name, *args, **kwargs):
        package_root = os.path.join(package_directory, package_subdir)
        dir_list = os.listdir(package_root)
        for cur_file in dir_list:
            if not CUtils.equal_ignore_case(CFile.file_main_name(cur_file), package_name):
                continue

            path = os.path.join(package_root, cur_file)
            if os.path.isfile(path) and (not cur_file.startswith('__init__')):
                package_root_name = '{0}.{1}.{2}'.format(package_root_name, package_subdir, package_name)
                package_obj = importlib.import_module(package_root_name)
                class_meta = getattr(package_obj, package_name)
                class_meta_one = class_meta
                obj_id = args[0]
                obj_params = args[1]
                obj = class_meta_one(obj_id, obj_params)
                return obj
        else:
            raise BusinessNotExistException(package_subdir, package_name)

    @classmethod
    def create_plugins_instance(cls, package_root_name, package_name, file_info_ex):  # -> CPlugins:
        package_full_name = '{0}.{1}'.format(package_root_name, package_name)
        package_obj = importlib.import_module(package_full_name)
        class_meta = getattr(package_obj, package_name)
        class_meta_one = class_meta
        obj = class_meta_one(file_info_ex)
        return obj

    @classmethod
    def create_module_instance(cls, package_root_name, package_name, db_id, obj_id, obj_name, obj_type, quality):
        try:
            package_full_name = '{0}.{1}'.format(package_root_name, package_name)
            package_obj = importlib.import_module(package_full_name)
            class_meta = getattr(package_obj, package_name)
            class_meta_one = class_meta
            obj = class_meta_one(db_id, obj_id, obj_name, obj_type, quality)
            return obj
        except Exception as error:
            print('CObject.create_module_instance():' + error.__str__())
            return None

    @classmethod
    def create_module_distribution_instance(cls, package_root_name, package_name, db_id, obj_id, obj_name,
                                            obj_type_code, quality, dataset):
        """
        同步第三方系统的对象构建
        """
        try:
            package_full_name = '{0}.{1}'.format(package_root_name, package_name)
            package_obj = importlib.import_module(package_full_name)
            class_meta = getattr(package_obj, package_name)
            class_meta_one = class_meta
            obj = class_meta_one(db_id, obj_id, obj_name, obj_type_code, quality, dataset)
            return obj
        except Exception as error:
            print('CObject.create_module_distribution_instance():' + error.__str__())
            return None

    @classmethod
    def get_plugins_instance_by_object_id(cls, db_id, object_id):
        """
        根据对应object_id获取识别的插件对象
        """
        sql_query = '''
            SELECT dsoobjecttype, dsodatatype FROM dm2_storage_object WHERE dsoid = '{0}'
        '''.format(object_id)
        dataset = CFactory().give_me_db(db_id).one_row(sql_query)
        object_plugin_file_main_name = dataset.value_by_name(0, 'dsoobjecttype', '')  # plugins_8000_dom_10
        object_plugin_type = dataset.value_by_name(0, 'dsodatatype', '')  # 数据类型:dir-目录;file-文件

        class_classified_obj_real = None
        # 构建数据对象object对应的识别插件
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), object_plugin_type)
        # 判断插件是否存在
        plugins_root_dir = CSys.get_plugins_root_dir()
        plugins_type_root_dir = CFile.join_file(plugins_root_dir, object_plugin_type)
        plugins_file = CFile.join_file(plugins_type_root_dir, '{0}.py'.format(object_plugin_file_main_name))
        if CFile.file_or_path_exist(plugins_file):
            class_classified_obj = cls.create_plugins_instance(
                plugins_root_package_name,
                object_plugin_file_main_name,
                None
            )
            class_classified_obj_real = class_classified_obj
        return class_classified_obj_real