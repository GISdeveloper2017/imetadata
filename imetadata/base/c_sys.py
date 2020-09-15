#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys


class CSys:
    def __init__(self):
        pass

    @classmethod
    def get_application_name(cls):
        return 'imetadata'

    @classmethod
    def get_application_dir(cls):
        cur_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(cur_path[:cur_path.find("imetadata/") + len("imetadata/") - 1], cls.get_application_name())

    @classmethod
    def get_application_package_name(cls):
        return 'imetadata'

    @classmethod
    def get_business_root_dir(cls):
        return os.path.join(cls.get_application_dir(), 'business')

    @classmethod
    def get_business_package_root_name(cls):
        return '{0}.business'.format(cls.get_application_name())

    @classmethod
    def get_plugins_root_dir(cls):
        return os.path.join(cls.get_business_root_dir(), 'plugins')

    @classmethod
    def get_plugins_package_root_name(cls):
        return '{0}.plugins'.format(cls.get_business_package_root_name())

    @classmethod
    def get_job_root_dir(cls):
        return os.path.join(cls.get_application_dir(), 'job')

    @classmethod
    def get_job_package_root_name(cls):
        return '{0}.job'.format(cls.get_application_name())

    @classmethod
    def get_execute_filename(cls):
        return sys.executable

    @classmethod
    def get_execute_process_id(cls):
        return os.getpid()

    @classmethod
    def get_execute_os_name(cls):
        return os.name
