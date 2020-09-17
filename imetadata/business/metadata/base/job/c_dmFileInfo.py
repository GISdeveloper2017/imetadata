# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:33 
# @Author : 王西亚 
# @File : c_dmFileInfo.py
from imetadata.business.metadata.base.job.c_dmFilePathInfoEx import CDMFilePathInfoEx


class CDMFileInfo(CDMFilePathInfoEx):
    __db_existed__: bool

    def __init__(self, file_name_with_full_path, root_path, storage_id, file_id):
        super().__init__(file_name_with_full_path, root_path)
        self.__db_existed__ = False

    def update_db(self):
        pass
