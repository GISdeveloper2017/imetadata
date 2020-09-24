# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:31 
# @Author : 王西亚 
# @File : init.py.py

import argparse
import logging

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys


class CApplicationInit(CResource):
    def register_dm_metadata_plugins_2_dm2_storage_object_def(self):
        sql_register_dm_metadata_plugins_clear = '''
        delete from dm2_storage_object_def
        '''

        sql_register_dm_metadata_plugins = '''
        insert into dm2_storage_object_def(dsodid, dsodname, dsodtitle, dsodtype, dsod_metadata_engine, dsod_detail_engine, dsod_tags_engine, dsod_ext_whitelist, dsod_browserimg, dsod_thumbimg, dsod_check_engine_type, dsod_check_engine, dsod_check_engine_workdir, dsod_deploy_engine_type, dsod_deploy_engine, dsod_deploy_engine_workdir, dsodtype_title, dsodcode, dsocatalog) 
        '''

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
                    class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name,
                                                                           None)
                    print('{0}/{1}:{2}'.format(plugins_type, file_main_name, class_classified_obj.get_information()))


def start_init():
    application_init = CApplicationInit()
    application_init.register_dm_metadata_plugins_2_dm2_storage_object_def()


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
    start_init()
    CLogger().info('初始化工作已经成功完成...')
