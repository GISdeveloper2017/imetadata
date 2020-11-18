# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : distribution_guotu.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base
from imetadata.database.c_factory import CFactory


class distribution_guotu(distribution_base):
    """
    国土即时服务的基础类
    """
    _dict_sync = {}  # 构建通用sql的字段结果值，在_before_sync中处理获取

    def information(self) -> dict:
        info = super().information()
        info['table_name'] = 'ap3_product_rsp'
        return info

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
        sql_all_archived = ''
        table_name = CUtils.dict_value_by_name(self.information(), 'table_name', 'ap3_product_rsp')
        sql_check = '''
        select aprid from {0} where aprid='{1}'
        '''.format(table_name, self._obj_id)
        record_cheak = CFactory().give_me_db(self._db_id).one_row(sql_check).size()  # 查找记录数
        if record_cheak == 0:
            sql_temporary_1 = ''
            sql_temporary_2 = ''
            for column_name, column_value in self.get_sync_dict().items():
                sql_temporary_1 = sql_temporary_1 + ",{0}".format(column_name)
                sql_temporary_2 = sql_temporary_2 + ",{0}".format(column_value)
            sql_all_archived = '''
            INSERT INTO {0}(aprid{2}) VALUES ('{1}'{3})
            '''.format(table_name, self._obj_id, sql_temporary_1, sql_temporary_2)
        else:
            sql_temporary = ''
            for column_name, column_value in self.get_sync_dict().items():
                sql_temporary = sql_temporary + "{0}={1},".format(column_name, column_value)
            sql_temporary = sql_temporary[:-1]
            sql_all_archived = '''
            UPDATE {0} SET {2} WHERE aprid='{1}'
            '''.format(table_name, self._obj_id, sql_temporary)

        if CFactory().give_me_db(self._db_id).execute(sql_all_archived):
            return CResult.merge_result(
                self.Success,
                '对象[{0}]的同步成功! '.format(self._obj_name)
            )
        else:
            return CResult.merge_result(
                self.Failure,
                '对象[{0}]的同步错误!,请检查配置.'.format(self._obj_name)
            )

    def get_sync_dict(self) -> dict:
        """
        本方法的写法为强规则，字典key为字段名，字典value为对应的值或者sql语句，在写时需要加语句号，子查询语句加(),值加‘’
        子查询：sync_dict['字段名']=“(select 字段 from 表 where id=‘1’)”
        值：sync_dict['字段名']=“‘值’”
        同时，配置插件方法时请在information()方法中添加info['table_name'] = '表名'的字段
        """
        sync_dict = dict()
        return sync_dict
