# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:17 
# @Author : 王西亚 
# @File : c_daModule.py
from abc import abstractmethod

from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class CDAModule(CResource):
    __obj_id: str
    __obj_name: str
    __obj_type: str
    __quality_info: CXml

    def __init__(self, obj_id, obj_name, obj_type, quality):
        self.__obj_id = obj_id
        self.__obj_name = obj_name
        self.__obj_type = obj_type
        self.__quality_info = quality

    def information(self) -> dict:
        info = dict()
        info[self.Name_ID] = type(self).__name__
        info[self.Name_Title] = None

        return info

    def access(self) -> str:
        result = CResult.merge_result(
            self.Success,
            '模块[{0}.{1}]对对象[{2}]的访问能力已经分析完毕!'.format(
                CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                self.__obj_name
            )
        )
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)
