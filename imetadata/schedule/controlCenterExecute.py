#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52
# @Author : 王西亚
# @File : controlCenterExecute.py

from imetadata.schedule.scheduleBase import scheduleBase
from imetadata.schedule.scheduleExecuteBase import scheduleExecuteBase
from imetadata.base.c_object import CObject
from imetadata.base.c_sys import CSys
from imetadata.database.factory import Factory


class controlCenterExecute(scheduleExecuteBase):

    def default_create_schedule(self, schedule_algorithm, *args, **kwargs) -> scheduleBase:
        return CObject.create_business_instance(CSys.get_business_dir(), 'imetadata.business', schedule_algorithm, args, kwargs)

    def stop(self) -> bool:
        sql = '''
        select scmid
        from sch_center_mission
        where scmparallelcount > -1 or scmstatus <> 0
        limit 1
        '''

        try:
            factory = Factory()
            db = factory.give_me_db()
            return not db.if_exists(sql)
        except:
            return True
