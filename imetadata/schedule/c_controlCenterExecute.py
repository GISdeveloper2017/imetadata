#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 13:52
# @Author : 王西亚
# @File : controlCenterExecute.py
from imetadata import settings
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.execute.c_dbQueueScheduleExecute import CDBQueueScheduleExecute


class CControlCenterExecute(CDBQueueScheduleExecute):
    def __init__(self, schedule_id, schedule_trigger, schedule_algorithm, schedule_params=None):
        super(CControlCenterExecute, self).__init__(schedule_id, schedule_trigger, schedule_algorithm, schedule_params)
        self.__application_id = settings.application.xpath_one(self.Path_Setting_Application_ID, None)

    def should_stop(self) -> bool:
        if self.__application_id is None:
            sql = '''
            select scmid
            from sch_center_mission
            where (scmcommand <> '{0}' or scmstatus <> {1})
                and (
                    (scmcenterid is null) or 
                    (scmcenterid in (select scid from sch_center where scserver is null))
                )
            limit 1
            '''.format(self.CMD_SHUTDOWN, self.Status_Finish)
        else:
            sql = '''
            select scmid
            from sch_center_mission
            where (scmcommand <> '{0}' or scmstatus <> {1})
                and (scmcenterid in (select scid from sch_center where scserver = '{2}'))
            limit 1
            '''.format(self.CMD_SHUTDOWN, self.Status_Finish, CUtils.any_2_str(self.__application_id))

        try:
            factory = CFactory()
            db = factory.give_me_db()
            return not db.if_exists(sql)
        except:
            return True
