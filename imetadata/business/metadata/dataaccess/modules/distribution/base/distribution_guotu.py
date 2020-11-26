# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : distribution_guotu.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base
from imetadata.database.c_factory import CFactory
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.database.tools.c_table import CTable


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
        try:
            table_name = CUtils.dict_value_by_name(self.information(), 'table_name', '')
            # 因此类插件的表格情况特殊，为双主键，且要先确定插入还是更新，所以不用table.if_exists()方法
            sql_check = '''
            select aprid from {0} where aprid='{1}'
            '''.format(table_name, self._obj_id)
            record_cheak = CFactory().give_me_db(self._db_id).one_row(sql_check).size()  # 查找记录数
            if record_cheak == 0:  # 记录数为0则拼接插入语句
                insert_or_updata = self.DB_True
            else:  # 记录数不为0则拼接更新语句
                insert_or_updata = self.DB_False

            table = CTable()
            table.load_info(CResource.DB_Server_ID_Default, table_name)
            # insert_or_updatad的意义是要先确定是更新还是插入，不能把不该更新的，在插入时是默认值的参数更新
            for field_dict in self.get_sync_dict_list(insert_or_updata):
                field_name = CUtils.dict_value_by_name(field_dict, 'field_name', '')  # 获取字段名
                field_value = CUtils.dict_value_by_name(field_dict, 'field_value', '')  # 获取字段值
                field_value_type = CUtils.dict_value_by_name(field_dict, 'field_value_type', '')  # 获取值类型
                if CUtils.equal_ignore_case(field_value, ''):
                    table.column_list.column_by_name(field_name).set_null()
                elif CUtils.equal_ignore_case(field_value_type, self.DataValueType_Value):
                    table.column_list.column_by_name(field_name).set_value(field_value)
                elif CUtils.equal_ignore_case(field_value_type, self.DataValueType_SQL):
                    table.column_list.column_by_name(field_name).set_sql(field_value)
                elif CUtils.equal_ignore_case(field_value_type, self.DataValueType_Array):
                    table.column_list.column_by_name(field_name).set_array(field_value)
                else:
                    pass

            # 不多执行table.if_exists()多查一次哭，所以不用savedata()方法
            if insert_or_updata:
                result = table.insert_data()
            else:
                result = table.update_data()

            if CResult.result_success(result):
                return CResult.merge_result(
                    self.Success,
                    '对象[{0}]的同步成功! '.format(self._obj_name)
                )
            else:
                return result
        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '数据检索分发模块在进行数据同步时出现错误:同步的对象[{0}]在处理时出现异常, 详细情况: [{1}]!'.format(
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

    def add_value_to_sync_dict_list(self, sync_dict_list, field_name, field_value
                                    , field_value_type=CResource.DataValueType_Value):
        """
        本方法构建同步用的配置列表
        """
        sync_dict_list.extend([
            {
                'field_name': field_name,
                'field_value': field_value,
                'field_value_type': field_value_type
            }
        ])
