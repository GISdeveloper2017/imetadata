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
from imetadata.database.base.c_dataset import CDataSet
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

    def notify(self, access: str) -> str:
        """
        处理数管中识别的对象, 与第三方模块的同步
        . 如果第三方模块自行处理, 则无需继承本方法
        . 如果第三方模块可以处理, 则在本模块中, 从数据库中提取对象的信息, 写入第三方模块的数据表中, 或者调用第三方模块接口
        :return:
        """
        ds_na = CFactory().give_me_db(self._db_id).one_row(
            '''
            select dsonid, dson_notify_status
            from dm2_storage_obj_na
            where dson_app_id = :app_id 
                and dson_object_id = :object_id
            ''',
            {
                'app_id': CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                'object_id': self._obj_id
            }
        )
        target_notify_status = self.ProcStatus_InQueue
        if CUtils.equal_ignore_case(access, self.DataAccess_Wait):
            target_notify_status = self.ProcStatus_Finished
        if not ds_na.is_empty():
            na_id = CUtils.any_2_str(ds_na.value_by_name(0, 'dsonid', 0))
            if ds_na.value_by_name(0, 'dson_notify_status', self.ProcStatus_Finished) == self.ProcStatus_Finished:
                CFactory().give_me_db(self._db_id).execute(
                    '''
                    update dm2_storage_obj_na
                    set dson_notify_status = :status
                        , dson_object_access = :object_access
                    where dsonid = :id 
                    ''',
                    {'id': na_id, 'status': target_notify_status, 'object_access': access}
                )
        else:
            CFactory().give_me_db(self._db_id).execute(
                '''
                insert into dm2_storage_obj_na(dson_app_id, dson_object_access, dson_object_id) 
                values(:app_id, :object_access, :object_id)
                ''',
                {
                    'app_id': CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    'object_id': self._obj_id,
                    'object_access': access
                }
            )

        return CResult.merge_result(
            self.Success,
            '对象[{0}]已经推送给模块[{1}]队列! '.format(
                self._obj_name,
                CUtils.dict_value_by_name(self.information(), self.Name_Title, '')
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
        sql_get_def_type = '''
                select dsodtype from dm2_storage_object_def where dsodid = '{0}'
                '''.format(self._obj_type)
        # todo sql语句查询（暂预留）
        dataset = CFactory().give_me_db(self._db_id).one_row(sql_get_def_type)
        def_type = dataset.value_by_name(0, 'dsodtype', '')
        # _obj_id
        # _quality_info

        access_modules_root_dir = CSys.get_metadata_data_access_modules_root_dir()
        access_modules_distribution_root_dir = CFile.join_file(access_modules_root_dir, self.Name_Distribution)
        plugins_file_list = CFile.file_or_subpath_of_path(access_modules_distribution_root_dir,
                                                          '{0}_*.{1}'.format(self.Name_Module,
                                                                             self.FileExt_Py))
        distribution_obj_real = None
        # 从目录下的py文件中查找满足要求的同步算法文件
        for file_name_without_path in plugins_file_list:
            if CFile.is_dir(file_name_without_path):
                continue
            file_main_name = CFile.file_main_name(file_name_without_path)
            distribution_obj = CObject.create_module_distribution_instance(
                '{0}.{1}'.format(CSys.get_metadata_data_access_modules_root_name(), self.Name_Distribution),
                file_main_name,
                self._db_id,
                self._obj_id,
                self._quality_info,
                dataset
            )

            if distribution_obj is not None:
                distribution_info = distribution_obj.get_information()
                distribution_type = distribution_info[self.Name_Type]
                if CUtils.equal_ignore_case(distribution_type, def_type):
                    distribution_obj_real = distribution_obj
                    break
        # if distribution_obj_real is None:
        #     pass    # TODO 采用默认的处理方式（分对象，数据集）
        return distribution_obj_real
