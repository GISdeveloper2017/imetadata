# -*- coding: utf-8 -*- 
# @Time : 2020/9/23 16:14 
# @Author : 王西亚 
# @File : job_dm_obj_detail.py


from __future__ import absolute_import

from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.business.metadata.base.parser.detail.c_detailParserMng import CDetailParserMng
from imetadata.business.metadata.base.plugins.manager.c_pluginsMng import CPluginsMng
from imetadata.database.c_factory import CFactory


class job_dm_obj_detail(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsodetailparseprocid = '{0}', dsodetailparsestatus = 2
where dsoid = (
  select dsoid  
  from   dm2_storage_object 
  where  dsodetailparsestatus = 1 
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self):
        return '''
select dsoid, dsodatatype, dsoobjecttype, dsoobjectname from dm2_storage_object where dsodetailparseprocid = '{0}'        
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_object 
set dsodetailparsestatus = 1, dsodetailparseprocid = null 
where dsodetailparsestatus = 2
        '''

    def process_mission(self, dataset):
        dso_id = dataset.value_by_name(0, 'dsoid', '')
        dso_data_type = dataset.value_by_name(0, 'dsodatatype', '')
        dso_object_type = dataset.value_by_name(0, 'dsoobjecttype', '')
        dso_object_name = dataset.value_by_name(0, 'dsoobjectname', '')

        CLogger().debug('开始处理对象: {0}.{1}.{2}.{3}的元数据'.format(dso_id, dso_data_type, dso_object_type, dso_object_name))

        ds_file_info = self.get_object_info(dso_id, dso_data_type)

        if ds_file_info.value_by_name(0, 'query_object_valid', self.DB_False) == self.DB_False:
            CFactory().give_me_db(self.get_mission_db_id()).execute('''
                update dm2_storage_object
                set dsodetailparsestatus = 0
                  , dsolastmodifytime = now()
                  , dsodetailparsememo = '文件或目录不存在，元数据无法解析'
                where dsoid = :dsoid
                ''', {'dsoid': dso_id})
            return CResult.merge_result(self.Success, '文件或目录[{0}]不存在，元数据无法解析, 元数据处理正常结束!'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', '')))

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
                'dsdStorageID': ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
                'dsdDirectory': ds_file_info.value_by_name(0, 'query_object_relation_path', '')
            }
        )
        ds_rule_content = rule_ds.value_by_name(0, 'dsScanRule', '')
        file_info_obj = CDMFilePathInfoEx(
            dso_data_type,
            ds_file_info.value_by_name(0, 'query_object_fullname', ''),
            ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
            ds_file_info.value_by_name(0, 'query_object_file_id', ''),
            ds_file_info.value_by_name(0, 'query_object_file_parent_id', ''),
            ds_file_info.value_by_name(0, 'query_object_owner_id', ''),
            self.get_mission_db_id(),
            ds_rule_content
        )

        plugins_obj = CPluginsMng.plugins(file_info_obj, dso_object_type)
        if plugins_obj is None:
            return CResult.merge_result(
                self.Failure,
                '文件或目录[{0}]的类型插件[{1}]不存在，对象详情无法解析, 处理结束!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''),
                    dso_object_type
                )
            )

        try:
            plugins_obj.classified()
            plugins_information = plugins_obj.get_information()

            detail_parser = CDetailParserMng.give_me_parser(
                CUtils.dict_value_by_name(plugins_information, plugins_obj.Plugins_Info_DetailEngine, None),
                dso_id, dso_object_name, file_info_obj,
                plugins_obj.object_detail_file_full_name_list
            )
            process_result = plugins_obj.parser_detail(detail_parser)
            if not CResult.result_success(process_result):
                self.db_update_object_status(dso_id, self.ProcStatus_Error, '文件或目录[{0}]对象详情解析过程出现错误! 错误原因为: {1}'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''), CResult.result_message(process_result)))
                return process_result

            process_result = self.object_copy_stat(
                ds_file_info.value_by_name(0, 'query_object_storage_id', ''),
                dso_id,
                dso_object_name,
                ds_file_info.value_by_name(0, 'query_object_relation_path', '')
            )

            if CResult.result_success(process_result):
                # 更新父对象的容量和最后修改时间
                self.__update_object_owner_object_size_and_modifytime(file_info_obj.owner_obj_id)

                self.db_update_object_status(
                    dso_id,
                    self.ProcStatus_Finished,
                    '文件或目录[{0}]对象详情解析成功结束!'.format(
                        ds_file_info.value_by_name(0, 'query_object_fullname', '')
                    )
                )
                return CResult.merge_result(self.Success, '文件或目录[{0}]对象详情解析成功结束!'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', '')))
            else:
                self.db_update_object_status(dso_id, self.ProcStatus_Error, '文件或目录[{0}]对象详情解析过程出现错误! 错误原因为: {1}'.format(
                    ds_file_info.value_by_name(0, 'query_object_fullname', ''), CResult.result_message(process_result)))
                return process_result
        except Exception as error:
            self.db_update_object_status(dso_id, self.ProcStatus_Error, '文件或目录[{0}]对象详情解析过程出现错误! 错误原因为: {1}'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', ''), error.__str__()))
            return CResult.merge_result(self.Failure, '文件或目录[{0}]对象详情解析过程出现错误! 错误原因为: {1}'.format(
                ds_file_info.value_by_name(0, 'query_object_fullname', ''), error.__str__()))

    def db_update_object_status(self, dso_id, dso_status, memo):
        CFactory().give_me_db(self.get_mission_db_id()).execute('''
            update dm2_storage_object
            set dsodetailparsestatus = :status
              , dsolastmodifytime = now()
              , dsodetailparsememo = :dsodetailparsememo
            where dsoid = :dsoid
            ''', {'dsoid': dso_id, 'dsodetailparsememo': memo, 'status': dso_status})

    def object_copy_stat(self, storage_id, object_id, object_name, object_relation_name):
        try:
            ds_object_stat = CFactory().give_me_db(self.get_mission_db_id()).one_row(
                '''
                select sum(dodfilesize), max(dodfilemodifytime) from dm2_storage_obj_detail where dodobjectid = :object_id
                ''',
                {'object_id': object_id}
            )

            object_size = None
            object_last_modify_time = None
            if not ds_object_stat.is_empty():
                object_size = ds_object_stat.value_by_index(0, 0, 0)
                object_last_modify_time = ds_object_stat.value_by_index(0, 1, None)

            batch_root_relation_dir = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select dsddirectory
                from dm2_storage_directory
                where dsdStorageid = :storage_id and Position(dsddirectory || '{0}' in :directory) = 1
                    and dsddirectory <> ''
                order by dsddirectory 
                limit 1
                '''.format(CFile.sep()),
                {'storage_id': storage_id, 'directory': object_relation_name},
                object_relation_name
            )

            # 更新当前对象的存储大小, 以及最后修改时间
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_object 
                set dso_volumn_now = :object_size, dso_obj_lastmodifytime = :object_last_modify_time
                where dsoid = :object_id
                ''',
                {
                    'object_id': object_id,
                    'object_size': object_size,
                    'object_last_modify_time': object_last_modify_time
                }
            )

            count_copy_same_filename_core = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_directory on dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id 
                    left join dm2_storage on dm2_storage_directory.dsdstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid is not null
                    and dm2_storage.dsttype = '{0}'
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{1}'
                '''.format(self.Storage_Type_Core, self.FileType_Dir),
                {'object_id': object_id, 'object_name': object_name}, 0
            ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_file on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                    left join dm2_storage on dm2_storage_file.dsfstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid is not null
                    and dm2_storage.dsttype = '{0}'
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{1}'
                '''.format(self.Storage_Type_Core, self.FileType_File),
                {'object_id': object_id, 'object_name': object_name}, 0
            )

            count_copy_same_filename_and_size_core = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_directory on dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id 
                    left join dm2_storage on dm2_storage_directory.dsdstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid is not null
                    and dm2_storage.dsttype = '{0}'
                    and dm2_storage_object.dso_volumn_now = :object_size
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{1}'
                '''.format(self.Storage_Type_Core, self.FileType_Dir),
                {'object_id': object_id, 'object_name': object_name, 'object_size': object_size}, 0
            ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_file on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                    left join dm2_storage on dm2_storage_file.dsfstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid is not null
                    and dm2_storage.dsttype = '{0}'
                    and dm2_storage_object.dso_volumn_now = :object_size
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{1}'
                '''.format(self.Storage_Type_Core, self.FileType_File),
                {'object_id': object_id, 'object_name': object_name, 'object_size': object_size}, 0
            )

            count_copy_same_filename_same_batch = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_directory on dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id 
                    left join dm2_storage on dm2_storage_directory.dsdstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid = :storage_id
                    and position(:directory in dm2_storage_directory.dsddirectory) = 1
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{0}'
                '''.format(self.FileType_Dir),
                {
                    'storage_id': storage_id,
                    'object_id': object_id,
                    'object_name': object_name,
                    'directory': batch_root_relation_dir
                }, 0
            ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_file on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                    left join dm2_storage on dm2_storage_file.dsfstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid = :storage_id
                    and position(:directory in dm2_storage_file.dsffilerelationname) = 1
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{0}'
                '''.format(self.FileType_File),
                {
                    'storage_id': storage_id,
                    'object_id': object_id,
                    'object_name': object_name,
                    'directory': batch_root_relation_dir
                }, 0
            )

            count_copy_same_filename_and_size_same_batch = CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_directory on dm2_storage_object.dsoid = dm2_storage_directory.dsd_object_id 
                    left join dm2_storage on dm2_storage_directory.dsdstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid = :storage_id
                    and position(:directory in dm2_storage_directory.dsddirectory) = 1
                    and dm2_storage_object.dso_volumn_now = :object_size
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{0}'
                '''.format(self.FileType_Dir),
                {
                    'storage_id': storage_id,
                    'object_id': object_id,
                    'object_name': object_name,
                    'object_size': object_size,
                    'directory': object_relation_name
                }, 0
            ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
                '''
                select count(dm2_storage_object.dsoid)
                from dm2_storage_object
                    left join dm2_storage_file on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                    left join dm2_storage on dm2_storage_file.dsfstorageid = dm2_storage.dstid 
                where 
                    dm2_storage.dstid = :storage_id
                    and position(:directory in dm2_storage_file.dsffilerelationname) = 1
                    and dm2_storage_object.dso_volumn_now = :object_size
                    and dm2_storage_object.dsoobjectname = :object_name
                    and dm2_storage_object.dsoid <> :object_id
                    and dm2_storage_object.dsodatatype = '{0}'
                '''.format(self.FileType_File),
                {
                    'storage_id': storage_id,
                    'object_id': object_id,
                    'object_name': object_name,
                    'object_size': object_size,
                    'directory': object_relation_name
                }, 0
            )

            json_text = None
            if count_copy_same_filename_and_size_same_batch + \
                    count_copy_same_filename_and_size_core + \
                    count_copy_same_filename_same_batch + count_copy_same_filename_core > 0:
                json_obj = CJson()
                json_obj.load_obj({
                    self.Storage_Type_Core: {
                        self.Name_FileName: count_copy_same_filename_core,
                        '{0}_{1}'.format(self.Name_FileName, self.Name_Size): count_copy_same_filename_and_size_core
                    },
                    self.Storage_Type_InBound: {
                        self.Name_FileName: count_copy_same_filename_same_batch,
                        '{0}_{1}'.format(self.Name_FileName,
                                         self.Name_Size): count_copy_same_filename_and_size_same_batch
                    }
                })
                json_text = json_obj.to_json()

            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_object
                set dsocopystat = :copy_stat
                where dsoid = :dsoid
                ''', {'dsoid': object_id, 'copy_stat': json_text}
            )
            return CResult.merge_result(self.Success, '数据容量统计和数据重复数据分析成功完成! ')
        except Exception as error:
            return CResult.merge_result(self.Failure, '数据容量统计和数据重复数据分析过程出现错误, 详细情况: {0}'.format(error.__str__()))

    def __update_object_owner_object_size_and_modifytime(self, owner_obj_id):
        if CUtils.equal_ignore_case(owner_obj_id, ''):
            return

        ds_object_stat = CFactory().give_me_db(self.get_mission_db_id()).one_row(
            '''
            select sum(dso_volumn_now), max(dso_obj_lastmodifytime) 
            from dm2_storage_object 
            where dsoparentobjid = :object_id
            ''',
            {'object_id': owner_obj_id}
        )

        object_size = None
        object_last_modify_time = None
        if not ds_object_stat.is_empty():
            object_size = ds_object_stat.value_by_index(0, 0, 0)
            object_last_modify_time = ds_object_stat.value_by_index(0, 1, None)

        CFactory().give_me_db(self.get_mission_db_id()).execute(
            '''
            update dm2_storage_object 
            set dso_volumn_now = :object_size, dso_obj_lastmodifytime = :object_last_modify_time
            where dsoid = :object_id
            ''',
            {
                'object_id': owner_obj_id,
                'object_size': object_size,
                'object_last_modify_time': object_last_modify_time
            }
        )



if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_obj_detail('', '').execute()
