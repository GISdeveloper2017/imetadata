# -*- coding: utf-8 -*- 
# @Time : 2020/11/19 12:57 
# @Author : 王西亚 
# @File : job_dm_inbound_qi.py

from imetadata.base.c_file import CFile
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.fileinfo.c_dmPathInfo import CDMPathInfo
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_inbound_qi(CDMBaseJob):

    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsiprocid = '{0}', dsiStatus = {1}
where dsiid = (
  select dsiid  
  from   dm2_storage_inbound 
  where  dsistatus = {2}  
  order by dsiaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID, self.IB_Status_QI_Dir_Scan_Creating, self.IB_Status_QI_InQueue)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage_inbound.dsiid as query_ib_id
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dsttitle as query_storage_title
  , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
  , dm2_storage_inbound.dsidirectory as query_ib_relation_dir
  , dm2_storage_inbound.dsidirectoryid as query_ib_relation_dir_id
  , dm2_storage_inbound.dsibatchno as query_ib_batchno
  , dm2_storage_inbound.dsiotheroption as query_ib_option
from dm2_storage_inbound 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_inbound.dsistorageid 
where dm2_storage_inbound.dsiprocid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsiStatus = {0}, dsiprocid = null 
where dsiStatus = {1}
        '''.format(self.IB_Status_QI_InQueue, self.IB_Status_QI_Dir_Scan_Creating)

    def process_mission(self, dataset) -> str:
        """
        :param dataset:
        :return:
        """
        ds_ib_id = dataset.value_by_name(0, 'query_ib_id', '')
        ds_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_storage_title = dataset.value_by_name(0, 'query_storage_title', '')
        ds_storage_root_dir = dataset.value_by_name(0, 'query_rootpath', '')
        ds_ib_directory_name = dataset.value_by_name(0, 'query_ib_relation_dir', '')
        ds_ib_directory_id = dataset.value_by_name(0, 'query_ib_relation_dir_id', '')
        # 按需要再开启
        # ds_ib_option = CUtils.any_2_str(dataset.value_by_name(0, 'query_ib_option', ''))

        CLogger().debug('正在入库的是存储[{0}]下的目录[{1}]'.format(ds_storage_title,
                                                        CFile.join_file(ds_storage_root_dir, ds_ib_directory_name)))
        ib_full_directory = CFile.join_file(ds_storage_root_dir, ds_ib_directory_name)

        try:
            super().clear_anything_in_directory(ds_storage_id, ds_ib_directory_name)
            metadata_rule_file_name = CFile.join_file(ib_full_directory, self.FileName_MetaData_Rule)
            metadata_rule_content = ''
            if CFile.file_or_path_exist(metadata_rule_file_name):
                try:
                    metadata_rule_content = CXml.file_2_str(metadata_rule_file_name)
                    CLogger().debug(
                        '在目录[{0}]下发现元数据规则文件, 它的内容为[{1}]'.format(ib_full_directory, metadata_rule_content)
                    )
                except Exception as error:
                    result = CResult.merge_result(
                        self.Failure,
                        '在目录[{0}]下发现元数据规则文件, 但它的格式不合法, 详细错误为: [{1}]'.format(
                            ib_full_directory,
                            error.__str__()
                        )
                    )
                    self.update_inbound_qi_result(ds_ib_id, result)
                    return result

            path_obj = CDMPathInfo(
                self.FileType_Dir,
                ib_full_directory,
                ds_storage_id,
                ds_ib_directory_id,
                ds_storage_id,
                None,
                self.get_mission_db_id(),
                metadata_rule_content
            )

            if path_obj.white_black_valid():
                path_obj.db_check_and_update()

                result = CResult.merge_result(
                    self.Success,
                    '目录[{0}]的入库质检任务创建成功, 系统正在质检, 请稍后...'.format(ib_full_directory)
                )
            else:
                result = CResult.merge_result(
                    self.Failure,
                    '目录[{0}]未通过黑白名单检验, 不允许入库! '.format(ib_full_directory)
                )

            self.update_inbound_qi_result(ds_ib_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '目录[{0}]的入库质检任务创建过程出现错误, 详细错误为: [{1}]'.format(
                    ib_full_directory,
                    error.__str__()
                )
            )
            self.update_inbound_qi_result(ds_ib_id, result)
            return result

    def update_inbound_qi_result(self, notify_id, result):
        CLogger().debug(CResult.result_message(result))
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsiStatus = {0}, dsiprocmemo = :notify_message
                where dsiid = :notify_id   
                '''.format(self.IB_Status_QI_Processing),
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsiStatus = {0}, dsiprocmemo = :notify_message
                where dsiid = :notify_id   
                '''.format(self.IB_Status_QI_Error),
                {'notify_id': notify_id, 'notify_message': CResult.result_message(result)}
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound_qi('', '').execute()
