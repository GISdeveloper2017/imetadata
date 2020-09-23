# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 20:56 
# @Author : 王西亚 
# @File : c_pluginsMng.py

from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_logger import CLogger
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CPluginsMng(CResource):
    @classmethod
    def plugins_classified(cls, file_info: CFileInfoEx) -> CPlugins:
        target = file_info.__file_main_name__
        target_type = file_info.__file_type__
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_list = CFile.search_file_or_subpath_of_path(path,
                                                                 '{0}_*.{1}'.format(cls.Name_Plugins, cls.FileExt_Py))
        for file_name_with_path in plugins_file_list:
            file_main_name = CFile.file_main_name(file_name_with_path)
            try:
                class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name, file_info)
                object_confirm, object_name = class_classified_obj.classified()
                if object_confirm != cls.Object_Confirm_IUnKnown:
                    CLogger().debug(
                        '{0} is classified as {1}.{2}'.format(target, class_classified_obj.get_information(),
                                                                      class_classified_obj.get_id()))
                    return class_classified_obj
            except:
                CLogger().debug('插件[{0}]解析出现异常, 请检查!'.format(file_main_name))
                continue
        else:
            return None

    @classmethod
    def plugins(cls, file_info: CFileInfoEx, plugins_id: str) -> CPlugins:
        target_type = file_info.__file_type__
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, plugins_id, file_info)
        return class_classified_obj
