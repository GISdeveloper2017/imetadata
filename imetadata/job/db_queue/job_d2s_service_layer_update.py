# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 08:47 
# @Author : 王西亚 
# @File : job_d2s_service_layer_update.py
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.base.c_mdObjectCatalog import CMDObjectCatalog
from imetadata.business.data2service.base.job.c_d2sBaseJob import CD2SBaseJob
from imetadata.database.c_factory import CFactory


class job_d2s_service_layer_update(CD2SBaseJob):
    """
    数据服务发布-服务数据更新-调度
    1. 解析dp_v_qfg, dp_v_qfg_layer, 获取数据需求, 检查数据对象变化情况, 更新dp_v_qfg_layer_file表
update dp_v_qfg_schema set dpprocessid = '$missionid$', dpstatus = 2
where dpID = (
select dpID from dp_v_qfg_schema
where dpstatus = 1 and dpid not in
(
  select dpschemaid
  from
  (
    select dpschemaid, count(*) from dp_v_qfg where dpstatus <> 0  group by dpschemaid
   ) schema_stat
)
order by dplastmodifytime limit 1 for update skip locked)

    """

    def get_mission_seize_sql(self) -> str:
        return '''
        update dp_v_qfg_layer 
        set dpprocessid = '{0}', dpStatus = {2}
        where dpid = (
          select dpid  
          from   dp_v_qfg_layer  
          where  dpStatus = {1}  and dpservice_id in 
          (
              select dpid from dp_v_qfg where dpstatus = {2} 
          )
          order by dpaddtime
          limit 1
          for update skip locked
        )        
        '''.format(self.SYSTEM_NAME_MISSION_ID, self.ProcStatus_InQueue, self.ProcStatus_Processing)

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
        set dpStatus = {0}, dpprocessid = null 
        where dpStatus = {1}
        '''.format(self.ProcStatus_InQueue, self.ProcStatus_Processing)

    def process_mission(self, dataset, is_retry_mission: bool) -> str:
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
            self.__layer_init(layer_id)

            object_da_result.load_json_text(layer_object)
            object_catalog = CMDObjectCatalog(self.get_mission_db_id())
            object_dataset = object_catalog.search(
                self.ModuleName_Data2Service,
                object_da_result
            )
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
                        object_dataset.size(), data_index, object_id, object_name
                    )
                )
                layer_file_id = self.__layer_object_id(layer_id, object_id)
                if layer_file_id is None:
                    layer_file_id = CUtils.one_id()
                    object_full_name = object_catalog.object_full_name_by_id(object_id)
                    CFactory().give_me_db(self.get_mission_db_id()).execute(
                        '''
                        insert into dp_v_qfg_layer_file(
                            dpdf_id, dpdf_layer_id, dpdf_group_id, dpdf_object_id
                            , dpdf_object_fullname, dpdf_object_title, dpdf_object_size, dpdf_object_date) 
                        values(:layer_file_id, :layer_id, :group_id, :object_id
                            , :object_fullname, :object_title, :object_size, :object_date)
                        ''',
                        {
                            'object_id': object_id,
                            'object_title': object_name,
                            'object_fullname': object_full_name,
                            'object_date': object_dataset.value_by_name(data_index, 'object_lastmodifytime', None),
                            'object_size': object_dataset.value_by_name(data_index, 'object_size', 0),
                            'layer_file_id': layer_file_id,
                            'layer_id': layer_id,
                            'group_id': layer_id
                        }
                    )
                else:
                    CFactory().give_me_db(self.get_mission_db_id()).execute(
                        '''
                        update dp_v_qfg_layer_file 
                        set dpdf_object_size = :object_size
                            , dpdf_object_date = :object_date
                        where dpdf_id = :layer_file_id   
                        ''',
                        {
                            'object_date': object_dataset.value_by_name(data_index, 'object_lastmodifytime', None),
                            'object_size': object_dataset.value_by_name(data_index, 'object_size', 0),
                            'layer_file_id': layer_file_id
                        }
                    )

                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dp_v_qfg_layer_file 
                    set dpdf_object_fp = MD5(
                            coalesce(dpdf_object_title, '')||'-'||
                            coalesce(dpdf_object_size, 0)::text||'-'||
                            coalesce(dpdf_object_date, now())::text
                        )
                    where dpdf_id = :layer_file_id   
                    ''',
                    {'layer_file_id': layer_file_id}
                )
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dp_v_qfg_layer_file 
                    set dpdf_processtype = :process_type
                    where dpdf_id = :layer_file_id and dpdf_object_fp = dpdf_object_fp_lastdeploy
                    ''',
                    {'layer_file_id': layer_file_id, 'process_type': self.ProcType_Same}
                )
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dp_v_qfg_layer_file 
                    set dpdf_processtype = :process_type 
                    where dpdf_id = :layer_file_id 
                        and ( dpdf_object_fp <> dpdf_object_fp_lastdeploy or dpdf_object_fp_lastdeploy is null)
                    ''',
                    {'layer_file_id': layer_file_id, 'process_type': self.ProcType_Update}
                )

            self.__layer_clear(layer_id)
            self.__layer_re_calc_group(layer_id)

            result = CResult.merge_result(
                self.Success,
                '服务[{0}.{1}]的图层[{2}.{3}.{4}]检查更新成功完成'.format(
                    layer_service_name, layer_service_title, layer_id, layer_name, layer_title
                )
            )
            self.__update_layer_update_result(layer_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '服务[{0}.{1}]的图层[{2}.{3}.{4}]检查更新失败, 错误原因为: {5}'.format(
                    layer_service_name, layer_service_title, layer_id, layer_name, layer_title, error.__str__()
                )
            )
            self.__update_layer_update_result(layer_id, result)
            return result

    def __update_layer_update_result(self, deploy_id, result):
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

    def __layer_object_id(self, layer_id, object_id):
        return CFactory().give_me_db(self.get_mission_db_id()).one_value(
            '''
            select dpdf_id
            from dp_v_qfg_layer_file
            where dpdf_layer_id = :layer_id
                and dpdf_object_id = :object_id
            ''',
            {'layer_id': layer_id, 'object_id': object_id}
        )

    def __layer_init(self, layer_id):
        """
        将所有该层下的文件都设置为delete
        :param layer_id:
        :return:
        """
        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dp_v_qfg_layer_file
            set dpdf_processtype = :process_type
            where dpdf_layer_id = :layer_id
            ''',
            {'layer_id': layer_id, 'process_type': self.ProcType_Delete}
        )

    def __layer_clear(self, layer_id):
        """
        将该层下, 所有标记为delete的文件
        :param layer_id:
        :return:
        """
        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            delete from dp_v_qfg_layer_file
            where dpdf_layer_id = :layer_id and dpdf_processtype = :process_type
            ''',
            {'layer_id': layer_id, 'process_type': self.ProcType_Delete}
        )

    def __layer_re_calc_group(self, layer_id):
        """
        重算该层下的组
        :param layer_id:
        :return:
        """
        ds_group = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select dm2_storage_object.dso_prj_proj4 
            from dp_v_qfg_layer_file 
                left join dm2_storage_object on dp_v_qfg_layer_file.dpdf_object_id = dm2_storage_object.dsoid
            where dpdf_layer_id = :layer_id 
            group by dm2_storage_object.dso_prj_proj4
            ''',
            {'layer_id': layer_id}
        )
        if ds_group.size() == 1:
            return

        for group_index in range(ds_group.size()):
            proj4_text = ds_group.value_by_index(group_index, 0, None)
            group_id = '{0}_{1}'.format(layer_id, group_index)

            if proj4_text is None:
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dp_v_qfg_layer_file
                    set dpdf_group_id = :group_id
                    from dm2_storage_object
                    where 
                        dp_v_qfg_layer_file.dpdf_object_id = dm2_storage_object.dsoid
                        and dp_v_qfg_layer_file.dpdf_layer_id = :layer_id 
                        and dm2_storage_object.dso_prj_proj4 is null
                    ''',
                    {'layer_id': layer_id, 'group_id': group_id}
                )
            else:
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dp_v_qfg_layer_file
                    set dpdf_group_id = :group_id
                    from dm2_storage_object
                    where 
                        dp_v_qfg_layer_file.dpdf_object_id = dm2_storage_object.dsoid
                        and dp_v_qfg_layer_file.dpdf_layer_id = :layer_id 
                        and dm2_storage_object.dso_prj_proj4 = :proj4_text
                    ''',
                    {'layer_id': layer_id, 'group_id': group_id, 'proj4_text': proj4_text}
                )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_d2s_service_layer_update('', '').execute()
