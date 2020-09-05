#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52
# @Author : 王西亚
# @File : controlCenterExecute.py

from imetadata.schedule.execute.c_dbQueueScheduleExecute import CDBQueueScheduleExecute
from imetadata.database.c_factory import CFactory


class CControlCenterExecute(CDBQueueScheduleExecute):
    def should_stop(self) -> bool:
        sql = '''
        select scmid
        from sch_center_mission
        where scmcommand <> 'shutdown' or scmstatus <> 0
        limit 1
        '''

        try:
            factory = CFactory()
            db = factory.give_me_db()
            return not db.if_exists(sql)
        except:
            return True
