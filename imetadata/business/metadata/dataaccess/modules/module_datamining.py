# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:58 
# @Author : 王西亚 
# @File : module_distribution.py
from imetadata.base.c_result import CResult
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule


class module_datamining(CDAModule):
    """
    数据挖掘模块对数管编目的质检要求
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据分析挖掘'
        info[self.Name_Enable] = False

        return info

    def access(self, obj_id, obj_name, obj_type, quality) -> str:
        """
        解析数管中识别出的对象, 与第三方模块的访问能力, 在本方法中进行处理
        返回的json格式字符串中, 是默认的CResult格式, 但是在其中还增加了Access属性, 通过它反馈当前对象是否满足第三方模块的应用要求
        注意: 一定要反馈Access属性
        :return:
        """
        result = super().access(obj_id, obj_name, obj_type, quality)
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Wait)
