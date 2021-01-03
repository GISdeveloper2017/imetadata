# -*- coding: utf-8 -*- 
# @Time : 2021/1/2 16:06 
# @Author : 王西亚 
# @File : job_dm_inbound_storage_scan_monitor.py
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_dm_ib_storage_sch_scan_monitor(CTimeJob):

    def execute(self) -> str:
        inbound_storage_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select dstid, dsttitle, dstwatchoption, dstscanlasttime
            from dm2_storage 
            where dstwatch = {0} and dsttype = '{1}' and dstscanstatus = {2}      
            '''.format(self.DB_True, self.Storage_Type_InBound, self.ProcStatus_Finished)
        )
        if inbound_storage_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有需要检查的定时任务！')

        for data_index in range(inbound_storage_list.size()):
            storage_id = inbound_storage_list.value_by_name(data_index, 'dstid', '')
            storage_title = inbound_storage_list.value_by_name(data_index, 'dsttitle', '')
            storage_scan_last_time = inbound_storage_list.value_by_name(data_index, 'dstscanlasttime', None)
            storage_scan_option = CUtils.any_2_str(
                inbound_storage_list.value_by_name(data_index, 'dstwatchoption', None))

            CLogger().debug('正在检查存储[{0}]的定时器, 分析目前是否需要启动扫描...'.format(storage_title))

            try:
                # 如果最后一次扫描时间为空, 则立即启动扫描
                if CUtils.equal_ignore_case(storage_scan_last_time, ''):
                    self.start_storage_scan_immediately(storage_id)
                else:
                    # 扫描周期
                    json_storage_scan_option = CJson()
                    json_storage_scan_option.load_json_text(storage_scan_option)
                    storage_scan_period_type = json_storage_scan_option.xpath_one(
                        self.Name_Period,
                        self.Scan_Period_Hour
                    )

                    if CUtils.equal_ignore_case(storage_scan_period_type, self.Scan_Period_Minute):
                        storage_scan_period = json_storage_scan_option.xpath_one(self.Scan_Period_Minute, 15)
                        over_time = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                            '''
                            select trunc(extract(epoch FROM ((now()::timestamp + '-{0} minute') - '{1}'::timestamp))::numeric) as over_time
                            '''.format(storage_scan_period, storage_scan_last_time)
                        )
                    elif CUtils.equal_ignore_case(storage_scan_period_type, self.Scan_Period_Hour):
                        storage_scan_period = json_storage_scan_option.xpath_one(self.Scan_Period_Hour, 1)
                        over_time = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                            '''
                            select trunc(extract(epoch FROM ((now()::timestamp + '-{0} hour') - '{1}'::timestamp))::numeric) as over_time
                            '''.format(storage_scan_period, storage_scan_last_time)
                        )
                    elif CUtils.equal_ignore_case(storage_scan_period_type, self.Scan_Period_Day):
                        storage_scan_period = json_storage_scan_option.xpath_one(self.Scan_Period_Day, 1)
                        over_time = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                            '''
                            select trunc(extract(epoch FROM ((now()::timestamp + '-{0} day') - '{1}'::timestamp))::numeric) as over_time
                            '''.format(storage_scan_period, storage_scan_last_time)
                        )
                    elif CUtils.equal_ignore_case(storage_scan_period_type, self.Scan_Period_Week):
                        storage_scan_period = json_storage_scan_option.xpath_one(self.Scan_Period_Week, 1)
                        over_time = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                            '''
                            select trunc(extract(epoch FROM ((now()::timestamp + '-{0} week') - '{1}'::timestamp))::numeric) as over_time
                            '''.format(storage_scan_period, storage_scan_last_time)
                        )
                    elif CUtils.equal_ignore_case(storage_scan_period_type, self.Scan_Period_Month):
                        storage_scan_period = json_storage_scan_option.xpath_one(self.Scan_Period_Month, 1)
                        over_time = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                            '''
                            select trunc(extract(epoch FROM ((now()::timestamp + '-{0} month') - '{1}'::timestamp))::numeric) as over_time
                            '''.format(storage_scan_period, storage_scan_last_time)
                        )
                    else:  # CUtils.equal_ignore_case(storage_scan_period_type, self.Scan_Period_Year):
                        storage_scan_period = json_storage_scan_option.xpath_one(self.Scan_Period_Year, 1)
                        over_time = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                            '''
                            select trunc(extract(epoch FROM ((now()::timestamp + '-{0} year') - '{1}'::timestamp))::numeric) as over_time
                            '''.format(storage_scan_period, storage_scan_last_time)
                        )

                    if over_time >= 0:
                        CLogger().debug('存储[{0}]的定时器将启动...'.format(storage_title))
                        self.start_storage_scan_immediately(storage_id)
            except Exception as error:
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dm2_storage
                    set dstlastmodifytime=now()
                        , dstscanmemo=:message
                    where dstid = :storage_id   
                    ''',
                    {'storage_id': storage_id, 'message': '系统分析定时扫描条件过程中发现错误, 详细信息为: {0}!'.format(error.__str__())}
                )
                continue

        return CResult.merge_result(self.Success, '本次分析定时扫描任务成功结束！')

    def start_storage_scan_immediately(self, storage_id):
        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage
            set dstscanstatus = {0}
                , dstscanlasttime=now()
                , dstlastmodifytime=now()
                , dstscanmemo=:message
            where dstid = :storage_id   
            '''.format(self.ProcStatus_InQueue),
            {'storage_id': storage_id, 'message': '系统已经检查定时扫描条件, 目前需要启动扫描!'}
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_ib_storage_sch_scan_monitor('', '').execute()
