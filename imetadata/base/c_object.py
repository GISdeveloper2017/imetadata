#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/13 14:09 
# @Author : 王西亚 
# @File : c_object.py

import importlib
import os

from imetadata.base.Exceptions import BusinessNotExistException
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


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
    def create_plugins_instance(cls, package_root_name, package_name, file_info_ex) -> CPlugins:
        package_full_name = '{0}.{1}'.format(package_root_name, package_name)
        package_obj = importlib.import_module(package_full_name)
        class_meta = getattr(package_obj, package_name)
        class_meta_one = class_meta
        obj = class_meta_one(file_info_ex)
        return obj
