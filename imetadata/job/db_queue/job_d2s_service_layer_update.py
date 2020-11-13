# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 08:47 
# @Author : 王西亚 
# @File : job_d2s_service_layer_update.py
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.base.c_mdObjectSearch import CMDObjectSearch
from imetadata.business.data2service.base.job.c_d2sBaseJob import CD2SBaseJob
from imetadata.database.c_factory import CFactory


class job_d2s_service_layer_update(CD2SBaseJob):
    """
    数据服务发布-服务数据更新-调度
    1. 解析dp_v_qfg\dp_v_qfg_layer, 获取数据需求, 检查数据对象变化情况, 更新dp_v_qfg_layer_file表
    """

    def get_mission_seize_sql(self) -> str:
        return '''
        update dp_v_qfg_layer 
        set dpprocessid = '{0}', dpStatus = 2
        where dpid = (
          select dpid  
          from   dp_v_qfg_layer 
          where  dpStatus = 1  
          order by dpaddtime
          limit 1
          for update skip locked
        )        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
        select dp_v_qfg_layer.dpid, dp_v_qfg_layer.dplayer_id, dp_v_qfg_layer.dplayer_name
            , dp_v_qfg_layer.dplayer_object
            , dp_v_qfg.dpname, dp_v_qfg.dptitle
        from dp_v_qfg_layer left join dp_v_qfg on dp_v_qfg_layer.dpservice_id = dp_v_qfg.dpid 
        where dp_v_qfg_layer.dpprocessid = '{0}' and dp_v_qfg.dpid is not null
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
        update dp_v_qfg_layer 
        set dpStatus = 1, dpprocessid = null 
        where dpStatus = 2
        '''

    def process_mission(self, dataset) -> str:
        """
        详细算法复杂, 参见readme.md中[##### 服务发布调度]章节
        :param dataset:
        :return:
        """
        layer_id = dataset.value_by_name(0, 'dpid', '')
        layer_name = dataset.value_by_name(0, 'dplayer_id', '')
        layer_title = dataset.value_by_name(0, 'dplayer_name', '')
        layer_service_name = dataset.value_by_name(0, 'dpname', '')
        layer_service_title = dataset.value_by_name(0, 'dptitle', '')
        layer_object = CUtils.any_2_str(dataset.value_by_name(0, 'dplayer_object', None))
        CLogger().debug(
            '即将更新服务[{0}.{1}]的图层[{2}.{3}.{4}]...'.format(
                layer_service_name, layer_service_title, layer_id, layer_name, layer_title
            )
        )

        object_da_result = CJson()

        try:
            object_da_result.load_json_text(layer_object)

            object_dataset = CMDObjectSearch(self.get_mission_db_id()).search_object(object_da_result)
            if object_dataset.is_empty():
                self.__layer_file_empty(layer_id)
                result = CResult.merge_result(
                    self.Success,
                    '服务[{0}.{1}]的图层[{2}.{3}.{4}]检查更新成功完成'.format(
                        layer_service_name, layer_service_title, layer_id, layer_name, layer_title
                    )
                )
                return result

            CLogger().debug(
                '服务[{0}.{1}]的图层[{2}.{3}.{4}], 发现[{5}]个符合要求的数据对象!'.format(
                    layer_service_name, layer_service_title, layer_id, layer_name, layer_title, object_dataset.size()
                )
            )

            for data_index in range(object_dataset.size()):
                object_id = object_dataset.value_by_name(data_index, 'object_id', '')
                object_name = object_dataset.value_by_name(data_index, 'object_name', '')
                CLogger().debug(
                    '服务[{0}.{1}]的图层[{2}.{3}.{4}], 发现[{5}]个符合要求的数据对象!\n第[{6}]个可用的对象为[{7}.{8}]'.format(
                        layer_service_name, layer_service_title, layer_id, layer_name, layer_title,
                        object_dataset.size(), object_id, object_name
                    )
                )

            result = CResult.merge_result(
                self.Success,
                '服务[{0}.{1}]的图层[{2}.{3}.{4}]检查更新成功完成'.format(
                    layer_service_name, layer_service_title, layer_id, layer_name, layer_title
                )
            )
            self.update_layer_update_result(layer_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '服务[{0}.{1}]的图层[{2}.{3}.{4}]检查更新失败, 错误原因为: {5}'.format(
                    layer_service_name, layer_service_title, layer_id, layer_name, layer_title, error.__str__()
                )
            )
            self.update_layer_update_result(layer_id, result)
            return result

    def update_layer_update_result(self, deploy_id, result):
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dp_v_qfg_layer 
                set dpStatus = 0, dpprocessresult = :message
                where dpid = :id   
                ''', {'id': deploy_id, 'message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dp_v_qfg_layer 
                set dpStatus = 21, dpprocessresult = :message
                where dpid = :id   
                ''', {'id': deploy_id, 'message': CResult.result_message(result)}
            )

    def __layer_file_empty(self, layer_id):
        CFactory().give_me_db(self.get_mission_db_id()).execute_batch(
            [
                (
                    '''
                    delete from dp_v_qfg_layer_file 
                    where dpdf_layer_id = :layer_id   
                    ''',
                    {'layer_id': layer_id}
                ),
                (
                    '''
                    delete from dp_v_qfg_layer
                    where dpid = :layer_id   
                    ''',
                    {'layer_id': layer_id}
                )
            ]
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_d2s_service_layer_update('', '').execute()
