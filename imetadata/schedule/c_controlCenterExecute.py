#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52
# @Author : 王西亚
# @File : controlCenterExecute.py

from imetadata.database.c_factory import CFactory
from imetadata.schedule.execute.c_dbQueueScheduleExecute import CDBQueueScheduleExecute


class CControlCenterExecute(CDBQueueScheduleExecute):
    def should_stop(self) -> bool:
        sql = '''
        select scmid
        from sch_center_mission
        where scmcommand <> '{0}' or scmstatus <> {1}
        limit 1
        '''.format(self.CMD_SHUTDOWN, self.Status_Finish)

        try:
            factory = CFactory()
            db = factory.give_me_db()
            return not db.if_exists(sql)
        except:
            return True
