# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 16:14 
# @Author : 王西亚 
# @File : job_dm_obj_detail.py


from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CUtils
from imetadata.base.Exceptions import DBException
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_obj_detail(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsodetailparseprocid = '{0}', dsodetailparsestatus = 2
where dsoid = (
  select dsoid  
  from   dm2_storage_object 
  where  dsodetailparsestatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dsoid, dsodatatype, dsoobjecttype from dm2_storage_object where dsodetailparseprocid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsodetailparsestatus = 1, dsodetailparseprocid = null 
where dsodetailparsestatus = 2
        '''

    def process_mission(self, dataset):
        dso_id = dataset.value_by_name(0, 'dsoid', '')
        dso_data_type = dataset.value_by_name(0, 'dsodatatype', '')
        dso_object_type = dataset.value_by_name(0, 'dsoobjecttype', '')

        CLogger().debug('开始处理对象: {0}.{1}.{2}的元数据'.format(dso_id, dso_data_type, dso_object_type))


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_obj_detail('', '').execute()
