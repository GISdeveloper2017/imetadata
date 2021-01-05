# -*- coding: utf-8 -*- 
# @Time : 2021/1/2 18:24 
# @Author : 王西亚 
# @File : job_dm_ib_storage_scan_monitor.py
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.database.c_factory import CFactory
from imetadata.schedule.job.c_timeJob import CTimeJob


class job_dm_ib_storage_scan_monitor(CTimeJob):

    def execute(self) -> str:
        inbound_storage_list = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            '''
            select dstid, dsttitle
            from dm2_storage 
            where dsttype = '{0}' and dstscanstatus = {1}      
            '''.format(self.Storage_Type_InBound, self.ProcStatus_InQueue)
        )
        if inbound_storage_list.is_empty():
            return CResult.merge_result(CResult.Success, '本次没有发现需要启动入库的任务！')

        for data_index in range(inbound_storage_list.size()):
            storage_id = inbound_storage_list.value_by_name(data_index, 'dstid', '')
            storage_title = inbound_storage_list.value_by_name(data_index, 'dsttitle', '')

            CLogger().debug('正在检查和启动存储[{0}]的定时扫描...'.format(storage_title))

            try:
                if self.inbound_mission_existed(storage_id):
                    self.update_storage_status(
                        storage_id,
                        self.ProcStatus_Finished,
                        '当前存储下发现正在进行中的入库任务, 本次定时扫描将被忽略! '
                    )
                else:
                    self.create_inbound_mission(storage_id)
                    self.update_storage_status(
                        storage_id,
                        self.ProcStatus_Finished,
                        '系统已创建入库批次, 启动扫描! '
                    )
            except Exception as error:
                CFactory().give_me_db(self.get_mission_db_id()).execute(
                    '''
                    update dm2_storage
                    set dstscanstatus = {0}
                        , dstlastmodifytime=now()
                        , dstscanmemo=:message
                    where dstid = :storage_id
                    '''.format(self.ProcStatus_Error),
                    {'storage_id': storage_id, 'message': '系统启动扫描任务过程中出现错误, 详细信息为: {0}!'.format(error.__str__())}
                )
                continue

        return CResult.merge_result(self.Success, '本次分析定时扫描任务成功结束！')

    def update_storage_status(self, storage_id, scan_status, message):
        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage
            set dstscanstatus = {0}
                , dstlastmodifytime=now()
                , dstscanmemo=:message
            where dstid = :storage_id   
            '''.format(scan_status),
            {'storage_id': storage_id, 'message': message}
        )

    def create_inbound_mission(self, storage_id):
        database = CFactory().give_me_db(self.get_mission_db_id())
        new_batch_no = database.seq_next_value(self.Seq_Type_Date_AutoInc)
        database.execute(
            '''
            insert into dm2_storage_inbound(dsiid, dsistorageid, dsidirectory, dsibatchno, dsidirectoryid, dsistatus) 
            VALUES(:dsiid, :storageid, :directory, :batch_no, :directory_id, :status) 
            ''',
            {
                'dsiid': CUtils.one_id(),
                'storageid': storage_id,
                'directory': '',
                'batch_no': new_batch_no,
                'directory_id': CUtils.one_id(),
                'status': self.IB_Status_QI_InQueue
            }
        )

    def inbound_mission_existed(self, storage_id):
        return CFactory().give_me_db(self.get_mission_db_id()).if_exists(
            '''
            select dsiid
            from dm2_storage_inbound
            where dsistorageid = :storage_id
                and 
                (
                    dsistatus <> {0}
                )
            '''.format(self.ProcStatus_Finished),
            {'storage_id': storage_id}
        )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_ib_storage_scan_monitor('', '').execute()
