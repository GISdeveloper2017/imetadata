# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:45 
# @Author : 王西亚 
# @File : c_dmPathInfo.py

from imetadata.business.metadata.base.job.c_dmFilePathInfoEx import CDMFilePathInfoEx


class CDMPathInfo(CDMFilePathInfoEx):
    def __init__(self, file_name_with_full_path, root_path, storage_id, path_id):
        """

        :param file_name_with_full_path:
        :param root_path:
        :param storage_id: 必须提供
        :param path_id:
            如果为None, 则首先根据文件相对路径和storage_id, 查找数据库中登记的标识, 如果不存在, 则自行创建uuid;
            如果不为空, 则表明数据库中已经存储该文件标识
        """
        super().__init__(file_name_with_full_path, root_path)
        self.__db_existed__ = False

    def update_db(self):
        pass
