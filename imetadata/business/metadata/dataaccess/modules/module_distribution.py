# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:58 
# @Author : 王西亚 
# @File : module_distribution.py
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule
from imetadata.database.c_factory import CFactory


class module_distribution(CDAModule):
    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据检索分发'

        return info

    def access(self) -> str:
        """
        解析数管中识别出的对象, 与第三方模块的访问能力, 在本方法中进行处理
        返回的json格式字符串中, 是默认的CResult格式, 但是在其中还增加了Access属性, 通过它反馈当前对象是否满足第三方模块的应用要求
        注意: 一定要反馈Access属性
        :return:
        """
        result = super().access()
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Pass)

    def notify(self) -> str:
        """
        处理数管中识别的对象, 与第三方模块的同步
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口
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
                'object_id': self._obj_id
            }
        )
        if not ds_na.is_empty():
            na_id = CUtils.any_2_str(ds_na.value_by_name(0, 'dsonid', 0))
            if ds_na.value_by_name(0, 'dson_notify_status', self.ProcStatus_Finished) == self.ProcStatus_Finished:
                CFactory().give_me_db(self._db_id).execute(
                    '''
                    update dm2_storage_obj_na
                    set dson_notify_status = :status
                    where dsonid = :id 
                    ''',
                    {'id': na_id, 'status': self.ProcStatus_InQueue}
                )
        else:
            CFactory().give_me_db(self._db_id).execute(
                '''
                insert into dm2_storage_obj_na(dson_app_id, dson_object_id) 
                values(:app_id, :object_id)
                ''',
                {
                    'app_id': CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    'object_id': self._obj_id
                }
            )

        return CResult.merge_result(
            self.Success,
            '对象[{0}]已经推送给模块[{1}]队列! '.format(
                self._obj_name,
                CUtils.dict_value_by_name(self.information(), self.Name_Title, '')
            )
        )

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
            '在[{0}]里写对象[{1}]向模块[{2}]中同步的算法! '.format(
                CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                self._obj_name,
                CUtils.dict_value_by_name(self.information(), self.Name_Title, '')
            )
        )
