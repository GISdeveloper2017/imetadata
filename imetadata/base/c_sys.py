#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys

from imetadata.base.c_resource import CResource


class CSys(CResource):
    def __init__(self):
        pass

    @classmethod
    def get_project_dir(cls):
        cur_path = os.path.abspath(os.path.dirname(__file__))
        return cur_path[:cur_path.find(cls.get_application_name()) + len(cls.get_application_name())]

    @classmethod
    def get_application_name(cls):
        return cls.Name_Application

    @classmethod
    def get_application_dir(cls):
        return os.path.join(cls.get_project_dir(), cls.get_application_name())

    @classmethod
    def get_application_package_name(cls):
        return cls.Name_Application

    @classmethod
    def get_job_root_dir(cls):
        return os.path.join(cls.get_application_dir(), cls.NAME_JOB)

    @classmethod
    def get_job_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_application_name(), cls.NAME_JOB)

    @classmethod
    def get_execute_filename(cls):
        return sys.executable

    @classmethod
    def get_execute_process_id(cls):
        return os.getpid()

    @classmethod
    def get_execute_os_name(cls):
        return os.name

    @classmethod
    def get_business_root_dir(cls):
        return os.path.join(cls.get_application_dir(), cls.Name_Business)

    @classmethod
    def get_business_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_application_name(), cls.Name_Business)

    @classmethod
    def get_metadata_root_dir(cls):
        return os.path.join(cls.get_business_root_dir(), cls.Name_MetaData)

    @classmethod
    def get_metadata_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_business_package_root_name(), cls.Name_MetaData)

    @classmethod
    def get_plugins_root_dir(cls):
        return os.path.join(cls.get_metadata_root_dir(), cls.Name_Plugins)

    @classmethod
    def get_plugins_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_metadata_package_root_name(), cls.Name_Plugins)

    @classmethod
    def get_work_root_dir(cls):
        return os.path.join(cls.get_project_dir(), cls.Name_WorkDir)


if __name__ == '__main__':
    print(CSys.get_project_dir())
    print(CSys.get_application_dir())
    print(CSys.get_plugins_package_root_name())
    print(CSys.get_plugins_root_dir())
    print(CSys.get_job_package_root_name())
    print(CSys.get_job_root_dir())
    print(CSys.get_work_root_dir())
