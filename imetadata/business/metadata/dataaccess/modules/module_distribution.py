# -*- coding: utf-8 -*- 
# @Time : 2020/10/28 15:58 
# @Author : 王西亚 
# @File : module_distribution.py
import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_object import CObject
from imetadata.base.c_result import CResult
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
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
        module_obj_real, result = self.__find_module_obj()
        if not CResult.result_success(result):
            return result
        if module_obj_real is None:
            message = '没有对应的算法, 直接通过!'
            result = CResult.merge_result(self.Success, message)
            return result

        module_obj_real_type = type(module_obj_real)
        try:
            result = module_obj_real.access()
            return result
        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '模块插件{0}检查访问可用性出现异常, 具体错误原因为: {1}'.format(
                    module_obj_real_type,
                    error.__str__()
                )
            )

    def sync(self) -> str:
        """
        处理数管中识别的对象, 与第三方模块的同步
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口

        注意: 在本方法中, 不要用_quality_info属性, 因为外部调用方考虑的效率因素, 没有传入!!!
        :return:
        """
        # 根据objecttype类型查找distribution文件夹下对应的类文件（识别通过objecttype找object_def表中的dsodtype字段与类对象中的info[self.Name_Type]值相同）
        distribution_obj_real, result = self.__find_module_obj()
        if not CResult.result_success(result):
            return result
        elif distribution_obj_real is None:
            message = '没有对应的算法, 直接通过!'
            result = CResult.merge_result(self.Success, message)
            return result
        result = distribution_obj_real.sync()
        return result

    def __find_module_obj(self) -> distribution_base:
        sql_query = '''
            SELECT
                dm2_storage_file.dsfid as query_file_id,
                dm2_storage_file.dsfdirectoryid as query_directory_id,
                dm2_storage_directory.dsddirlastmodifytime as query_directory_lastmodifytime,
                dm2_storage_directory.dsdid as query_dataset_directory_id,
                dm2_storage_object.* 
            FROM
                dm2_storage_object
                LEFT JOIN dm2_storage_file on dm2_storage_file.dsf_object_id = dm2_storage_object.dsoid
                LEFT JOIN dm2_storage_directory on dm2_storage_directory.dsd_object_id = dm2_storage_object.dsoid
            WHERE
                dm2_storage_object.dsoid = '{0}'
        '''.format(self._obj_id)
        db_id = self._db_id  # 数据库连接标识（查询的dm2的数管库）
        dataset = CFactory().give_me_db(db_id).one_row(sql_query)
        object_id = dataset.value_by_name(0, 'dsoid', '')
        object_name = dataset.value_by_name(0, 'dsoobjectname', '')
        quality_info = dataset.value_by_name(0, 'dso_quality', '')
        quality_info_xml = CXml()
        quality_info_xml.load_xml(quality_info)  # 加载查询出来的xml

        db_id_distribution = self.DB_Server_ID_Distribution  # 同步处理的目标数据库标识id
        # 构建数据对象object对应的识别插件，获取get_information里面的Plugins_Info_Module_Distribute_Engine信息
        class_classified_obj = CObject.get_plugins_instance_by_object_id(db_id, object_id)
        if class_classified_obj is not None:
            plugins_info = class_classified_obj.get_information()
            obj_type_code = CUtils.dict_value_by_name(plugins_info, class_classified_obj.Plugins_Info_Type_Code, '')
            distribution_file_main_name = CUtils.dict_value_by_name(
                plugins_info, class_classified_obj.Plugins_Info_Module_Distribute_Engine, ''
            )  # 对应同步文件的类名称
            # 判断同步插件文件是否存在
            access_modules_root_dir = CSys.get_metadata_data_access_modules_root_dir()
            distribution_root_dir = CFile.join_file(access_modules_root_dir, self.Name_Distribution)
            distribution_file = CFile.join_file(distribution_root_dir, '{0}.py'.format(distribution_file_main_name))
            if CFile.file_or_path_exist(distribution_file):
                # 构建同步对象
                distribution_obj = CObject.create_module_distribution_instance(
                    '{0}.{1}'.format(CSys.get_metadata_data_access_modules_root_name(), self.Name_Distribution),
                    distribution_file_main_name,
                    db_id_distribution,
                    object_id,
                    object_name,
                    obj_type_code,
                    quality_info_xml,
                    dataset
                )

                try:  # 主要用于卫星插件的方法
                    dsometadataxml_xml = CXml()
                    dsometadataxml = dataset.value_by_name(0, 'dsometadataxml_bus', '')
                    dsometadataxml_xml.load_xml(dsometadataxml)

                    view_path = settings.application.xpath_one(self.Path_Setting_MetaData_Dir_View, None)
                    browser_path = CFile.file_path(dataset.value_by_name(0, 'dso_browser', None))
                    multiple_metadata_bus_filename_dict = \
                        class_classified_obj.get_multiple_metadata_bus_filename_with_path(
                            CFile.join_file(view_path, browser_path)
                        )
                    result, metadata_bus_dict = class_classified_obj.metadata_bus_xml_to_dict(
                        dsometadataxml_xml, multiple_metadata_bus_filename_dict
                    )
                    if CUtils.equal_ignore_case(distribution_file_main_name, 'distribution_satellite_all'):
                        if not CResult.result_success(result):
                            return None, CResult.merge_result(
                                self.Failure,
                                '卫星数据的业务元数据的详细内容解析出错!原因为{0}'.format(CResult.result_message(result))
                            )

                    distribution_obj.set_metadata_bus_dict(metadata_bus_dict)
                    result = CResult.merge_result(self.Success, '数据的信息提取完成')
                    return distribution_obj, result
                except Exception as error:
                    if CUtils.equal_ignore_case(distribution_file_main_name, 'distribution_satellite_all'):
                        return None, CResult.merge_result(
                            self.Failure,
                            '卫星数据的业务元数据的详细内容解析出错!原因为{0}'.format(error.__str__())
                        )
                    else:
                        return None, CResult.merge_result(
                            self.Failure,
                            '卫星数据的业务元数据的详细内容解析出错!原因为{0}'.format(error.__str__())
                        )
            else:
                result = CResult.merge_result(self.Failure, '系统在构建同步模块时发生异常，原因为数据的同步模块缺失')
                return None, result
        else:
            result = CResult.merge_result(self.Failure, '系统在构建同步模块时发生异常，原因为识别模块缺失或异常')
            return None, result
