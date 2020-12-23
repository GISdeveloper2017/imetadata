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
set dsiprocid = '{0}', dsistatus = {1}
where dsiid = (
  select dsiid  
  from   dm2_storage_inbound 
  where  dsistatus = {2}  
  order by dsiaddtime
  limit 1
  for update skip locked
)
        '''.format(self.SYSTEM_NAME_MISSION_ID, self.IB_Status_IB_Processing, self.IB_Status_IB_InQueue)

    def get_mission_info_sql(self) -> str:
        return '''
select 
    dm2_storage_inbound.dsiid as query_ib_id
  , dm2_storage_inbound.dsidirectory as query_ib_relation_dir
  , dm2_storage_inbound.dsibatchno as query_ib_batchno
  , dm2_storage_inbound.dsiotheroption as query_ib_option
  , dm2_storage.dstid as query_storage_id
  , dm2_storage.dsttype as query_storage_type
  , coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as query_rootpath
  , dm2_storage_directory.dsdid as query_ib_dir_id 
from dm2_storage_inbound 
  left join dm2_storage on dm2_storage.dstid = dm2_storage_inbound.dsistorageid 
  left join dm2_storage_directory 
    on dm2_storage_directory.dsdid = dm2_storage_inbound.dsidirectoryid 
where dm2_storage_inbound.dsiprocid = '{0}'
        '''.format(self.SYSTEM_NAME_MISSION_ID)

    def get_abnormal_mission_restart_sql(self) -> str:
        return '''
update dm2_storage_inbound 
set dsistatus = {0}, dsiprocid = null 
where dsistatus = {1}
        '''.format(self.IB_Status_IB_InQueue, self.IB_Status_IB_Processing)

    def process_mission(self, dataset, is_retry_mission: bool) -> str:
        """
        详细算法复杂, 参见readme.md中[### 数据入库调度]章节
        :param dataset:
        :return:
        """
        ds_src_storage_id = dataset.value_by_name(0, 'query_storage_id', '')
        ds_src_storage_type = dataset.value_by_name(0, 'query_storage_type', self.Storage_Type_Mix)
        ds_src_root_path = dataset.value_by_name(0, 'query_rootpath', '')
        ds_src_dir_id = dataset.value_by_name(0, 'query_ib_dir_id', '')

        ds_ib_id = dataset.value_by_name(0, 'query_ib_id', '')
        ds_ib_directory_name = dataset.value_by_name(0, 'query_ib_relation_dir', '')
        ds_ib_batch_no = dataset.value_by_name(0, 'query_ib_batchno', '')
        ds_ib_option = dataset.value_by_name(0, 'query_ib_option', '')

        src_need_storage_size = self.get_storage_size(ds_ib_id, ds_src_storage_id, ds_ib_directory_name, ds_ib_option)
        src_path = CFile.join_file(ds_src_root_path, ds_ib_directory_name)
        src_dataset_metadata_filename = CFile.join_file(src_path, self.FileName_MetaData_Bus_21AT)

        CLogger().debug('入库的目录为: {0}.{1}'.format(ds_ib_id, ds_ib_directory_name))
        try:
            # 检查所有文件与元数据是否相符
            all_ib_file_or_path_existed = self.check_all_ib_file_or_path_existed(ds_ib_id)
            if not CResult.result_success(all_ib_file_or_path_existed):
                self.update_ib_result(ds_ib_id, all_ib_file_or_path_existed)
                return all_ib_file_or_path_existed

            # 将数据入库的记录保存到日志中
            result = self.ib_log(ds_ib_id, ds_src_storage_id, ds_ib_directory_name)
            if not CResult.result_success(result):
                self.update_ib_result(ds_ib_id, result)
                return result

            # 如果是在核心存储或混合存储中直接入库, 则仅仅改变元数据状态即可
            if CUtils.equal_ignore_case(ds_src_storage_type, self.Storage_Type_Mix) \
                    or CUtils.equal_ignore_case(ds_src_storage_type, self.Storage_Type_Core):
                result_ib_in_core_or_mix_storage = self.update_ib_data_status_in_core_or_mix_storage(
                    ds_ib_id,
                    ds_src_storage_id,
                    ds_ib_directory_name,
                    ds_src_dir_id
                )
                self.update_ib_result(ds_ib_id, result_ib_in_core_or_mix_storage)
                return result_ib_in_core_or_mix_storage

            # 加载目录下的待入库数据集的元数据文件
            src_dataset_xml = CXml()
            src_dataset_type = self.Name_Default
            if CFile.file_or_path_exist(src_dataset_metadata_filename):
                src_dataset_xml.load_file(src_dataset_metadata_filename)
                src_dataset_type = CXml.get_element_text(src_dataset_xml.xpath_one(self.Path_MD_Bus_ProductType))
            if CUtils.equal_ignore_case(src_dataset_type, ''):
                src_dataset_type = self.Name_Default

            # 获取匹配的入库模式
            src_ib_schema = self.get_ib_schema(src_dataset_type, ds_ib_option)
            if src_ib_schema is None:
                result = CResult.merge_result(
                    self.Failure,
                    '目录为[{0}.{1}]的数据集类型为[{2}], 未找到匹配的入库模式, 请检查修正后重试!'.format(
                        ds_ib_id, ds_ib_directory_name, src_dataset_type)
                )
                self.update_ib_result(ds_ib_id, result)
                return result

            # 计算入库的目标存储\存储根目录\目标子目录在目标存储中的副目录的标识\目标子目录\反馈消息
            dest_ib_storage_id, dest_ib_root_path, desc_ib_dir_id, dest_ib_subpath, message = self.get_dest_storage(
                ds_ib_batch_no, src_need_storage_size, ds_ib_option, src_ib_schema, src_dataset_xml)
            if dest_ib_storage_id is None or dest_ib_subpath is None:
                result = CResult.merge_result(self.Failure, message)
                self.update_ib_result(ds_ib_id, result)
                return result

            dest_ib_subpath = CFile.unify(dest_ib_subpath)
            if CJson.json_attr_value(ds_ib_option, self.Path_IB_Switch_CheckFileLocked, self.DB_False) == self.DB_True:
                src_ib_files_not_locked, message = self.check_src_ib_files_not_locked(ds_src_root_path, src_path)
                if not src_ib_files_not_locked:
                    result = CResult.merge_result(self.Failure, message)
                    self.update_ib_result(ds_ib_id, result)
                    return result

            proc_ib_src_path = CFile.join_file(ds_src_root_path, ds_ib_directory_name)
            proc_ib_dest_path = CFile.join_file(
                CFile.join_file(dest_ib_root_path, dest_ib_subpath),
                ds_ib_directory_name
            )

            # --------------------------------------------------------------至此, 数据入库前的检查处理完毕
            # 移动源目录至目标目录
            result = self.ib_files_move(proc_ib_src_path, proc_ib_dest_path)
            if not CResult.result_success(result):
                # 利用相同的方法, 把移动的数据, 重新移动回原目录, 这里理论上应该100%成功
                sub_result = self.ib_files_move(proc_ib_dest_path, proc_ib_src_path)
                if not CResult.result_success(sub_result):
                    sub_result_message = CResult.result_message(sub_result)
                    result_message = CResult.result_message(result)
                    result = CResult.merge_result(self.Failure, '{0}\n{1}'.format(result_message, sub_result_message))

                self.update_ib_result(ds_ib_id, result)
                return result

            # 将源文件的元数据, 移动至目标存储下, 如果出现异常, 则在方法内部rollback
            result = self.src_ib_metadata_move_to_storage(
                ds_ib_id, ds_src_storage_id, ds_src_dir_id, ds_ib_directory_name, dest_ib_storage_id, desc_ib_dir_id,
                dest_ib_subpath)
            if not CResult.result_success(result):
                # 利用相同的方法, 把移动的数据, 重新移动回原目录, 这里理论上应该100%成功
                sub_result = self.ib_files_move(proc_ib_dest_path, proc_ib_src_path)
                if not CResult.result_success(sub_result):
                    sub_result_message = CResult.result_message(sub_result)
                    result_message = CResult.result_message(result)
                    result = CResult.merge_result(self.Failure, '{0}/n{1}'.format(result_message, sub_result_message))

                self.update_ib_result(ds_ib_id, result)
                return result

            result = CResult.merge_result(self.Success, '目录为[{0}.{1}]入库成功!'.format(ds_ib_id, ds_ib_directory_name))
            self.update_ib_result(ds_ib_id, result)
            return result
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '目录为[{0}.{1}]入库出现异常! 错误原因为: {2}'.format(ds_ib_id, ds_ib_directory_name, error.__str__())
            )
            self.update_ib_result(ds_ib_id, result)
            return result

    def get_storage_size(self, ds_ib_id: str, storage_id: str, relation_dir: str, ib_option) -> int:
        """
        获取指定存储指定路径下的数据所需要的存储量
        . file表中未识别为数据的文件, dsf_object_confirm=2
        . object表中的存储量
        :param ds_ib_id: 入库批次编号: inbound.dsiid
        :param ib_option: 入库的个性化要求, 其中包含是全部入库, 还是质检通过的入库, 或者人工选择后入库等配置选项, 会影响到存储大小的计算
        :param storage_id:
        :param relation_dir:
        :return:
        """
        # 文件中不认识的部分, 加上已经识别的对象的大小
        inbound_file_size = CFactory().give_me_db(self.get_mission_db_id()).one_value(
            '''
            select sum(dsffilesize)
            from dm2_storage_file 
            where dsf_ib_id = :ib_id
                and dsf_object_confirm = 0
            ''',
            {'ib_id': ds_ib_id},
            0
        ) + CFactory().give_me_db(self.get_mission_db_id()).one_value(
            '''
            select sum(dso_volumn_now)
            from dm2_storage_object 
            where dso_ib_id = :ib_id
                and dso_bus_status = '{0}'
            '''.format(self.IB_Bus_Status_InBound),
            {'ib_id': ds_ib_id},
            0
        )

        return inbound_file_size

    def get_ib_schema(self, dataset_type, ib_option):
        """
        根据数据集类型, 获取系统设置中的最佳入库模式
        :param ib_option: 其他入库的特殊要求
        :param dataset_type:
        :return:
        """
        ib_schema_list = settings.application.xpath_one(self.Path_Setting_MetaData_InBound_Schema_Special, [])
        ib_schema_default = settings.application.xpath_one(self.Path_Setting_MetaData_InBound_Schema_Default, None)
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
        dest_ib_storage_id: 目标入库的存储标识, 如果没有满足要求的, 则返回None
        dest_ib_root_path: 目标入库的存储的目录
        desc_ib_dir_id: 入库的父目录的标识, 默认可以等于目标存储的标识
        dest_ib_subpath: 入库的数据的子目录, 如果没有满足要求的, 则返回None
        message: 错误消息
        """

        storage_id = ''
        storage_title = ''
        storage_root_path = ''
        storage_volumn_free = 0
        storage_volumn_max = 0
        ib_schema_storage_type = CJson.dict_attr_by_path(
            ib_schema, 'storage.type',
            self.InBound_Storage_Match_Mode_Auto)
        if CUtils.equal_ignore_case(ib_schema_storage_type, self.InBound_Storage_Match_Mode_Set):
            storage_id = CJson.dict_attr_by_path(ib_schema, 'storage.id', '')
            if not CUtils.equal_ignore_case(storage_id, ''):
                sql_storage = '''
                select dm2_storage.dstid, dm2_storage.dsttitle, 
                    coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as root_path,
                    dm2_storage.dst_volumn_max, dm2_storage.dst_volumn_max - coalesce(stat.file_size_sum, 0) as free_space
                from dm2_storage left join (
                    select dsfstorageid, sum(dsffilesize) as file_size_sum
                    from dm2_storage_file left join dm2_storage
                        on dm2_storage_file.dsfstorageid = dm2_storage.dstid
                    where dm2_storage.dsttype = 'core'
                    group by dsfstorageid
                    ) stat on dm2_storage.dstid = stat.dsfstorageid
                where dm2_storage.dsttype = 'core' and dm2_storage.dstid = :storage_id  
                '''
                ds_available_storage = CFactory().give_me_db(self.get_mission_db_id()).one_row(
                    sql_storage, {'storage_id': storage_id})
                if ds_available_storage.is_empty():
                    return None, None, None, None, '没有找到编号为[{0}]的存储! '.format(storage_id)
                else:
                    storage_volumn_max = ds_available_storage.value_by_name(0, 'dst_volumn_max', 0)
                    storage_volumn_free = ds_available_storage.value_by_name(0, 'free_space', 0)
                    storage_title = ds_available_storage.value_by_name(0, 'dsttitle', '')

                    if storage_volumn_max > 0 and storage_volumn_free < need_storage_size:
                        CLogger().debug(
                            '存储[{0}]的剩余存储空间为[{1}], 本批数据存储所需空间为[{2}], 本批数据无法入库到该存储下!'.format(
                                storage_title, storage_volumn_free, need_storage_size
                            )
                        )
                        return \
                            None, None, None, None, \
                            '存储[{0}]的剩余存储空间为[{1}], 本批数据存储所需空间为[{2}], 本批数据无法入库到该存储下!'.format(
                                storage_title, storage_volumn_free, need_storage_size
                            )

                    storage_root_path = ds_available_storage.value_by_name(0, 'root_path', '')

        if CUtils.equal_ignore_case(storage_id, ''):
            sql_available_storage = '''
            select dm2_storage.dstid, dm2_storage.dsttitle, 
                coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) as root_path,
                dm2_storage.dst_volumn_max, dm2_storage.dst_volumn_max - coalesce(stat.file_size_sum, 0) as free_space
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

                if storage_volumn_max <= 0:
                    storage_id = ds_available_storage.value_by_name(storage_index, 'dstid', '')
                    storage_root_path = ds_available_storage.value_by_name(storage_index, 'root_path', '')
                    CLogger().debug('存储[{0}]的存储空间没有限制, 系统将把本批数据入库到该存储下'.format(storage_title))
                    break
                elif storage_volumn_free > need_storage_size:
                    storage_id = ds_available_storage.value_by_name(storage_index, 'dstid', '')
                    storage_root_path = ds_available_storage.value_by_name(storage_index, 'root_path', '')
                    CLogger().debug(
                        '存储[{0}]的剩余存储空间为[{1}], 本批数据存储所需空间为[{2}], 系统将把本批数据入库到该存储下'.format(
                            storage_title, storage_volumn_free, need_storage_size
                        )
                    )
                    break

        if CUtils.equal_ignore_case(storage_id, ''):
            return \
                None, None, None, None, \
                '本批待入库数据的容量为[{0}], 未找到符合要求的存储, 请检查各个存储的剩余空间!'.format(need_storage_size)

        # 当前字典将用于计算入库到存储中的相对子目录
        params = dict()
        # 将批次信息加入字典
        params['batch_id'] = ib_batch_no
        # 将待入库数据集的元数据信息(一级元素)加入字典
        self.metadata_bus_2_params(dataset_xml, params)
        # 开始用字典重算相对子目录
        try:
            ib_schema_storage_path = CUtils.replace_placeholder(
                CUtils.any_2_str(CJson.dict_attr_by_path(ib_schema, 'path', '')),
                params,
                False
            )
        except Exception as error:
            return \
                None, None, None, None, \
                '本批待入库数据的入库目标目录无法确认, 部分信息未提供, 具体错误信息: [{0}]!'.format(error.__str__())

        if storage_volumn_max <= 0:
            return \
                storage_id, storage_root_path, storage_id, ib_schema_storage_path, \
                '存储[{0}]的存储空间无限制, 本批数据存储所需空间为[{1}], 系统将把本批数据入库到该存储下'.format(
                    storage_title, need_storage_size
                )
        else:
            return \
                storage_id, storage_root_path, storage_id, ib_schema_storage_path, \
                '存储[{0}]的剩余存储空间为[{1}], 本批数据存储所需空间为[{2}], 系统将把本批数据入库到该存储下'.format(
                    storage_title, storage_volumn_free, need_storage_size
                )

    def check_src_ib_files_not_locked(self, root_path, parent_path):
        """
        检测指定目录下的文件是否没有被锁定
        1. 只有所有文件都没有被锁定, 则返回True
        1. 如果有任何一个文件被锁定, 则返回False, 而且把文件信息写入message中返回
        todo(注意) 这里检查所有文件是否被锁定, 在处理切片数据时, 效率会极慢!!!
        :param root_path: 根目录
        :param parent_path: 父目录, 在加入提示信息中时, 需要将父目录加入到反馈信息中
        :return:
        1. 目录下是否全部文件都没有锁定, 都可以入库
        1. 被锁定文件的名称列表
        """
        parent_path = CFile.join_file(root_path, parent_path)
        locked_file_list = CFile.find_locked_file_in_path(parent_path)
        more_locked_file = False
        max_locked_file_count = len(locked_file_list)
        if max_locked_file_count > 3:
            max_locked_file_count = 3
            more_locked_file = True

        message = ''
        for locked_file in locked_file_list:
            message = CUtils.str_append(message, CFile.join_file(parent_path, locked_file))

        if more_locked_file:
            message = CUtils.str_append(message, '...')
        if max_locked_file_count > 0:
            message = CUtils.str_append(message, '被其他应用占用了, 无法入库, 请检查解除锁定后重试入库! ')

        return max_locked_file_count == 0, message

    def ib_files_move(self, src_dir, dest_dir):
        """
        移动源文件到目标路径下
        . 注意: 在将源目录下的文件和子目录, 移动至目标目录下
        todo(优化) 如何得知两个目录在一个存储上, 而使用目录的移动替代. 只有不同的存储, 才使用本方法!!!
        :param dest_dir:
        :param src_dir:
        :return:
        """
        result, failure_file_list = CFile.move_path_to(src_dir, dest_dir)
        if result:
            return CResult.merge_result(self.Success, '源目录[{0}]已经成功的, 完整的移动至目录[{1}]下! '.format(src_dir, dest_dir))
        else:
            more_failure_file = False
            max_failure_file_count = len(failure_file_list)
            if max_failure_file_count > 3:
                max_failure_file_count = 3
                more_failure_file = True

            message = ''
            for failure_file in failure_file_list:
                message = CUtils.str_append(message, failure_file)

            if more_failure_file:
                message = CUtils.str_append(message, '...')
            if max_failure_file_count > 0:
                message = CUtils.str_append(message, '上述数据向核心存储中迁移时出现错误, 请检查后重试入库! ')

            return CResult.merge_result(
                self.Failure,
                '源目录[{0}]想核心存储目录[{1}]下入库时出现错误! \n{2}'.format(src_dir, dest_dir, message)
            )

    def src_ib_metadata_move_to_storage(self, ib_id, src_storage_id, src_dir_id, src_ib_directory_name,
                                        dest_ib_storage_id,
                                        desc_ib_dir_id, dest_ib_subpath):
        """
        将源文件的元数据, 移动至目标存储下

        :param ib_id: 入库记录标识 dm2_storage_inbound.dsiid
        :param src_storage_id: 待入库存储标识 dm2_storage_inbound.dsistorageid
        :param src_dir_id: 入库目录标识
        :param src_ib_directory_name: 入库目录名称
        :param dest_ib_storage_id: 入库目标存储标识
        :param desc_ib_dir_id: 入库目标目录标识
        :param dest_ib_subpath: 入库目标子目录(迁入的子目录)
        :return:
        """
        # 将文件的路径, 修正为新的的路径
        sql_move_file = '''
        update dm2_storage_file
        set dsfstorageid = :dest_storage_id
            , dsffilerelationname = '{0}'||dsffilerelationname
            , dsf_bus_status = '{1}'
        where dsf_ib_id = :ib_id
        '''.format(dest_ib_subpath, self.IB_Bus_Status_Online)
        params_move_file = {
            'ib_id': ib_id
        }

        # 将目录, 更新到目标存储和目录下
        sql_move_directory_metadata = '''
        update dm2_storage_directory
        set dsdstorageid = :dest_storage_id
            , dsddirectory = '{0}'||dsddirectory
            , dsd_bus_status = '{1}'
        where dsd_ib_id = :ib_id
        '''.format(dest_ib_subpath, self.IB_Bus_Status_Online)
        params_move_directory_metadata = {
            'ib_id': ib_id
        }

        # 将目录, 更新到目标存储和目录下
        sql_move_directory_metadata = '''
        update dm2_storage_directory
        set dsdstorageid = :dest_storage_id
            , dsddirectory = '{0}'||dsddirectory
            , dsd_bus_status = '{1}'
        where dsd_ib_id = :ib_id
        '''.format(dest_ib_subpath, self.IB_Bus_Status_Online)
        params_move_directory_metadata = {
            'ib_id': ib_id
        }

        # 将数据附属文件, 更新到目标目录下
        sql_move_obj_detail_metadata = '''
        update dm2_storage_obj_detail
        set dodfilename = '{0}'||dodfilename
        where dodobjectid in 
            (
                select dsoid
                from dm2_storage_object
                where dso_ib_id = :ib_id
            )
        '''.format(dest_ib_subpath)
        params_move_obj_detail_metadata = {
            'ib_id': ib_id
        }

        # 更新对象状态
        sql_move_obj_metadata = '''
        update dm2_storage_object
        set dso_bus_status = '{0}'
        where dso_ib_id = :ib_id
        '''.format(self.IB_Bus_Status_Online)
        params_move_obj_metadata = {
            'ib_id': ib_id
        }

        # 将入库记录中的目标存储标识进行更新
        sql_update_ib_target_storage = '''
        update dm2_storage_inbound
        set dsitargetstorageid = :target_storage_id
        where dsiid = :ib_id
        '''
        params_update_ib_target_storage = {
            'target_storage_id': dest_ib_storage_id,
            'ib_id': ib_id
        }

        commands = [
            (sql_move_file, params_move_file),
            (sql_move_directory_metadata, params_move_directory_metadata),
            (sql_move_obj_detail_metadata, params_move_obj_detail_metadata),
            (sql_move_obj_metadata, params_move_obj_metadata),
            (sql_update_ib_target_storage, params_update_ib_target_storage)
        ]
        try:
            CFactory().give_me_db(self.get_mission_db_id()).execute_batch(commands)
            return CResult.merge_result(self.Success, '元数据迁移成功!')
        except Exception as error:
            return CResult.merge_result(self.Failure, '元数据迁移失败, 错误原因为: [{0}]!'.format(error.__str__()))

    def update_ib_result(self, ib_id, result):
        if CResult.result_success(result):
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsistatus = {0}, dsiprocmemo = :ib_message, dsi_na_status = {1}
                where dsiid = :ib_id   
                '''.format(self.ProcStatus_Finished, self.ProcStatus_InQueue),
                {'ib_id': ib_id, 'ib_message': CResult.result_message(result)}
            )
        else:
            CFactory().give_me_db(self.get_mission_db_id()).execute(
                '''
                update dm2_storage_inbound 
                set dsistatus = {0}, dsiprocmemo = :ib_message
                where dsiid = :ib_id   
                '''.format(self.IB_Status_IB_Error),
                {'ib_id': ib_id, 'ib_message': CResult.result_message(result)}
            )

    def check_all_ib_file_or_path_existed(self, ib_id):
        """
        判断待入库数据的元数据, 与实体数据是否相符
        . 返回CResult
            . 如果全部相符, 则返回True
            . 如果有任何一个不符, 则返回False, 且把不符的文件名通过信息返回
        :param storage_id:
        :param directory_name:
        :return:
        """
        invalid_file_list = []
        more_failure_file = False
        sql_all_ib_file = '''
        select 
            coalesce(dm2_storage.dstownerpath, dm2_storage.dstunipath) || dm2_storage_file.dsffilerelationname as file_name
            , dm2_storage_file.dsffilesize as file_size
            , dm2_storage_file.dsffilemodifytime as file_modify_time
        from dm2_storage_file left join dm2_storage
            on dm2_storage.dstid = dm2_storage_file.dsfstorageid
        where dsf_ib_id = :ib_id       
        '''
        params_all_ib_file = {
            'ib_id': ib_id
        }
        ds_ib_file = CFactory().give_me_db(self.get_mission_db_id()).all_row(sql_all_ib_file, params_all_ib_file)
        for ds_ib_file_index in range(ds_ib_file.size()):
            file_valid = True
            file_name = ds_ib_file.value_by_name(ds_ib_file_index, 'file_name', '')
            if not CUtils.equal_ignore_case(file_name, ''):
                if not CFile.file_or_path_exist(file_name):
                    file_valid = False
                elif not CUtils.equal_ignore_case(
                        CFile.file_modify_time(file_name),
                        ds_ib_file.value_by_name(ds_ib_file_index, 'file_modify_time', '')
                ):
                    file_valid = False
                elif CFile.file_size(file_name) != ds_ib_file.value_by_name(ds_ib_file_index, 'file_size', 0):
                    file_valid = False
            if not file_valid:
                if len(invalid_file_list) <= 3:
                    invalid_file_list.append(file_name)
                else:
                    more_failure_file = True
                    break

        if len(invalid_file_list) > 0:
            message = ''
            for invalid_file in invalid_file_list:
                message = CUtils.str_append(message, invalid_file)
            if more_failure_file:
                message = CUtils.str_append(message, '...')
            message = CUtils.str_append(message, '上述数据与库中记录不统一, 请重新扫描入库! ')

            return CResult.merge_result(self.Failure, message)
        else:
            return CResult.merge_result(self.Success, '所有文件均存在, 且与库中记录统一! ')

    def ib_log(self, ib_id, storage_id, directory_name):
        """
        记录入库的日志
        . 注意: 如用户对入库日志记录有要求, 可在此进行dm2_storage_inbound_log表结构的调整, 和日志记录的完善.
        :param ib_id:
        :param storage_id:
        :param directory_name:
        :return:
        """
        sql_log_clear_old = '''
        delete from dm2_storage_inbound_log where dsilownerid = :ib_id
        '''
        params_log_clear_old = {
            'ib_id': ib_id
        }
        sql_log_ib_file = '''
        insert into dm2_storage_inbound_log(dsilownerid, dsildirectory, dsilfilename, dsilobjectname, dsilobjecttype)
        select
              '{0}' as owner_id
            , dm2_storage_directory.dsddirectory
            , dm2_storage_file.dsffilename
            , dm2_storage_object.dsoobjectname
            , dm2_storage_object.dsoobjecttype
        from dm2_storage_file
            left join dm2_storage on dm2_storage.dstid = dm2_storage_file.dsfstorageid
            left join dm2_storage_directory on dm2_storage_directory.dsdid = dm2_storage_file.dsfdirectoryid
            left join dm2_storage_object on dm2_storage_object.dsoid = dm2_storage_file.dsf_object_id
        where dsf_ib_id = :ib_id
        '''.format(ib_id)
        params_log_ib_file = {
            'ib_id': ib_id
        }
        try:
            CFactory().give_me_db(self.get_mission_db_id()).execute_batch(
                [
                    (sql_log_clear_old, params_log_clear_old),
                    (sql_log_ib_file, params_log_ib_file)
                ]
            )
            return CResult.merge_result(self.Success, '日志记录登记完成!')
        except Exception as error:
            return CResult.merge_result(self.Failure, '日志记录登记出错, 详细原因为: [{0}]'.format(error.__str__()))

    def update_ib_data_status_in_core_or_mix_storage(self, ib_id, storage_id, ib_directory_name, ib_dir_id):
        """
        如果是在线存储或混合存储, 直接将业务状态修改即可
        :param ib_id:
        :param ib_dir_id:
        :param storage_id:
        :param ib_directory_name:
        :return:
        """
        sql_update_file = '''
        update dm2_storage_file
        set dsf_bus_status = '{0}'
        where dsf_ib_id = :ib_id
        '''.format(self.IB_Bus_Status_Online)
        params_update_file = {
            'ib_id': ib_id
        }

        # 更新子目录状态
        sql_update_directory = '''
        update dm2_storage_directory
        set dsd_bus_status = '{0}'
        where dsd_ib_id = :ib_id
        '''.format(self.IB_Bus_Status_Online)
        params_update_directory = {
            'ib_id': ib_id
        }

        # 更新对象状态
        sql_update_object = '''
        update dm2_storage_object
        set dso_bus_status = '{0}'
        where dso_ib_id = :ib_id
        '''.format(self.IB_Bus_Status_Online)
        params_update_object = {
            'ib_id': ib_id
        }

        # 将入库记录中的目标存储标识进行更新
        sql_update_ib_target_storage = '''
        update dm2_storage_inbound
        set dsitargetstorageid = :target_storage_id
        where dsiid = :ib_id
        '''
        params_update_ib_target_storage = {
            'target_storage_id': storage_id,
            'ib_id': ib_id
        }

        commands = [
            (sql_update_file, params_update_file),
            (sql_update_directory, params_update_directory),
            (sql_update_object, params_update_object),
            (sql_update_ib_target_storage, params_update_ib_target_storage)
        ]
        try:
            CFactory().give_me_db(self.get_mission_db_id()).execute_batch(commands)
            return CResult.merge_result(
                self.Success,
                '存储[{0}]下的数据[{1}]入库成功!'.format(storage_id, ib_directory_name)
            )
        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '存储[{0}]下的数据[{1}]入库成功失败, 错误原因为: [{2}]!'.format(storage_id, ib_directory_name, error.__str__())
            )


if __name__ == '__main__':
    """
    Job对象的简洁测试模式
    创建时, 以sch_center_mission表的scmid, scmParams的内容初始化即可, 调用其execute方法, 即是一次并行调度要运行的主要过程
    """
    job_dm_inbound('', '').execute()
