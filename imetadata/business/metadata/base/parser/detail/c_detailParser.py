# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 10:33 
# @Author : 王西亚 
# @File : c_detailParser.py
from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils


class CDetailParser(CResource):
    __db_server_id__ = None
    __object_id__ = None
    __file_info__: CFileInfoEx = None

    __detail_file_path__: str
    __detail_file_match_text__: str
    __detail_file_match_type__: int = CFile.MatchType_Common
    __detail_file_recurse__: bool = False

    def __init__(self, db_server_id: str, object_id: str, file_info: CFileInfoEx):
        self.__db_server_id__ = db_server_id
        self.__object_id__ = object_id
        self.__file_info__ = file_info
        self.custom_init()

    def process(self) -> str:
        """
        在这里处理将__file_info__中记录的对象所对应的文件或目录信息, 根据__detail_*变量的定义, 进行目录扫描, 记录到dm2_storage_object_detail中
        todo 负责人: 赵宇飞  内容:完成文件或子目录的扫描入库dm2_storage_object_detail
        :return:
        """
        if self.__detail_file_path__ == '':
            return CUtils.merge_result(self.Success, '附属目录为空, 表明无需处理附属文件, 处理结束!')

        list_file_name = CFile.file_or_subpath_of_path(self.__detail_file_path__, self.__detail_file_match_text__, self.__detail_file_match_type__)
        for item_file_name_without_path in list_file_name:
            item_file_name_with_path = CFile.join_file(self.__detail_file_path__, item_file_name_without_path)
            if CFile.is_dir(item_file_name_with_path):
                pass

        return CUtils.merge_result(self.Success, '处理完毕!')

    @abstractmethod
    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        __detail_file_path__ = ''
