# -*- coding: utf-8 -*- 
# @Time : 2020/9/12 09:31 
# @Author : 王西亚 
# @File : job_dm_path2object.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmPathInfo import CDMPathInfo
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_path2object(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdprocessid = '{0}', dsdscanstatus = dsdscanstatus / 10 * 10 + {1}
where dsdid = (
  select dsdid  
  from   dm2_storage_directory 
  where  dsdscanstatus % 10 = {2} and dsddirtype <> '2'
  order by dsdaddtime 
  limit 1
  for update skip locked
)
        '''.format(
            self.SYSTEM_NAME_MISSION_ID,
            self.ProcStatus_Processing,
            self.ProcStatus_InQueue
        )

    def get_mission_info_sql(self) -> str:
        return '''
select 
    coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_root_path
  , dm2_storage_directory.dsdparentid as query_dir_parent_id
  , dm2_storage_directory.dsddirectory as query_subpath
  , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_directory.dsdpath as query_dir_full_path
  , dm2_storage_directory.dsddirectoryname as query_subpath_name
  , dm2_storage_directory.dsdid as query_dir_id
  , dm2_storage_directory.dsddirtype as query_dir_type
  , dm2_storage_directory.dsddirlastmodifytime as query_dir_lastmodifytime
  , dm2_storage.dstid as query_storage_id
  , dm2_storage_directory.dsd_object_type as query_dir_object_type
  , dm2_storage_directory.dsd_object_confirm as query_dir_object_confirm
  , dm2_storage_directory.dsd_object_id as query_dir_object_id
  , dm2_storage_directory.dsdscandirstatus as query_dir_ScanDirStatus
  , dm2_storage_directory.dsdparentobjid as query_dir_parent_objid
  , dm2_storage_object.dsoobjecttype as query_dir_parent_objtype
  , dm2_storage_directory.dsdscanstatus / 10 as retry_times
  , dm2_storage_directory.dsdscanmemo as last_process_memo
from dm2_storage_directory 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  left join dm2_storage_object on dm2_storage_object.dsoid = dm2_storage_directory.dsdparentobjid
where dm2_storage_directory.dsdprocessid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_directory 
set dsdscanstatus = {0}, dsdprocessid = null 
where dsdscanstatus % 10 = {1}
        '''.format(self.ProcStatus_InQueue, self.ProcStatus_Processing)

    def process_mission(self, dataset) -> str:
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
        ds_root_path = dataset.value_by_name(0, 'query_root_path', '')
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_id = dataset.value_by_name(0, 'query_dir_id', '')
        owner_obj_id = dataset.value_by_name(0, 'query_dir_parent_objid', '')
        parent_id = dataset.value_by_name(0, 'query_dir_parent_id', '')

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
            self.update_dir_status(ds_id, process_result, self.ProcStatus_Error)
            return process_result

        if CUtils.equal_ignore_case(ds_subpath, ''):
            result = CResult.merge_result(CResult.Success, '根目录[{0}]不支持识别为对象, 当前流程被忽略!')
            self.update_dir_status(ds_id, result)
            return result

        ds_path_full_name = CFile.join_file(ds_root_path, ds_subpath)
        CLogger().debug('处理的子目录为: {0}'.format(ds_path_full_name))

        try:
            sql_get_rule = '''
                select dsdScanRule
                from dm2_storage_directory
                where dsdStorageid = :dsdStorageID and Position(dsddirectory || '{0}' in :dsdDirectory) = 1
                    and dsdScanRule is not null
                order by dsddirectory desc
                limit 1
                '''.format(CFile.sep())
            rule_ds = CFactory().give_me_db(self.get_mission_db_id()).one_row(
                sql_get_rule,
                {
                    'dsdStorageID': ds_storage_id,
                    'dsdDirectory': ds_subpath
                }
            )
            ds_rule_content = rule_ds.value_by_name(0, 'dsdScanRule', '')

            path_obj = CDMPathInfo(self.FileType_Dir, ds_path_full_name, ds_storage_id, ds_id, parent_id, owner_obj_id,
                                   self.get_mission_db_id(), ds_rule_content)
            if not path_obj.file_existed:
                path_obj.db_update_status_on_path_invalid()
                return CResult.merge_result(
                    CResult.Success,
                    '目录[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_path_full_name)
                )
            else:
                path_obj.db_check_and_update_metadata_rule(
                    CFile.join_file(ds_path_full_name, self.FileName_MetaData_Rule)
                )
                path_obj.db_path2object()

            result = CResult.merge_result(CResult.Success, '目录[{0}]处理顺利完成!'.format(ds_path_full_name))
            self.update_dir_status(ds_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                CResult.Failure,
                '目录[{0}]识别过程出现错误, 详细情况: {1}!'.format(ds_path_full_name, error.__str__())
            )
            self.update_dir_status(ds_id, result)
            return result

    def update_dir_status(self, dir_id, result, status=None):
        if status is not None:
            sql_update_directory_status = '''
            update dm2_storage_directory
            set 
                dsdscanstatus = :status,
                dsdscanmemo = :memo,
                dsdlastmodifytime = now()
            where dsdid = :dsdid
            '''
        elif CResult.result_success(result):
            sql_update_directory_status = '''
            update dm2_storage_directory
            set 
                dsdscanstatus = {0},
                dsdscanmemo = :memo, 
                dsdlastmodifytime = now()
            where dsdid = :dsdid
            '''.format(self.ProcStatus_Finished)
        else:
            sql_update_directory_status = '''
            update dm2_storage_directory
            set 
                dsdscanstatus = (dsdscanstatus / 10 + 1) * 10 + {0},
                dsdscanmemo = :memo, 
                dsdlastmodifytime = now()
            where dsdid = :dsdid
            '''.format(self.ProcStatus_InQueue)
        params = dict()
        params['dsdid'] = dir_id
        params['memo'] = CResult.result_message(result)
        params['status'] = status
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_directory_status, params)


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_path2object('', '').execute()
