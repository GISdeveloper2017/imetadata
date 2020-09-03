#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52
# @Author : 王西亚
# @File : controlCenterExecute.py

from imetadata.schedule.type.c_DBQueueSchedule import CDBQueueSchedule
from imetadata.schedule.execute.c_DBQueueScheduleExecute import CDBQueueScheduleExecute
from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from imetadata.database.c_factory import CFactory


class CControlCenterExecute(CDBQueueScheduleExecute):

    def default_create_sch_mission(self, schedule_algorithm, *args, **kwargs) -> CDBQueueSchedule:
        return CObject.create_business_instance(CSys.get_business_dir(), 'imetadata.business', schedule_algorithm, args, kwargs)

    def stop(self) -> bool:
        sql = '''
        select scmid
        from sch_center_mission
        where scmparallelcount > -1 or scmstatus <> 0
        limit 1
        '''

        try:
            factory = CFactory()
            db = factory.give_me_db()
            return not db.if_exists(sql)
        except:
            return True
