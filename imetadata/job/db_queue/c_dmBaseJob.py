# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 11:41 
# @Author : 王西亚 
# @File : c_dmBaseJob.py

from __future__ import absolute_import

from abc import ABC
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.core.Exceptions import DBException
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob
from imetadata.base.c_logger import CLogger


class CDMBaseJob(CDBQueueJob):
    def bus_white_black_valid(self, ds_path_with_relation_path, ds_storage_option, is_dir: bool):
        if ds_storage_option == '' or ds_storage_option is None:
            return True

        dir_filter_white_list = CJson.json_attr_value(ds_storage_option,
                                                      CJson.json_join(self.Name_Filter, self.Name_Directory,
                                                                      self.Name_White_List), '')
        dir_filter_black_list = CJson.json_attr_value(ds_storage_option,
                                                      CJson.json_join(self.Name_Filter, self.Name_Directory,
                                                                      self.Name_Black_List), '')
        file_filter_white_list = CJson.json_attr_value(ds_storage_option,
                                                       CJson.json_join(self.Name_Filter, self.Name_File,
                                                                       self.Name_White_List), '')
        file_filter_black_list = CJson.json_attr_value(ds_storage_option,
                                                       CJson.json_join(self.Name_Filter, self.Name_File,
                                                                       self.Name_Black_List), '')

        if is_dir:
            if (dir_filter_white_list != '') and (dir_filter_black_list != ''):
                return CFile.file_match(ds_path_with_relation_path, dir_filter_white_list) and (
                    not CFile.file_match(ds_path_with_relation_path, dir_filter_black_list))
            elif dir_filter_white_list != '':
                return CFile.file_match(ds_path_with_relation_path, dir_filter_white_list)
            elif dir_filter_black_list != '':
                return not CFile.file_match(ds_path_with_relation_path, dir_filter_black_list)
            else:
                return True
        else:
            if (file_filter_white_list != '') and (file_filter_black_list != ''):
                return CFile.file_match(ds_path_with_relation_path, file_filter_white_list) and (
                    not CFile.file_match(ds_path_with_relation_path, file_filter_black_list))
            elif file_filter_white_list != '':
                return CFile.file_match(ds_path_with_relation_path, file_filter_white_list)
            elif file_filter_black_list != '':
                return not CFile.file_match(ds_path_with_relation_path, file_filter_black_list)
            else:
                return True
