# -*- coding: utf-8 -*- 
# @Time : 2020/9/15 12:54 
# @Author : 王西亚 
# @File : job_dm_file2object.py

from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFileInfo import CDMFileInfo
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_file2object(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_file 
set dsfprocessid = '{0}', dsfscanstatus = dsfscanstatus / 10 * 10 + {1}
where dsfid = (
  select dsfid  
  from   dm2_storage_file 
  where  dsfscanstatus % 10 = {2} 
  order by dsfaddtime 
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
    coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
  , dm2_storage_directory.dsddirectory as query_subpath
  , dm2_storage.dstid as query_storage_id
  , dm2_storage_file.dsfid as query_file_id
  , dm2_storage_file.dsfdirectoryid as query_directory_id
  , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_file.dsffilerelationname as query_file_full_name
  , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_directory.dsddirectory as query_file_full_path
  , dm2_storage_file.dsffilename as query_file_name
  , dm2_storage_file.dsffilemainname as query_file_main_name
  , dm2_storage_file.dsfext as query_file_ext
  , dm2_storage_file.dsffilemodifytime as query_file_modifytime
  , dm2_storage_file.dsffilesize as query_file_size
  , dm2_storage_file.dsf_object_type as query_file_object_type
  , dm2_storage_file.dsf_object_confirm as query_file_object_confirm
  , dm2_storage_file.dsf_object_id as query_file_object_id
  , dm2_storage_file.dsfparentobjid as query_dir_parent_objid
  , dm2_storage_file.dsfscanstatus / 10 as retry_times
  , dm2_storage_file.dsfscanmemo as last_process_memo
from dm2_storage, dm2_storage_directory, dm2_storage_file
where dm2_storage.dstid = dm2_storage_directory.dsdstorageid 
  and dm2_storage_file.dsfdirectoryid = dm2_storage_directory.dsdid
  and dm2_storage_file.dsfprocessid ='{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_file 
set dsfscanstatus = {0}, dsfprocessid = null 
where dsfscanstatus % 10 = {1}
        '''.format(self.ProcStatus_InQueue, self.ProcStatus_Processing)

    def process_mission(self, dataset) -> str:
        ds_subpath = dataset.value_by_name(0, 'query_subpath', '')
        ds_file_name_with_path = dataset.value_by_name(0, 'query_file_full_name', '')
        ds_dir_id = dataset.value_by_name(0, 'query_dir_id', '')
        ds_file_id = dataset.value_by_name(0, 'query_file_id', '')
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_owner_obj_id = dataset.value_by_name(0, 'query_dir_parent_objid', '')
        CLogger().debug('处理的文件为: {0}.{1}'.format(ds_file_id, ds_file_name_with_path))

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
            self.update_file_status(ds_file_id, process_result, self.ProcStatus_Error)
            return process_result

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

            file_obj = CDMFileInfo(
                self.FileType_File,
                ds_file_name_with_path,
                ds_storage_id,
                ds_file_id,
                ds_dir_id,
                ds_owner_obj_id,
                self.get_mission_db_id(),
                ds_rule_content
            )

            if not file_obj.file_existed:
                file_obj.db_update_status_on_file_invalid()
                return CResult.merge_result(CResult.Success, '文件[{0}]不存在, 在设定状态后, 顺利结束!'.format(ds_file_name_with_path))
            else:
                file_obj.db_file2object()

            result = CResult.merge_result(CResult.Success, '文件[{0}]的识别过程顺利完成!'.format(ds_file_name_with_path))
            self.update_file_status(ds_file_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                CResult.Failure,
                '文件[{0}]的识别过程出现错误, 详细情况: {1}!'.format(ds_file_name_with_path, error.__str__())
            )
            self.update_file_status(ds_file_id, result)
            return result

    def update_file_status(self, file_id, result, status=None):
        if status is not None:
            sql_update_file_status = '''
            update dm2_storage_file
            set dsfscanstatus = :status
                , dsflastmodifytime = now()
                , dsfscanmemo = :memo
            where dsfid = :dsfid
            '''
        elif CResult.result_success(result):
            sql_update_file_status = '''
            update dm2_storage_file
            set dsfscanstatus = {0}
                , dsflastmodifytime = now()
                , dsfscanmemo = :memo
            where dsfid = :dsfid
            '''.format(self.ProcStatus_Finished)
        else:
            sql_update_file_status = '''
            update dm2_storage_file
            set dsfscanstatus = (dsfscanstatus / 10 + 1) * 10 + {0},
                , dsflastmodifytime = now()
                , dsfscanmemo = :memo
            where dsfid = :dsfid
            '''.format(self.ProcStatus_InQueue)
        params = dict()
        params['dsfid'] = file_id
        params['memo'] = CResult.result_message(result)
        params['status'] = status
        CFactory().give_me_db(self.get_mission_db_id()).execute(sql_update_file_status, params)


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_file2object('', '').execute()
