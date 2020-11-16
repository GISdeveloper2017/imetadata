# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 14:31 
# @Author : 王西亚 
# @File : job_d2s_service_update_monitor.py
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_d2s_service_update_monitor(CTimeJob):
    def execute(self) -> str:
        service_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select dpid, dptitle
            from dp_v_qfg
            where dpstatus = 2
            '''
        )
        if service_list.is_empty():
            return CResult.merge_result(CResult.Success, '任务执行成功结束！')

        for data_index in range(service_list.size()):
            record_index = data_index

            service_id = service_list.value_by_index(record_index, 0, '')
            service_title = service_list.value_by_index(record_index, 1, '')
            CLogger().debug('正在检查服务[{0}.{1}]的状态...'.format(service_id, service_title))
            try:
                layer_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
                    '''
                    select dpstatus
                    from dp_v_qfg_layer
                    group by dpstatus
                    '''
                )
                has_finished = False
                has_processing = False
                has_error = False
                for layer_index in range(layer_list.size()):
                    layer_status = CUtils.any_2_str(layer_list.value_by_index(layer_index, 0, 0))
                    if CUtils.equal_ignore_case(layer_status, '0'):
                        has_finished = True
                    elif CUtils.equal_ignore_case(layer_status, '1'):
                        has_processing = True
                    elif CUtils.equal_ignore_case(layer_status, '2'):
                        has_processing = True
                    else:
                        has_error = True

                if not has_processing:
                    if has_error:
                        message = '服务[{0}.{1}]下的图层均已经处理完毕, 但有错误的记录!'.format(service_id, service_title)
                        CLogger().debug(message)
                        CFactory().give_me_db(self.get_mission_db_id()).execute(
                            '''
                            update dp_v_qfg
                            set dpstatus = 11, dpprocessresult = :message, dplastmodifytime = now()
                            where dpid = :id
                            ''',
                            {'id': service_id, 'message': message}
                        )
                    elif has_finished:
                        message = '服务[{0}.{1}]下的图层均已经处理完毕!'.format(service_id, service_title)
                        CLogger().debug(message)
                        # todo(王西亚) 这里先将检查完毕的服务状态改为4, 后续改为从ro_global_config中读取设定值
                        CFactory().give_me_db(self.get_mission_db_id()).execute(
                            '''
                            update dp_v_qfg
                            set dpstatus = 4, dpprocessresult = :message, dplastmodifytime = now()
                            where dpid = :id
                            ''',
                            {'id': service_id, 'message': message}
                        )
                    else:
                        CLogger().debug('服务[{0}.{1}]下无任何图层, 该服务将被删除!!!'.format(service_id, service_title))
                        CFactory().give_me_db(self.get_mission_db_id()).execute(
                            '''
                            delete from dp_v_qfg
                            where dpid = :id
                            ''',
                            {'id': service_id}
                        )
                else:
                    message = '服务[{0}.{1}]下有正在检查处理的图层, 系统稍后会再次检查!'.format(service_id, service_title)
                    CLogger().debug(message)
                    CFactory().give_me_db(self.get_mission_db_id()).execute(
                        '''
                        update dp_v_qfg
                        set dpprocessresult = :message, dplastmodifytime = now()
                        where dpid = :id
                        ''',
                        {'id': service_id, 'message': message}
                    )
            except Exception as error:
                message = '检查服务[{0}.{1}]的状态过程出现异常! 错误信息为: {2}'.format(service_id, service_title, error.__str__())
                CLogger().debug(message)
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dp_v_qfg
                    set dpstatus = 21, dpprocessresult = :message, dplastmodifytime = now()
                    where dpid = :id
                    ''',
                    {'id': service_id, 'message': message}
                )

        return CResult.merge_result(CResult.Success, '服务发布监控任务执行成功结束！')
