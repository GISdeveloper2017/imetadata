# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : distribution_guotu.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base
from imetadata.database.c_factory import CFactory
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


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
        try:
            quality_info_xml = self._quality_info  # 获取质检xml
            quality_summary = self._dataset.value_by_name(0, 'dso_quality_summary', '')
            quality_summary_json = CJson()
            quality_summary_json.load_obj(quality_summary)
            access_Wait_flag = self.DB_False  # 定义等待标志，为True则存在检查项目为等待
            access_Forbid_flag = self.DB_False  # 定义禁止标志，为True则存在检查项目为禁止
            message = ''

            # 文件与影像质检部分
            file_qa = quality_summary_json.xpath_one('total', '')
            image_qa = quality_summary_json.xpath_one('metadata.data', '')
            if CUtils.equal_ignore_case(file_qa, self.QA_Result_Pass) \
                    and CUtils.equal_ignore_case(image_qa, self.QA_Result_Pass):
                pass
            elif CUtils.equal_ignore_case(file_qa, self.QA_Result_Warn) \
                    or CUtils.equal_ignore_case(image_qa, self.QA_Result_Warn):
                message = message + '[数据与其相关文件的质检存在warn!请进行检查！]'
                access_Wait_flag = self.DB_True
            else:
                message = message + '[数据与其相关文件的质检存在error!请进行修正！]'
                access_Forbid_flag = self.DB_True

            for qa_name, qa_id in self.access_check_dict().items():  # 循环写好的检查列表
                # qa_id = CUtils.dict_value_by_name(access_check_dict, 'qa_id', '')  # 获取id
                qa_node = quality_info_xml.xpath_one("//item[@id='{0}']".format(qa_id))  # 查询xml中的节点
                if qa_node is not None:
                    node_result = CXml.get_attr(qa_node, self.Name_Result, '', False)  # 获取质检结果
                    if CUtils.equal_ignore_case(node_result, self.QA_Result_Pass):
                        pass
                    elif CUtils.equal_ignore_case(node_result, self.QA_Result_Warn):  # 警告则等待
                        message = message + '[业务元数据的质检中，项目{0}为warn!请进行检查！]'.format(qa_name)
                        access_Wait_flag = self.DB_True
                    else:  # 错误以及其他情况，比如''，或者为其他字段
                        message = message + '[业务元数据的质检中，项目{0}为error!请进行修正！]'.format(qa_name)
                        access_Forbid_flag = self.DB_True
                else:
                    message = message + '[业务元数据的质检中，没有项目{0}!请进行修正！]'.format(qa_name)
                    access_Forbid_flag = self.DB_True

            # 数据库部分
            access_Wait_flag, access_Forbid_flag, message = \
                self.db_access_check(access_Wait_flag, access_Forbid_flag, message)

            # 开始进行检查的结果判断
            access_flag = self.DataAccess_Pass
            if access_Forbid_flag:
                access_flag = self.DataAccess_Forbid
            elif access_Wait_flag:
                access_flag = self.DataAccess_Wait
            if CUtils.equal_ignore_case(message, ''):
                message = '模块可以进行访问!'

            result = CResult.merge_result(
                self.Success,
                '模块[{0}.{1}]对对象[{2}]的访问能力已经分析完毕!分析结果为:{3}'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name,
                    message
                )
            )
            return CResult.merge_result_info(result, self.Name_Access, access_flag)
        except:
            result = CResult.merge_result(
                self.Failure,
                '模块[{0}.{1}]对对象[{2}]的访问能力的分析存在异常!'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name
                )
            )
            return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)

    def db_access_check(self, access_Wait_flag, access_Forbid_flag, message):
        return access_Wait_flag, access_Forbid_flag, message

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        return check_dict

    def sync(self) -> str:
        self._before_sync()
        result_do = self._do_sync()
        return result_do

    def _before_sync(self):
        pass

    def _do_sync(self) -> str:
        table_name = CUtils.dict_value_by_name(self.information(), 'table_name', '')
        sql_check = '''
        select aprid from {0} where aprid='{1}'
        '''.format(table_name, self._obj_id)
        record_cheak = CFactory().give_me_db(self._db_id).one_row(sql_check).size()  # 查找记录数
        if record_cheak == 0:  # 记录数为0则拼接插入语句
            sql_all_archived = self.process_insert_sql(table_name, self.get_sync_dict_list(self.DB_True))
        else:  # 记录数不为0则拼接更新语句
            sql_all_archived = self.process_updata_sql(table_name, self.get_sync_dict_list(self.DB_False)
                                                       , self._obj_id)
        try:
            if CFactory().give_me_db(self._db_id).execute(sql_all_archived):  # 执行拼好的语句
                return CResult.merge_result(
                    self.Success,
                    '对象[{0}]的同步成功! '.format(self._obj_name)
                )
            else:
                return CResult.merge_result(
                    self.Failure,
                    '对象[{0}]的同步错误!,请检查配置.'.format(self._obj_name)
                )
        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '数据检索分发模块在进行数据同步时出现错误:同步的对象[{0}]在录入数据库时出现异常, '
                '可能是业务元数据或空间信息存在问题,详细情况: [{1}]!'.format(
                    self._obj_name,
                    error.__str__()
                )
            )

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = list()
        # sync_dict_list = self.add_value_to_sync_dict_list(sync_dict_list,'name','value',self.DB_True)
        return sync_dict_list

    def process_insert_sql(self, table_name, field_dict_list):

        """
        本方法构建插入语句
        """
        sql_temporary_1 = ''  # 拼表名
        sql_temporary_2 = ''  # 拼值
        duplicate_removal_set = set()  # 用于去重判断
        field_dict_list.reverse()  # 倒序进行循环，用于去重
        for field_dict in field_dict_list:
            field_name = CUtils.dict_value_by_name(field_dict, 'field_name', '')  # 获取字段名
            field_value = CUtils.dict_value_by_name(field_dict, 'field_value', '')  # 获取字段值
            field_type = CUtils.dict_value_by_name(field_dict, 'field_type', '')  # 获取字段类型
            if not CUtils.equal_ignore_case(field_value, '') and field_name not in duplicate_removal_set:
                duplicate_removal_set.add(field_name)  # 如果没有拼接过这个字段，这加入set集合，用于查重
                sql_temporary_1 = sql_temporary_1 + '{0},'.format(field_name)  # 拼接字段部分的sql
                if field_type:  # 拼接values部分的sql field_type判断是否需要加''
                    sql_temporary_2 = sql_temporary_2 + "'{0}',".format(field_value)
                else:
                    sql_temporary_2 = sql_temporary_2 + "{0},".format(field_value)
        insert_sql = '''
        INSERT INTO {0}({1}) VALUES ({2})
        '''.format(table_name, sql_temporary_1[:-1], sql_temporary_2[:-1])  # 记得截取后面的逗号
        return insert_sql

    def process_updata_sql(self, table_name, field_dict_list, oid):
        """
        本方法构建更新
        """
        sql_temporary = ''
        duplicate_removal_set = set()  # 用于去重判断
        field_dict_list.reverse()  # 倒序进行循环，用于去重
        for field_dict in field_dict_list:
            field_name = CUtils.dict_value_by_name(field_dict, 'field_name', '')
            field_value = CUtils.dict_value_by_name(field_dict, 'field_value', '')
            field_type = CUtils.dict_value_by_name(field_dict, 'field_type', '')
            if not CUtils.equal_ignore_case(field_value, '') and field_name not in duplicate_removal_set:
                duplicate_removal_set.add(field_name)
                if field_type:
                    sql_temporary = sql_temporary + "{0}='{1}',".format(field_name, field_value)
                else:
                    sql_temporary = sql_temporary + "{0}={1},".format(field_name, field_value)
        updata_sql = '''
        UPDATE {0} SET {1} WHERE aprid='{2}'
        '''.format(table_name, sql_temporary[:-1], oid)
        return updata_sql

    def add_value_to_sync_dict_list(self, sync_dict_list, field_name, field_value, field_type=True):
        """
        本方法构建同步用的配置列表
        """
        sync_dict_list.extend([
            {
                'field_name': field_name,
                'field_value': field_value,
                'field_type': field_type
            }
        ])
