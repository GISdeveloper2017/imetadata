#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import platform
import sys

from imetadata import settings
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils


class CSys(CResource):
    def __init__(self):
        pass

    @classmethod
    def get_os_name(cls):
        return platform.system()

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
        rt_path = settings.application.xpath_one('{0}.{1}'.format(cls.Name_Directory, cls.Name_Work), None)
        if CUtils.equal_ignore_case(CUtils.any_2_str(rt_path), ''):
            rt_path = os.path.join(cls.get_project_dir(), cls.Name_Work)

        return rt_path

    @classmethod
    def get_metadata_view_root_dir(cls):
        rt_path = settings.application.xpath_one(
            '{0}.{1}.{2}'.format(cls.ModuleName_MetaData, cls.Name_Directory, cls.Name_View),
            None
        )
        if CUtils.equal_ignore_case(CUtils.any_2_str(rt_path), ''):
            rt_path = os.path.join(cls.get_project_dir(), cls.Name_View)

        return rt_path

    @classmethod
    def get_metadata_data_access_modules_root_dir(cls):
        return os.path.join(cls.get_metadata_root_dir(), cls.Name_DataAccess, cls.Name_Modules)

    @classmethod
    def get_metadata_data_access_modules_root_name(cls):
        return '{0}.{1}.{2}'.format(cls.get_metadata_package_root_name(), cls.Name_DataAccess, cls.Name_Modules)


if __name__ == '__main__':
    print(CSys.get_project_dir())
    print(CSys.get_application_dir())
    print(CSys.get_plugins_package_root_name())
    print(CSys.get_plugins_root_dir())
    print(CSys.get_metadata_data_access_modules_root_name())
    print(CSys.get_metadata_data_access_modules_root_dir())
    print(CSys.get_job_package_root_name())
    print(CSys.get_job_root_dir())
    print(CSys.get_work_root_dir())
    print(CSys.get_execute_os_name())
    print(platform.system())

    if (platform.system() == 'Windows'):
        print('Windows系统')
    elif (platform.system() == 'Linux'):
        print('Linux系统')
    else:
        print('其他')
