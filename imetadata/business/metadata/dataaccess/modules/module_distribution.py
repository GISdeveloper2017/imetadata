# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:58 
# @Author : 王西亚 
# @File : module_distribution.py
from imetadata.base.c_file import CFile
from imetadata.base.c_object import CObject
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule
from imetadata.business.metadata.dataaccess.modules.distribution.base import distribution_base
from imetadata.business.metadata.dataaccess.modules.distribution.distribution_default import distribution_default
from imetadata.database.c_factory import CFactory


class module_distribution(CDAModule):
    """
    数据检索分发模块对数管编目的质检要求
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据检索分发'

        return info

    def access(self) -> str:
        """
        解析数管中识别出的对象, 与第三方模块的访问能力, 在本方法中进行处理
        返回的json格式字符串中, 是默认的CResult格式, 但是在其中还增加了Access属性, 通过它反馈当前对象是否满足第三方模块的应用要求
        注意: 一定要反馈Access属性
        :return:
        """
        # module_obj_real = self.__find_module_obj()
        # if module_obj_real is None:
        #     message = '没有对应的算法, 直接通过!'
        #     result = CResult.merge_result(self.Success, message)
        #     return result
        # result = module_obj_real.access()
        # return result
        result = super().access()
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Pass)

    def sync(self) -> str:
        """
        处理数管中识别的对象, 与第三方模块的同步
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口

        注意: 在本方法中, 不要用_quality_info属性, 因为外部调用方考虑的效率因素, 没有传入!!!
        :return:
        """
        # 根据objecttype类型查找distribution文件夹下对应的类文件（识别通过objecttype找object_def表中的dsodtype字段与类对象中的info[self.Name_Type]值相同）
        distribution_obj_real = self.__find_module_obj()
        if distribution_obj_real is None:
            message = '没有对应的算法, 直接通过!'
            result = CResult.merge_result(self.Success, message)
            return result
        result = distribution_obj_real.sync()
        return result

        # return CResult.merge_result(
        #     self.Success,
        #     '在[{0}]里写对象[{1}]向模块[{2}]中同步的算法! '.format(
        #         CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
        #         self._obj_name,
        #         CUtils.dict_value_by_name(self.information(), self.Name_Title, '')
        #     )
        # )

    def __find_module_obj(self) -> distribution_base:
        sql_query = '''
            SELECT
                --dm2_storage_object_def.dsodtype,
                dm2_storage_object_def.dsodcode,
                dm2_storage_file.dsfid as query_file_id,
                dm2_storage_directory.dsddirlastmodifytime as query_directory_lastmodifytime,
                dm2_storage_directory.dsdid as query_directory_id,
                dm2_storage_object.* 
            FROM
                dm2_storage_object
                LEFT JOIN dm2_storage_object_def ON dm2_storage_object.dsoobjecttype = dm2_storage_object_def.dsodid
                LEFT JOIN dm2_storage_file on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                LEFT JOIN dm2_storage_directory on dm2_storage_file.dsfdirectoryid = dm2_storage_directory.dsdid
            WHERE
                dm2_storage_object.dsoid = '{0}'
        '''.format(self._obj_id)

        dataset = CFactory().give_me_db(self._db_id).one_row(sql_query)
        # object_def_type = dataset.value_by_name(0, 'dsodtype', '') #类型不需要了
        object_plugin_file_main_name = dataset.value_by_name(0, 'dsoobjecttype', '')  # plugins_8000_dom_10
        object_plugin_type = dataset.value_by_name(0, 'dsodatatype', '')  # 数据类型:dir-目录;file-文件
        object_id = dataset.value_by_name(0, 'dsoid', '')
        object_name = dataset.value_by_name(0, 'dsoobjectname', '')
        quality_info = dataset.value_by_name(0, 'dso_quality', '')

        distribution_obj_real = None
        # 构建数据对象object对应的识别插件，获取get_information里面的Plugins_Info_Module_Distribute_Engine信息
        plugins_root_package_name = '{0}.{1}'.format(CSys.get_plugins_package_root_name(), object_plugin_type)
        # 判断插件是否存在
        plugins_root_dir = CSys.get_plugins_root_dir()
        plugins_type_root_dir = CFile.join_file(plugins_root_dir, object_plugin_type)
        plugins_file = CFile.join_file(plugins_type_root_dir, '{0}.py'.format(object_plugin_file_main_name))
        if CFile.file_or_path_exist(plugins_file):
            class_classified_obj = CObject.create_plugins_instance(
                plugins_root_package_name,
                object_plugin_file_main_name,
                None
            )
            plugins_info = class_classified_obj.get_information()
            distinct_file_main_name = plugins_info[self.Plugins_Info_Module_Distribute_Engine]  # 对应同步文件的类名称

            # 判断同步插件文件是否存在
            access_modules_root_dir = CSys.get_metadata_data_access_modules_root_dir()
            distribution_root_dir = CFile.join_file(access_modules_root_dir, self.Name_Distribution)
            distribution_file = CFile.join_file(distribution_root_dir, '{0}.py'.format(distinct_file_main_name))
            if CFile.file_or_path_exist(distribution_file):
                # 构建同步对象
                distribution_obj = CObject.create_module_distribution_instance(
                    '{0}.{1}'.format(CSys.get_metadata_data_access_modules_root_name(), self.Name_Distribution),
                    distinct_file_main_name,
                    self._db_id,
                    object_id,
                    object_name,
                    quality_info,
                    dataset
                )
                distribution_obj_real = distribution_obj
        if distribution_obj_real is None:
            # 注意, 这里默认为默认处理的同步插件，先预留
            distribution_obj_real = distribution_default(self._db_id, object_id, object_name, quality_info, dataset)
        return distribution_obj_real
