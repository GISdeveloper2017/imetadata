# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:31 
# @Author : 王西亚 
# @File : init.py.py

import argparse
import logging

import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory


class CApplicationInit(CResource):
    def register_dm_metadata_plugins(self):
        sql_register_dm_metadata_plugins_clear = '''
        truncate table dm2_storage_object_def cascade
        '''

        sql_unregister_dm_metadata_plugins = '''
        delete from dm2_storage_object_def where dsodid = :dsodid
        '''
        sql_register_dm_metadata_plugins = '''
        insert into dm2_storage_object_def(
            dsodid, dsodtitle, dsodtype, dsodtypetitle, dsodtypecode, dsodgroup, dsodgrouptitle, 
            dsodcatalog, dsodcatalogtitle, dsod_isspace, dsod_isdataset) 
            values (:dsodid, :dsodtitle, :dsodtype, :dsodtypetitle, :dsodtypecode, :dsodgroup, :dsodgrouptitle, 
            :dsodcatalog, :dsodcatalogtitle, :dsod_isspace, :dsod_isdataset) 
        '''

        CFactory().give_me_db().execute(sql_register_dm_metadata_plugins_clear)

        plugins_root_dir = CSys.get_plugins_root_dir()
        plugins_type_list = CFile.file_or_subpath_of_path(plugins_root_dir)
        for plugins_type in plugins_type_list:
            if CFile.is_dir(CFile.join_file(plugins_root_dir, plugins_type)) and (
                    not (str(plugins_type)).startswith('_')):
                plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), plugins_type)
                path = CFile.join_file(CSys.get_plugins_root_dir(), plugins_type)
                plugins_file_list = CFile.file_or_subpath_of_path(path, '{0}_*.{1}'.format(self.Name_Plugins,
                                                                                           self.FileExt_Py))
                for file_name_without_path in plugins_file_list:
                    file_main_name = CFile.file_main_name(file_name_without_path)
                    class_classified_obj = CObject.create_plugins_instance(
                        plugins_root_package_name,
                        file_main_name,
                        None
                    )
                    plugins_info = class_classified_obj.get_information()
                    print('{0}/{1}:{2}'.format(plugins_type, file_main_name, plugins_info))

                    CFactory().give_me_db().execute(sql_unregister_dm_metadata_plugins, plugins_info)
                    CFactory().give_me_db().execute(sql_register_dm_metadata_plugins, plugins_info)

    def register_dm_modules(self):
        sql_register_dm_metadata_modules_clear = '''
        truncate table dm2_modules cascade
        '''

        sql_register_dm_metadata_modules = '''
        insert into dm2_modules(dmid, dmtitle) 
            values (:dmid, :dmtitle) 
        '''

        CFactory().give_me_db().execute(sql_register_dm_metadata_modules_clear)

        modules_root_dir = CSys.get_metadata_data_access_modules_root_dir()
        module_file_name_list = CFile.file_or_subpath_of_path(modules_root_dir, '*.{0}'.format(self.FileExt_Py))
        for module_file_name in module_file_name_list:
            if CFile.is_file(CFile.join_file(modules_root_dir, module_file_name)) and (
                    not (str(module_file_name)).startswith('_')):
                module_name = CFile.file_main_name(module_file_name)
                module_obj = CObject.create_module_instance(
                    CSys.get_metadata_data_access_modules_root_name(),
                    module_name,
                    CResource.DB_Server_ID_Default,
                    '',
                    '',
                    '',
                    None
                )
                module_info = module_obj.information()
                CFactory().give_me_db().execute(
                    sql_register_dm_metadata_modules,
                    {
                        'dmid': module_name,
                        'dmtitle': CUtils.dict_value_by_name(module_info, CResource.Name_Title, module_name)
                    }
                )

    def register_dm_metadata_quality_group(self):
        sql_register_dm_metadata_modules_clear = '''
        truncate table dm2_quality_group cascade
        '''

        sql_register_dm_metadata_modules = '''
        insert into dm2_quality_group(dqgid, dqgtitle) 
            values (:dqgid, :dqgtitle) 
        '''

        CFactory().give_me_db().execute_batch(
            [
                (sql_register_dm_metadata_modules_clear, None),
                (sql_register_dm_metadata_modules, {'dqgid': CResource.QA_Group_Data_Integrity, 'dqgtitle': '数据完整性'})
            ]
        )


def start_init():
    application_init = CApplicationInit()
    application_init.register_dm_metadata_plugins()
    application_init.register_dm_modules()
    application_init.register_dm_metadata_quality_group()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""
初始化
作者：王西亚
日期：2020-09-19

算法:
.系统根据内置的业务插件, 自动初始化数据表dm2_storage_object_def

    """)
    parser.add_argument('-log', '--log_filepath', required=False, help='Log文件名', dest='log_filepath')

    args = parser.parse_args()

    if args.log_filepath is not None:
        logging.basicConfig(filename=args.log_filepath + '/init.log', level=logging.ERROR,
                            format="%(levelname)s - %(asctime)s - %(message)s",
                            datefmt="%m/%d/%Y %H:%M:%S %p")

    CLogger().info('开始初始化工作...')
    application_dir = CFile.file_path(CFile.file_abs_path(__file__))
    application_name = CFile.file_main_name(application_dir)
    settings.application.set_app_information(application_dir, application_name)
    start_init()
    CLogger().info('初始化工作已经成功完成...')

    # print(__file__)
    # application_dir = CFile.file_path(CFile.file_abs_path(__file__))
    # application_name = CFile.file_main_name(application_dir)
    # settings.application.set_app_information(application_dir, application_name)
    # print('*' * 15)
    # print(CSys.get_execute_filename())
    # print(CSys.get_project_dir())
    # print(CSys.get_application_name())
    # print('*' * 15)
    # print(CSys.get_imetadata_dir())
    # print(CSys.get_job_root_dir())
    # print(CSys.get_business_root_dir())
    # print(CSys.get_metadata_root_dir())
    # print(CSys.get_inbound_root_dir())
    # print(CSys.get_plugins_root_dir())
    # print(CSys.get_dataaccess_root_dir())
    # print(CSys.get_metadata_data_access_modules_root_dir())
    # print('*' * 15)
    # print(CSys.get_work_root_dir())
    # print(CSys.get_metadata_view_root_dir())
    # print('*' * 15)
    # print(CSys.get_application_package_name())
    # print(CSys.get_job_package_root_name())
    # print(CSys.get_business_package_root_name())
    # print(CSys.get_metadata_package_root_name())
    # print(CSys.get_inbound_package_root_name())
    # print(CSys.get_plugins_package_root_name())
    # print(CSys.get_dataaccess_package_root_name())
    # print(CSys.get_metadata_data_access_modules_root_name())
