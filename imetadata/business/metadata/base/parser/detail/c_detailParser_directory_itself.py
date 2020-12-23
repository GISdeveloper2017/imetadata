# -*- coding: utf-8 -*- 
# @Time : 2020/9/24 10:36 
# @Author : 王西亚 
# @File : c_detailParser_same_file_main_name.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.parser.detail.c_detailParser import CDetailParser


class CDetailParser_Directory_Itself(CDetailParser):
    """
    为解决切片的数据统计问题, 特为切片数据增加本类型
    . dm2_storage_obj_detail中仅仅存储一个目录
    . 系统将统计目录下的子目录个数, 文件个数, 以及文件总容量大小, 存储在这个目录的信息中, 详见字段dodfilecount, doddircount, dodfilesize
    . 注意: 此时dm2_storage_obj_detail.dodfilesize中存储的, 是这个目录下所有文件的大小总和
    """

    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        super().custom_init()
        if CFile.is_file(self.file_info.file_name_with_full_path):
            self.__detail_file_path__ = self.file_info.file_path
        else:
            self.__detail_file_path__ = self.file_info.file_name_with_full_path
        self.__detail_file_recurse__ = True
        self.__detail_file_match_type__ = CFile.MatchType_Common
        self.__detail_file_match_text__ = '*'
        self._only_stat_file = True
