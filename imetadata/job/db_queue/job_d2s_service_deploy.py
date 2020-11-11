# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 08:48 
# @Author : 王西亚 
# @File : job_d2s_service_deploy.py
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.business.data2service.base.job.c_d2sBaseJob import CD2SBaseJob
from imetadata.database.c_factory import CFactory


class job_d2s_service_deploy(CD2SBaseJob):
    """
    数据服务发布-单个服务发布-算法
    1. 解析dp_v_qfg\dp_v_qfg_layer\dp_v_qfg_layer_file表, 将服务创建到mapserver中
    """

    def get_mission_seize_sql(self) -> str:
        return '''
update dp_v_qfg 
set dpprocessid = '{0}', dpStatus = 6
where dpid = (
  select dpid  
  from   dp_v_qfg 
  where  dpStatus = 5  
  order by dpaddtime
  limit 1
  for update skip locked
)        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select dpid, dptitle, dpname
    , dptimeid, dpspatialid, dpbusid
    , dpserviceparams
from dp_v_qfg 
where dpprocessid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dp_v_qfg 
set dpStatus = 5, dpprocessid = null 
where dpStatus = 6
        '''

    def process_mission(self, dataset) -> str:
        """
        详细算法复杂, 参见readme.md中[##### 服务发布调度]章节
        @todo(张雄雄) 开始开发服务发布框架
        :param dataset:
        :return:
        """
        deploy_id = dataset.value_by_name(0, 'dpid', '')
        deploy_s_title = dataset.value_by_name(0, 'dptitle', '')
        deploy_s_name = dataset.value_by_name(0, 'dpname', '')
        CLogger().debug('即将发布服务为: {0}.{1}.{2}'.format(deploy_id, deploy_s_name, deploy_s_title))
        try:

            # dataset = CFactory().give_me_db(self.get_mission_db_id()).all_row()
            result = CResult.merge_result(
                self.Success,
                '服务: {0}.{1}.{2}发布成功'.format(deploy_id, deploy_s_name, deploy_s_title)
            )
            self.update_deploy_result(deploy_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '服务: {0}.{1}.{2}发布失败, 错误原因为: {4}'.format(deploy_id, deploy_s_name, deploy_s_title, error.__str__())
            )
            self.update_deploy_result(deploy_id, result)
            return result

    def update_deploy_result(self, deploy_id, result):
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dp_v_qfg 
                set dpStatus = 0, dpprocessresult = :message
                where dpid = :id   
                ''', {'id': deploy_id, 'message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dp_v_qfg 
                set dpStatus = 61, dpprocessresult = :message
                where dpid = :id   
                ''', {'id': deploy_id, 'message': CResult.result_message(result)}
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_d2s_service_deploy('', '').execute()
