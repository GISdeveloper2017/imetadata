#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/13 14:09 
# @Author : 王西亚 
# @File : c_object.py

import importlib
import sys
import os
from imetadata.base.c_file import CFile
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CMetaDataUtils

sys.path.append(...)


class CObject:
    def __init__(self):
        pass

    @classmethod
    def create_business_instance(cls, package_dir, package_name, class_name, *args, **kwargs):
        dir_list = os.listdir(package_dir)
        for cur_file in dir_list:
            if not CMetaDataUtils.equal_ignore_case(CFile.file_main_name(cur_file), class_name):
                continue

            path = os.path.join(package_dir, cur_file)
            if os.path.isfile(path) and (not cur_file.startswith('__init__')):
                package_name = '{0}.{1}'.format(package_name, class_name)
                package_obj = importlib.import_module(package_name)
                class_meta = getattr(package_obj, class_name)
                class_meta_one = class_meta
                obj_id = args[0]
                obj = class_meta_one(obj_id)
                return obj

