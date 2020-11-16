# -*- coding: utf-8 -*- 
# @Time : 2020/11/16 17:39
# @Author : 赵宇飞
# @File : distribution_base.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.database.base.c_dataset import CDataSet


class distribution_base(CResource):
    _db_id: str
    # _obj_id: str
    # _obj_name: str
    _obj_type: str
    _quality_info: CXml
    _dataset: CDataSet

    def __init__(self, db_id, obj_id, quality, dataset):
        self._db_id = db_id
        self._obj_id = obj_id
        # self._obj_name = obj_name
        # self._obj_type = obj_type
        self._quality_info = quality
        self._dataset = CDataSet

    def information(self) -> dict:
        info = dict()
        info[self.Name_ID] = type(self).__name__
        info[self.Name_Title] = None
        info[self.Name_Type] = None
        return info

    def access(self) -> str:
        """
        解析数管中识别出的对象, 与第三方模块的访问能力, 在本方法中进行处理
        返回的json格式字符串中, 是默认的CResult格式, 但是在其中还增加了Access属性, 通过它反馈当前对象是否满足第三方模块的应用要求
        注意: 一定要反馈Access属性
        :return:
        """
        result = CResult.merge_result(
            self.Success,
            '模块[{0}.{1}]对对象[{2}]的访问能力已经分析完毕!'.format(
                CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                self._obj_name
            )
        )
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)

    def sync(self) -> str:
        """
        处理数管中识别的对象, 与第三方模块的同步
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口

        注意: 在本方法中, 不要用_quality_info属性, 因为外部调用方考虑的效率因素, 没有传入!!!
        :return:
        """
        return CResult.merge_result(
            self.Success,
            '对象[{0}]的同步机制无效, 第三方系统将自行从数据中心提取最新数据! '.format(self._obj_name)
        )