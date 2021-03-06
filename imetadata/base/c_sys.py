#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import platform
import sys

import settings
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils


class CSys(CResource):
    def __init__(self):
        pass

    @classmethod
    def get_platform_system_name(cls):
        return platform.system()

    @classmethod
    def get_project_dir(cls):
        return settings.application.xpath_one(cls.Path_Setting_Application_Dir, '')

    @classmethod
    def get_application_name(cls):
        return settings.application.xpath_one(cls.Path_Setting_Application_Name, '')

    @classmethod
    def get_imetadata_dir(cls):
        return os.path.join(cls.get_project_dir(), cls.Name_IMetaData)

    @classmethod
    def get_application_package_name(cls):
        return cls.Name_IMetaData

    @classmethod
    def get_job_root_dir(cls):
        return os.path.join(cls.get_imetadata_dir(), cls.NAME_JOB)

    @classmethod
    def get_job_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_application_package_name(), cls.NAME_JOB)

    @classmethod
    def get_execute_filename(cls):
        return sys.executable

    @classmethod
    def get_execute_process_id(cls):
        return os.getpid()

    @classmethod
    def get_os_name(cls):
        return os.name

    @classmethod
    def get_business_root_dir(cls):
        return os.path.join(cls.get_imetadata_dir(), cls.Name_Business)

    @classmethod
    def get_business_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_application_package_name(), cls.Name_Business)

    @classmethod
    def get_metadata_root_dir(cls):
        return os.path.join(cls.get_business_root_dir(), cls.Name_MetaData)

    @classmethod
    def get_inbound_root_dir(cls):
        return os.path.join(cls.get_metadata_root_dir(), cls.Name_InBound)

    @classmethod
    def get_dataaccess_root_dir(cls):
        return os.path.join(cls.get_metadata_root_dir(), cls.Name_DataAccess)

    @classmethod
    def get_metadata_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_business_package_root_name(), cls.Name_MetaData)

    @classmethod
    def get_inbound_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_metadata_package_root_name(), cls.Name_InBound)

    @classmethod
    def get_dataaccess_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_metadata_package_root_name(), cls.Name_DataAccess)

    @classmethod
    def get_plugins_root_dir(cls):
        return os.path.join(cls.get_inbound_root_dir(), cls.Name_Plugins)

    @classmethod
    def get_plugins_package_root_name(cls):
        return '{0}.{1}'.format(cls.get_inbound_package_root_name(), cls.Name_Plugins)

    @classmethod
    def get_work_root_dir(cls):
        rt_path = settings.application.xpath_one(cls.Path_Setting_Dir_WorkDir, None)
        if CUtils.equal_ignore_case(CUtils.any_2_str(rt_path), ''):
            rt_path = os.path.join(cls.get_project_dir(), cls.Name_Work)

        return rt_path

    @classmethod
    def get_metadata_view_root_dir(cls):
        rt_path = settings.application.xpath_one(cls.Path_Setting_MetaData_Dir_View, None)
        if CUtils.equal_ignore_case(CUtils.any_2_str(rt_path), ''):
            rt_path = os.path.join(cls.get_project_dir(), cls.Name_View)

        return rt_path

    @classmethod
    def get_no_inbound_root_dir(cls):
        rt_path = settings.application.xpath_one(cls.Path_Setting_Dir_NoInboundDir, None)
        if CUtils.equal_ignore_case(CUtils.any_2_str(rt_path), ''):
            rt_path = os.path.join(cls.get_project_dir(), cls.Name_NoInbound)

        return rt_path

    @classmethod
    def get_metadata_data_access_modules_root_dir(cls):
        return os.path.join(cls.get_dataaccess_root_dir(), cls.Name_Modules)

    @classmethod
    def get_metadata_data_access_modules_root_name(cls):
        return '{0}.{1}'.format(cls.get_dataaccess_package_root_name(), cls.Name_Modules)
