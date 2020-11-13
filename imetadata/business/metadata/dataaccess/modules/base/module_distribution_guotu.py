# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : module_distribution_guotu.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule


class module_distribution_guotu(CDAModule):
    """
    国土即时服务的基础类
    """
    _dict_sync = {}  # 构建通用sql的字段结果值，在_before_sync中处理获取

    def access(self) -> str:
        self._before_access()
        result_do = self._do_access()
        return result_do
        # if not CResult.result_success(result_do):
        #     return result_do
        # return CResult.merge_result_info(result_do, self.Name_Access, self.DataAccess_Forbid)
        # return CResult.merge_result_info(result_do, self.Name_Access, self.DataAccess_Pass)

    def _before_access(self):
        pass

    def _do_access(self) -> str:
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
        self._before_sync()
        result_do = self._do_sync()
        return result_do

    def _before_sync(self):
        pass

    def _do_sync(self) -> str:
        return CResult.merge_result(
            self.Success,
            '对象[{0}]的同步机制无效, 第三方系统将自行从数据中心提取最新数据! '.format(self._obj_name)
        )
