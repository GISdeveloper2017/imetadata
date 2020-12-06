# -*- coding: utf-8 -*- 
# @Time : 2020/11/10 11:34 
# @Author : 王西亚 
# @File : job_d2s_service_creator.py
from imetadata.business.data2service.base.job.c_d2sBaseJob import CD2SBaseJob


class job_d2s_service_creator(CD2SBaseJob):
    """
    数据服务发布-服务批量创建-算法
    1. 解析dp_v_qfg_schema和dp_v_qfg_schema_layer表, 将服务加入到dp_v_qfg中
    """

    def get_mission_seize_sql(self) -> str:
        pass

    def get_mission_info_sql(self) -> str:
        pass

    def get_abnormal_mission_restart_sql(self) -> str:
        pass

    def process_mission(self, dataset, is_retry_mission: bool) -> str:
        pass
