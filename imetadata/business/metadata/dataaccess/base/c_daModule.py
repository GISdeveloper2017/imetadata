# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:17 
# @Author : 王西亚 
# @File : c_daModule.py

from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.database.c_factory import CFactory


class CDAModule(CResource):
    _db_id: str

    def __init__(self, db_id):
        super().__init__()
        self._db_id = db_id

    def information(self) -> dict:
        info = dict()
        info[self.Name_ID] = type(self).__name__
        info[self.Name_Title] = None
        info[self.Name_Type] = None
        info[self.Name_Enable] = True
        return info

    def access(self, obj_id, obj_name, obj_type, quality) -> str:
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
                obj_name
            )
        )
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)

    def notify_inbound(self, inbound_id: str) -> str:
        """
        批次通知
        """
        return CResult.merge_result(
            self.Success,
            '批次[{0}]已经推送给模块[{1}]队列! '.format(
                inbound_id,
                CUtils.dict_value_by_name(self.information(), self.Name_Title, '')
            )
        )

    def notify_object(self, inbound_id: str, access: str, memo: str, obj_id, obj_name, obj_type, quality) -> str:
        """
        处理数管中识别的对象, 与第三方模块的通知
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口

        注意: 在本方法中, 不要用_quality_info属性, 因为外部调用方考虑的效率因素, 没有传入!!!
        @:param access 当前模块对当前对象的权限
        :return:
        """
        ds_na = CFactory().give_me_db(self._db_id).one_row(
            '''
            select dsonid, dson_notify_status
            from dm2_storage_obj_na
            where dson_app_id = :app_id 
                and dson_object_id = :object_id
            ''',
            {
                'app_id': CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                'object_id': obj_id
            }
        )
        target_notify_status = self.ProcStatus_InQueue
        if not CUtils.equal_ignore_case(access, self.DataAccess_Pass):
            target_notify_status = self.ProcStatus_Finished
        if not ds_na.is_empty():
            na_id = CUtils.any_2_str(ds_na.value_by_name(0, 'dsonid', 0))
            if (ds_na.value_by_name(0, 'dson_notify_status', self.ProcStatus_Finished) == self.ProcStatus_Finished) or \
                    (ds_na.value_by_name(0, 'dson_notify_status', self.ProcStatus_Finished) == self.ProcStatus_InQueue):
                CFactory().give_me_db(self._db_id).execute(
                    '''
                    update dm2_storage_obj_na
                    set dson_notify_status = :status
                        , dson_object_access = :object_access
                        , dson_access_memo = :object_access_memo
                        , dson_inbound_id = :inbound_id
                    where dsonid = :id 
                    ''',
                    {
                        'id': na_id,
                        'status': target_notify_status,
                        'object_access': access,
                        'inbound_id': inbound_id,
                        'object_access_memo': memo
                    }
                )
        else:
            CFactory().give_me_db(self._db_id).execute(
                '''
                insert into dm2_storage_obj_na(dson_app_id, dson_object_access, dson_object_id, dson_inbound_id, dson_access_memo) 
                values(:app_id, :object_access, :object_id, :inbound_id, :object_access_memo)
                ''',
                {
                    'app_id': CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    'object_id': obj_id,
                    'object_access': access,
                    'inbound_id': inbound_id,
                    'object_access_memo': memo
                }
            )

        return CResult.merge_result(
            self.Success,
            '对象[{0}]已经推送给模块[{1}]队列! '.format(
                obj_name,
                CUtils.dict_value_by_name(self.information(), self.Name_Title, '')
            )
        )

    def sync(self, object_access, obj_id, obj_name, obj_type, quality) -> str:
        """
        处理数管中识别的对象, 与第三方模块的同步
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口

        注意: 在本方法中, 不要用_quality_info属性, 因为外部调用方考虑的效率因素, 没有传入!!!
        :return:
        """
        return CResult.merge_result(
            self.Success,
            '对象[{0}]的同步机制无效, 第三方系统将自行从数据中心提取最新数据! '.format(obj_name)
        )
