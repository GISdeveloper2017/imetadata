# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:58 
# @Author : 王西亚 
# @File : module_distribution.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule


class module_datamining(CDAModule):
    def access(self) -> str:
        result = super().access()
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Wait)

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据分析挖掘'

        return info
