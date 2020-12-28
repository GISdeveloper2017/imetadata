# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : distribution_guotu.py
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base
from imetadata.database.c_factory import CFactory
from imetadata.database.tools.c_table import CTable
import datetime


class distribution_satellite(distribution_base):
    """
    卫星即时服务的基础类
    """

    def information(self) -> dict:
        info = super().information()
        info['metadata_table_name'] = 'ap_product_metadata'
        info['ndi_table_name'] = 'ap_product_ndi'
        return info

    def access(self) -> str:
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
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '模块[{0}.{1}]对对象[{2}]的访问能力的分析存在异常!详细情况: {3}!'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name,
                    error.__str__()
                )
            )
            return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)

    def db_access_check(self, access_Wait_flag, access_Forbid_flag, message):
        return access_Wait_flag, access_Forbid_flag, message

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        return check_dict

    def sync(self) -> str:
        try:
            metadata_table_name = CUtils.dict_value_by_name(self.information(), 'metadata_table_name', '')
            ndi_table_name = CUtils.dict_value_by_name(self.information(), 'ndi_table_name', '')
            # 因此类插件的表格情况特殊，为双主键，且要先确定插入还是更新，所以不用table.if_exists()方法
            metadata_sql_check = '''
            select id from {0} where id='{1}'
            '''.format(metadata_table_name, self._obj_id)
            metadata_record_cheak = CFactory().give_me_db(self._db_id).one_row(metadata_sql_check).size()  # 查找记录数

            ndi_sql_check = '''
            select id from {0} where id='{1}'
            '''.format(ndi_table_name, self._obj_id)
            ndi_record_cheak = CFactory().give_me_db(self._db_id).one_row(ndi_sql_check).size()  # 查找记录数

            if (metadata_record_cheak == 0) and (ndi_record_cheak == 0):  # 记录数为0则拼接插入语句
                insert_or_updata = self.DB_True
            elif (metadata_record_cheak > 0) and (ndi_record_cheak > 0):  # 记录数不为0则拼接更新语句
                insert_or_updata = self.DB_False
            else:
                return CResult.merge_result(
                    self.Failure,
                    '数据检索分发模块在进行数据同步时出现错误:同步的对象[{0}]在处理时出现异常, 详细情况: [{1}]!'.format(
                        self._obj_name,
                        '数据库中在存在异常数据，可能是垃圾数据未清理干净'
                    )
                )

            metadata_table = CTable()
            metadata_table.load_info(self._db_id, metadata_table_name)
            metadata_table.column_list.column_by_name('id').set_value(self._obj_id)
            metadata_table.column_list.column_by_name('fid').set_value(self._obj_id)
            dsometadataxml = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
            metadata_table.column_list.column_by_name('metaxml').set_value(dsometadataxml)
            now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
            metadata_table.column_list.column_by_name('addtime').set_value(now_time)
            metadata_table.column_list.column_by_name('version').set_null()

            ndi_table = CTable()
            ndi_table.load_info(self._db_id, ndi_table_name)
            # insert_or_updatad的意义是要先确定是更新还是插入，不能把不该更新的，在插入时是默认值的参数更新
            for field_dict in self.get_sync_dict_list(insert_or_updata):
                field_name = CUtils.dict_value_by_name(field_dict, 'field_name', '')  # 获取字段名
                field_value = CUtils.dict_value_by_name(field_dict, 'field_value', '')  # 获取字段值
                field_value_type = CUtils.dict_value_by_name(field_dict, 'field_value_type', '')  # 获取值类型
                if CUtils.equal_ignore_case(field_value, ''):
                    ndi_table.column_list.column_by_name(field_name).set_null()
                elif CUtils.equal_ignore_case(field_value_type, self.DataValueType_Value):
                    ndi_table.column_list.column_by_name(field_name).set_value(field_value)
                elif CUtils.equal_ignore_case(field_value_type, self.DataValueType_SQL):
                    ndi_table.column_list.column_by_name(field_name).set_sql(field_value)
                elif CUtils.equal_ignore_case(field_value_type, self.DataValueType_Array):
                    ndi_table.column_list.column_by_name(field_name).set_array(field_value)
                else:
                    pass

            # 不多执行table.if_exists()多查一次哭，所以不用savedata()方法
            if insert_or_updata:
                metadata_result = metadata_table.insert_data()
                ndi_result = ndi_table.insert_data()
            else:
                metadata_result = metadata_table.update_data()
                ndi_result = ndi_table.update_data()

            if CResult.result_success(metadata_result) and CResult.result_success(ndi_result):
                return CResult.merge_result(
                    self.Success,
                    '对象[{0}]的同步成功! '.format(self._obj_name)
                )
            else:
                if CResult.result_success(metadata_result):
                    return ndi_result
                else:
                    return metadata_result
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

    def add_value_to_sync_dict_list(self, sync_dict_list, field_name, field_value,
                                    field_value_type=CResource.DataValueType_Value):
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
