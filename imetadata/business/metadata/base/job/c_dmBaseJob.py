# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 11:41 
# @Author : 王西亚 
# @File : c_dmBaseJob.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins
from imetadata.base.c_logger import CLogger
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob


class CDMBaseJob(CDBQueueJob):

    def plugins_classified(self, target: str, target_type: str, target_id: str) -> CPlugins:
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_list = CFile.search_file_or_subpath_of_path(path,
                                                                 '{0}_*.{1}'.format(self.Name_Plugins, self.FileExt_Py))
        for file_name_with_path in plugins_file_list:
            file_main_name = CFile.file_main_name(file_name_with_path)
            class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name,
                                                                   target, target_type, target_id)
            object_confirm, object_name = class_classified_obj.classified()
            if object_confirm != CResource.Object_Confirm_IUnKnown:
                CLogger().debug(
                    '{0} is plugins_classified as {1}.{2}'.format(target, class_classified_obj.get_group_name(),
                                                                  class_classified_obj.get_id()))
                return class_classified_obj
        else:
            return None

    def plugins(self, plugins_id: str, target: str, target_type: str, target_id: str) -> CPlugins:
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), target_type)
        path = CFile.join_file(CSys.get_plugins_root_dir(), target_type)
        plugins_file_list = CFile.search_file_or_subpath_of_path(path,
                                                                 '{0}_*.{1}'.format(self.Name_Plugins, self.FileExt_Py))
        for file_name_with_path in plugins_file_list:
            file_main_name = CFile.file_main_name(file_name_with_path)
            if CMetaDataUtils.plugins_id_by_file_main_name(file_main_name) == plugins_id:
                class_classified_obj = CObject.create_plugins_instance(plugins_root_package_name, file_main_name,
                                                                       target, target_type, target_id)
                return class_classified_obj
        else:
            return None
