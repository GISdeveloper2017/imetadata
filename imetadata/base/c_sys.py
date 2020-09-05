#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys


class CSys:
    def __init__(self):
        pass

    @classmethod
    def get_application_dir(cls):
        return os.path.abspath('.')

    @classmethod
    def get_job_root_dir(cls):
        return os.path.join(cls.get_application_dir(), 'job')

    @classmethod
    def get_job_package_root_name(cls):
        return 'imetadata.job'

    @classmethod
    def get_execute_filename(cls):
        return sys.executable

    @classmethod
    def get_execute_process_id(cls):
        return os.getpid()

    @classmethod
    def get_execute_os_name(cls):
        return os.name
