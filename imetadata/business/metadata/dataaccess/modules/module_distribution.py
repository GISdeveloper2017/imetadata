# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:58 
# @Author : 王西亚 
# @File : module_distribution.py
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule


class module_distribution(CDAModule):
    def access(self) -> str:
        return super().access()

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据检索分发'

        return info
