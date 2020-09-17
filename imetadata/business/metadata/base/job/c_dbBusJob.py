# -*- coding: utf-8 -*- 
# @Time : 2020/9/16 19:41
# @Author : 赵宇飞
# @File : c_dbBusJob.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob


class CDBBusJob(CDMBaseJob):
    """
    数据库操作的业务类，如根据objectid删除对象数据，根据directoryid删除目录id对应的数据记录
    """

    def delete_by_directoryid(self, directory_id):
        """
          根据目录id删除dm2_storage_directory的数据库记录

        :param directory_id:
        :return:
        """
        pass

    def delete_by_fileid(self, file_id):
        """
          根据文件id删除dm2_storage_file数据库记录

        :param file_id:
        :return:
        """
        pass

    def delete_object_by_objectid(self, objectid):
        """
          根据对象id删除数据库记录，包含object表，detail表

        :param objectid:
        :return:
        """
        pass

    def delete_object_by_directoryid(self, directoryid):
        """
        根据目录id删除数据记录，不包含子目录  ，包含directory表，file表，object表，detail表

        :param directoryid:
        :return:
        """
        pass

    def delete_object_by_directoryid_with_dirchild(self, directoryid):
        """
        根据目录id删除数据记录,包含子目录 ，包含directory表，file表，object表，detail表

        :param directoryid:
        :return:
        """
        pass

    def clear_data_no_valid(self):
        """
        清除垃圾 ，包含directory表，file表，object表，detail表

        :return:
        """
        pass

    def bus_white_black_valid(self, ds_path_with_relation_path, ds_storage_option, is_dir: bool):
        """
        检查指定文件是否符合白名单, 黑名单验证
        """
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
