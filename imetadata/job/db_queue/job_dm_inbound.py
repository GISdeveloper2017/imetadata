# -*- coding: utf-8 -*- 
# @Time : 2020/10/24 12:53 
# @Author : 王西亚 
# @File : job_dm_inbound.py
from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.job.c_dmBaseJob import CDMBaseJob
from imetadata.database.c_factory import CFactory


class job_dm_inbound(CDMBaseJob):
    def get_mission_seize_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsiprocid = '{0}', dsistatus = 2
where dsiid = (
  select dsiid  
  from   dm2_storage_inbound 
  where  dsistatus = 1  
  order by dsiaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage_inbound.dsiid as query_ib_id
  , dm2_storage_inbound.dsidirectory as query_ib_relation_dir
  , dm2_storage_inbound.dsibatchno as query_ib_batchno
  , dm2_storage_inbound.dsiotheroption as query_ib_option
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dstunipath as query_rootpath
  , dm2_storage_directory.dsdid as query_ib_dir_id 
from dm2_storage_inbound 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_inbound.dsistorageid 
  left join dm2_storage_directory on dm2_storage_directory.dsddirectory = dm2_storage_inbound.dsidirectory
where dm2_storage_inbound.dsiprocid = '{0}'
            '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsistatus = 1, dsiprocid = null 
where dsistatus = 2
        '''

    def process_mission(self, dataset) -> str:
        ds_src_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_src_root_path = dataset.value_by_name(0, 'query_rootpath', '')
        ds_src_dir_id = dataset.value_by_name(0, 'query_ib_dir_id', '')

        ds_ib_id = dataset.value_by_name(0, 'query_ib_id', '')
        ds_ib_relation_dir = dataset.value_by_name(0, 'query_ib_relation_dir', '')
        ds_ib_batch_no = dataset.value_by_name(0, 'query_ib_batchno', '')
        ds_ib_option = dataset.value_by_name(0, 'query_ib_option', '')

        src_need_storage_size = self.get_storage_size(ds_src_storage_id, ds_ib_relation_dir, ds_ib_option)
        src_path = CFile.join_file(ds_src_root_path, ds_ib_relation_dir)
        src_dataset_metadata_filename = CFile.join_file(src_path, self.FileName_MetaData_Bus)

        CLogger().debug('入库的目录为: {0}.{1}'.format(ds_ib_id, ds_ib_relation_dir))
        try:
            src_dataset_xml = CXml()
            src_dataset_type = self.Name_Default
            if CFile.file_or_path_exist(src_dataset_metadata_filename):
                src_dataset_xml.load_file(src_dataset_metadata_filename)
                src_dataset_type = CXml.get_element_text(src_dataset_xml.xpath_one(self.Path_MD_Bus_ProductType))
            if CUtils.equal_ignore_case(src_dataset_type, ''):
                src_dataset_type = self.Name_Default

            src_ib_schema = self.get_ib_schema(src_dataset_type, ds_ib_option)
            if src_ib_schema is None:
                return CResult.merge_result(
                    self.Failure,
                    '目录为[{0}.{1}]的数据集类型为[{2}], 未找到匹配的入库模式, 请检查修正后重试!'.format(ds_ib_id, ds_ib_relation_dir,
                                                                             src_dataset_type)
                )

            dest_ib_storage_id, dest_ib_root_path, desc_ib_dir_id, dest_ib_subpath, message = self.get_dest_storage(
                ds_ib_batch_no, src_need_storage_size, ds_ib_option, src_ib_schema, src_dataset_xml)
            if dest_ib_storage_id is None or dest_ib_subpath is None:
                return CResult.merge_result(self.Failure, message)

            src_ib_files_not_locked, message = self.check_src_ib_files_not_locked(ds_src_root_path, src_path)
            if not src_ib_files_not_locked:
                return CResult.merge_result(self.Failure, message)

            # 移动源目录至目标目录
            result = self.src_ib_files_move_to_storage(
                CFile.join_file(ds_src_root_path, ds_ib_relation_dir),
                CFile.join_file(dest_ib_root_path, dest_ib_subpath)
            )
            if not CResult.result_success(result):
                # 利用相同的方法, 把移动的数据, 重新移动回原目录, 这里理论上应该100%成功
                sub_result = self.src_ib_files_move_to_storage(
                    CFile.join_file(dest_ib_root_path, dest_ib_subpath),
                    CFile.join_file(ds_src_root_path, ds_ib_relation_dir)
                )
                if not CResult.result_success(sub_result):
                    sub_result_message = CResult.result_message(sub_result)
                    result_message = CResult.result_message(result)
                    result = CResult.merge_result(self.Failure, '{0}/n{1}'.format(result_message, sub_result_message))
                return result

            # 将源文件的元数据, 移动至目标存储下, 如果出现异常, 则在方法内部rollback
            result = self.src_ib_metadata_move_to_storage(
                ds_src_storage_id, ds_src_dir_id, ds_ib_relation_dir, dest_ib_storage_id, desc_ib_dir_id,
                dest_ib_subpath)
            if not CResult.result_success(result):
                # 利用相同的方法, 把移动的数据, 重新移动回原目录, 这里理论上应该100%成功
                sub_result = self.src_ib_files_move_to_storage(
                    CFile.join_file(dest_ib_root_path, dest_ib_subpath),
                    CFile.join_file(ds_src_root_path, ds_ib_relation_dir)
                )
                if not CResult.result_success(sub_result):
                    sub_result_message = CResult.result_message(sub_result)
                    result_message = CResult.result_message(result)
                    result = CResult.merge_result(self.Failure, '{0}/n{1}'.format(result_message, sub_result_message))
                return result

            return CResult.merge_result(self.Success, '目录为[{0}.{1}]入库成功!'.format(ds_ib_id, ds_ib_relation_dir))
        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '目录为[{0}.{1}]入库出现异常! 错误原因为: {2}'.format(ds_ib_id, ds_ib_relation_dir, error.__str__())
            )

    def get_storage_size(self, storage_id: str, relation_dir: str, ib_option) -> int:
        """
        获取指定存储指定路径下的数据所需要的存储量
        :param ib_option: 入库的个性化要求, 其中包含是全部入库, 还是质检通过的入库, 或者人工选择后入库等配置选项, 会影响到存储大小的计算
        :param storage_id:
        :param relation_dir:
        :return:
        """
        all_file_size = 0

        sql_stat_not_inbound_file_size = '''
        select sum(dm2_storage_file.dsffilesize)
        from dm2_storage_file left join dm2_storage_directory on dm2_storage_file.dsfdirectoryid = dm2_storage_directory.dsdid
        where dm2_storage_directory.dsdstorageid = :dsdStorageID
            and position(:dsdSubDirectory in dm2_storage_directory.dsddirectory) = 1
        '''
        dataset = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            sql_stat_not_inbound_file_size,
            {'dsdStorageID': storage_id, 'dsdSubDirectory': relation_dir}
        )
        if not dataset.is_empty():
            all_file_size = dataset.value_by_index(0, 0, 0)

        not_inbound_file_size = 0
        sql_stat_not_inbound_file_size = '''
        select sum(dm2_storage_obj_detail.dodfilesize)
        from dm2_storage_obj_detail 
            left join dm2_storage_object on dm2_storage_object.dsoid = dm2_storage_obj_detail.dodobjectid
        where (
            dm2_storage_object.dsoid in (
                select dsd_object_id
                from dm2_storage_directory
                where dsdstorageid = :StorageID 
                    and dsd_object_id is not null
                    and position(:SubDirectory in dsddirectory) = 1
            ) or dm2_storage_object.dsoid in (
                select dsf_object_id
                from dm2_storage_file
                where dsfdirectoryid in (
                    select dsdid
                    from dm2_storage_directory
                    where dsdstorageid = :StorageID and position(:SubDirectory in dsddirectory) = 1
                )
            )
        ) and (
            coalesce(
                json_extract_path_text(
                    dm2_storage_object.dsootheroption, 
                    'inbound', 'allow'
                ), 
                'pass'
            ) = 'pass'
        )
        '''
        dataset = CFactory().give_me_db(self.get_mission_db_id()).all_row(
            sql_stat_not_inbound_file_size,
            {'StorageID': storage_id, 'SubDirectory': relation_dir}
        )
        if not dataset.is_empty():
            not_inbound_file_size = dataset.value_by_index(0, 0, 0)

        return all_file_size - not_inbound_file_size

    def get_ib_schema(self, dataset_type, ib_option):
        """
        根据数据集类型, 获取系统设置中的最佳入库模式
        :param ib_option: 其他入库的特殊要求
        :param dataset_type:
        :return:
        """
        ib_schema_list = settings.application.xpath_one(self.Path_Setting_MetaData_Schema_Special, [])
        ib_schema_default = settings.application.xpath_one(self.Path_Setting_MetaData_Schema_Default, None)
        for ib_schema in ib_schema_list:
            ib_schema_id = CUtils.dict_value_by_name(ib_schema, self.Name_ID, '')
            if CUtils.equal_ignore_case(ib_schema_id, dataset_type):
                return ib_schema
        else:
            return ib_schema_default

    def get_dest_storage(self, ib_batch_no, need_storage_size, ib_option, ib_schema, dataset_xml):
        """
        计算哪一个存储最合适, 以及入库后的子目录, 可以考虑如下因素:
        1. 批次
        1. 所需要的存储量
        1. 业务数据集内的属性
        :param ib_option:
        :param need_storage_size: 所需的存储量
        :param ib_batch_no: 批次编号
        :param ib_schema: 入库模式
        :param dataset_xml: 业务数据集的xml
        :return:
        """

        storage_id = ''
        ib_schema_storage_type = CJson.dict_attr_by_path(ib_schema, 'storage.type',
                                                         self.InBound_Storage_Match_Mode_Auto)
        if CUtils.equal_ignore_case(ib_schema_storage_type, self.InBound_Storage_Match_Mode_Set):
            storage_id = CJson.dict_attr_by_path(ib_schema, 'storage.id', '')

        if CUtils.equal_ignore_case(storage_id, ''):
            sql_available_storage = '''
            select dm2_storage.dstid, dm2_storage.dsttitle, dm2_storage.dst_volumn_max, dm2_storage.dst_volumn_max - coalesce(stat.file_size_sum, 0) as free_space
            from dm2_storage left join (
                select dsfstorageid, sum(dsffilesize) as file_size_sum
                from dm2_storage_file left join dm2_storage
                    on dm2_storage_file.dsfstorageid = dm2_storage.dstid
                where dm2_storage.dsttype = 'core'
                group by dsfstorageid
                ) stat on dm2_storage.dstid = stat.dsfstorageid
            where dm2_storage.dsttype = 'core'
            order by dm2_storage.dst_volumn_max desc        
            '''
            ds_available_storage = CFactory().give_me_db(self.get_mission_db_id()).all_row(sql_available_storage)

            for storage_index in range(0, ds_available_storage.size()):
                storage_title = ds_available_storage.value_by_name(storage_index, 'dsttitle', '')
                storage_volumn_max = ds_available_storage.value_by_name(storage_index, 'dst_volumn_max', 0)
                storage_volumn_free = ds_available_storage.value_by_name(storage_index, 'free_space', 0)
                storage_id = ds_available_storage.value_by_name(storage_index, 'dstid', '')

                if storage_volumn_max <= 0:
                    CLogger().debug('存储[{0}]的存储空间没有限制, 系统将把本批数据入库到该存储下'.format(storage_title))
                    break
                elif storage_volumn_free > need_storage_size:
                    CLogger().debug(
                        '存储[{0}]的剩余存储空间为[{1}], 本批数据存储所需空间为[{2}], 系统将把本批数据入库到该存储下'.format(
                            storage_title, storage_volumn_free, need_storage_size
                        )
                    )
                    break

        ib_schema_storage_path = CJson.dict_attr_by_path(ib_schema, 'path', '')
        ib_schema_storage_path = CUtils.replace_placeholder(ib_schema_storage_path, {'aa': 'bb'})

        return \
            '1', \
            '/Users/wangxiya/Documents/我的测试数据/1.入库存储', \
            '1', \
            '{0}/{1}'.format(
                CUtils.any_2_str(CUtils.dict_value_by_name(ib_schema, self.Name_ID, self.Name_Default)).lower().strip(),
                ib_batch_no
            ), \
            'success'

    def check_src_ib_files_not_locked(self, root_path, path):
        """
        检测指定目录下的文件是否没有被锁定
        1. 只有所有文件都没有被锁定, 则返回True
        1. 如果有任何一个文件被锁定, 则返回False, 而且把文件信息写入message中返回
        :param root_path:
        :param path:
        :return:
        """
        return True, ''

    def src_ib_files_move_to_storage(self, src_path, dest_path):
        """
        移动源文件到目标路径下
        . 注意: 在将源文件移动至目标目录下时, 需要保留原相对目录位置信息
        :param src_path:
        :param dest_path:
        :return:
        """
        return ''

    def src_ib_metadata_move_to_storage(self, src_storage_id, src_dir_id, src_ib_relation_dir, dest_ib_storage_id,
                                        desc_ib_dir_id, dest_ib_subpath):
        """
        将源文件的元数据, 移动至目标存储下

        :param src_storage_id:
        :param src_dir_id:
        :param src_ib_relation_dir:
        :param dest_ib_storage_id:
        :param desc_ib_dir_id:
        :param dest_ib_subpath:
        :return:
        """
        return ''


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound('', '').execute()
