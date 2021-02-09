#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time : 2020/8/12 17:28
# @Author : 王西亚
# @File : job_dm_root_parser.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_exceptions import DBException
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_root_parser(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage 
set dstprocessid = '{0}', dstscanstatus = dstscanstatus / 10 * 10 + {2}
where dstid = (
  select dstid  
  from   dm2_storage 
  where  dstscanstatus % 10 = {3} and dsttype = '{1}'
  limit 1
  for update skip locked
)
        '''.format(
            self.SYSTEM_NAME_MISSION_ID,
            self.Storage_Type_Mix,
            self.ProcStatus_Processing,
            self.ProcStatus_InQueue
        )

    def get_mission_info_sql(self):
        return '''
select dstid as root_directory_id
    , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as root_directory 
    , dstscanstatus / 10 as retry_times,
    , dstscanmemo as last_process_memo,
from dm2_storage where dstprocessid = '{0}'        
        '''.format(
            self.SYSTEM_NAME_MISSION_ID
        )

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage 
set dstscanstatus = {0}, dstprocessid = null 
where dstscanstatus % 10 = {1}
        '''.format(
            self.ProcStatus_InQueue,
            self.ProcStatus_Processing
        )

    def process_mission(self, dataset):
        storage_id = dataset.value_by_name(0, 'root_directory_id', '')
        storage_root_path = dataset.value_by_name(0, 'root_directory', '')

        CLogger().debug('storage_id: {0}'.format(storage_id))

        ds_retry_times = dataset.value_by_name(0, 'retry_times', 0)
        if ds_retry_times >= self.abnormal_job_retry_times():
            ds_last_process_memo = CUtils.any_2_str(dataset.value_by_name(0, 'last_process_memo', None))
            process_result = CResult.merge_result(
                self.Failure,
                '{0}, \n系统已经重试{1}次, 仍然未能解决, 请人工检查修正后重试!'.format(
                    ds_last_process_memo,
                    ds_retry_times
                )
            )
            self.update_status(storage_id, process_result, self.ProcStatus_Error)
            return process_result

        sql_check_root_storage_dir_exist = '''
        select dsdid
        from dm2_storage_directory
        where dsdid = :dsdid
        '''

        sql_update_root_storage_dir = '''
        update dm2_storage_directory
        set dsdParentID = '-1', dsdDirectory = '', dsdDirtype = {1}
            , dsdDirectoryName = '', dsdPath = ''
            , dsdDirCreateTime = :dsddircreatetime, dsdDirLastModifyTime = :dsddirlastmodifytime
            , dsdLastModifyTime = Now(), dsd_directory_valid = {0}
        where dsdid = :dsdid
        '''.format(self.File_Status_Unknown, self.Dir_Type_Root)

        sql_insert_root_storage_dir = '''
        insert into dm2_storage_directory(
            dsdid, dsdparentid, dsdstorageid, dsddirectory, dsddirtype, dsdlastmodifytime
            , dsddirectoryname, dsd_directory_valid, dsdpath, dsddircreatetime, dsddirlastmodifytime)
        values(:dsdid, '-1', :dsdStorageID, '', {1}, Now()
            , '', {0}, '', :dsddircreatetime, :dsddirlastmodifytime
        )
        '''.format(self.File_Status_Unknown, self.Dir_Type_Root)

        try:
            db = CFactory().give_me_db(self.get_mission_db_id())
            params = dict()
            params['dsdid'] = storage_id
            params['dsdStorageID'] = storage_id
            if CFile.file_or_path_exist(storage_root_path):
                params['dsdDirCreateTime'] = CFile.file_modify_time(storage_root_path)
                params['dsddirlastmodifytime'] = CFile.file_modify_time(storage_root_path)

            if db.if_exists(sql_check_root_storage_dir_exist, params):
                db.execute(sql_update_root_storage_dir, params)
            else:
                db.execute(sql_insert_root_storage_dir, params)
            process_result = CResult.merge_result(CResult.Success, '存储扫描处理成功')
            self.update_status(storage_id, process_result)
            return process_result
        except DBException as err:
            process_result = CResult.merge_result(CResult.Exception, '存储扫描失败, 原因为{0}'.format(err.__str__))
            self.update_status(storage_id, process_result)
            return process_result

    def update_status(self, storage_id, result, status=None):
        if status is not None:
            sql_update_status = '''
            update dm2_storage
            set 
                dstscanstatus = :status,
                dstscanmemo = :memo,
                dstlastmodifytime = now()
            where dstid = :dstid
            '''
        elif CResult.result_success(result):
            sql_update_status = '''
            update dm2_storage
            set 
                dstscanstatus = {0},
                dstscanmemo = :memo,
                dstlastmodifytime = now()
            where dstid = :dstid
            '''.format(self.ProcStatus_Finished)
        else:
            sql_update_status = '''
            update dm2_storage
            set 
                dstscanstatus = (dstscanstatus / 10 + 1) * 10 + {0},
                dstscanmemo = :memo,
                dstlastmodifytime = now()
            where dstid = :dstid
            '''.format(self.ProcStatus_InQueue)
        params = dict()
        params['dstid'] = storage_id
        params['memo'] = CResult.result_message(result)
        params['status'] = status
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_status, params)


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_root_parser('', '').execute()
