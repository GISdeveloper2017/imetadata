# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 08:47 
# @Author : 王西亚 
# @File : job_d2s_service_update.py
from imetadata.business.data2service.base.job.c_d2sBaseJob import CD2SBaseJob


class job_d2s_service_update(CD2SBaseJob):
    """
    数据服务发布-服务数据更新-调度
    1. 解析dp_v_qfg\dp_v_qfg_layer, 获取数据需求, 检查数据对象变化情况, 更新dp_v_qfg_layer_file表
    """
    def get_mission_seize_sql(self) -> str:
        pass

    def get_mission_info_sql(self) -> str:
        pass

    def get_abnormal_mission_restart_sql(self) -> str:
        pass

    def process_mission(self, dataset) -> str:
        pass
