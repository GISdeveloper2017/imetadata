# -*- coding: utf-8 -*- 
# @Time : 2020/9/16 19:41
# @Author : 赵宇飞
# @File : c_dbBusJob.py

from __future__ import absolute_import

from abc import ABC
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_object import CObject
from imetadata.base.c_resource import CResource
from imetadata.base.c_sys import CSys
from imetadata.base.core.Exceptions import DBException
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.base.c_plugins import CPlugins
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_dbQueueJob import CDBQueueJob
from imetadata.base.c_logger import CLogger


class CDBBusJob(CDBQueueJob):
    '''
      数据库操作的业务类，如根据objectid删除对象数据，根据directoryid删除目录id对应的数据记录
    '''

    def delete_by_directoryid(self, directory_id):
        '''
          根据目录id删除dm2_storage_directory的数据库记录

        :param directoryid:
        :return:
        '''
        pass

    def delete_by_fileid(self, file_id):
        '''
          根据文件id删除dm2_storage_file数据库记录

        :param file_id:
        :return:
        '''
        pass

    def delete_object_by_objectid(self, objectid):
        '''
          根据对象id删除数据库记录，包含object表，detail表

        :param objectid:
        :return:
        '''
        pass

    def delete_object_by_directoryid(self, directoryid):
        '''
        根据目录id删除数据记录，不包含子目录  ，包含directory表，file表，object表，detail表

        :param directoryid:
        :return:
        '''
        pass

    def delete_object_by_directoryid_with_dirchild(self, directoryid):
        '''
        根据目录id删除数据记录,包含子目录 ，包含directory表，file表，object表，detail表

        :param directoryid:
        :return:
        '''
        pass

    def clear_data_no_valid(self):
        '''
        清除垃圾 ，包含directory表，file表，object表，detail表

        :return:
        '''
        pass

