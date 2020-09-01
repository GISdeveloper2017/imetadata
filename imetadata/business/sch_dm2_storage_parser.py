#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import

from imetadata.base.core.Exceptions import DBException
from imetadata.base.utils import MetaDataUtils
from imetadata.database.factory import Factory
from imetadata.schedule.scheduleBase import scheduleBase
from imetadata.base.logger import Logger
from multiprocessing import Process, Semaphore, Queue, Lock, Manager, Event


class sch_dm2_storage_parser(scheduleBase):
    def process_mission(self, dataset):
        storage_id = dataset.value_by_name(0, 'root_directory_id', '')
        Logger().debug('storage_id: {0}'.format(storage_id))

        process_sql = '''
update dm2_storage 
set dstscanstatus = 0
where dstid = '{0}'
'''.format(storage_id)

        try:
            factory = Factory()
            db = factory.give_me_db(self.get_mission_db_id())
            db.execute(process_sql)
        except DBException as err:
            pass

        return MetaDataUtils.merge_result(MetaDataUtils.Success, '测试成功')

    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage 
set dstprocessid = '{0}', dstscanstatus = 2
where dstid = (
  select dstid  
  from   dm2_storage 
  where  dstscanstatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dstid as root_directory_id, dstunipath as root_directory from dm2_storage where dstprocessid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage 
set dstscanstatus = 1, dstprocessid = null 
where dstscanstatus = 2
        '''
