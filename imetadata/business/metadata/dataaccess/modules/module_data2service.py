# -*- coding: utf-8 -*- 
# @Time : 2020/11/13 18:56 
# @Author : 王西亚 
# @File : module_data2service.py
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule
from imetadata.database.c_factory import CFactory


class module_data2service(CDAModule):
    """
    数据服务发布模块
    """

    def __init__(self, db_id):
        super().__init__(db_id)
        self._db_id = db_id
        # 在这里将所有dp_dm2_auto_deploy配置读取到cdataset里
        sql_query = '''
                            SELECT
                                ddad_id,
                                ddad_title,
                                ddad_datatype,
                                ddad_startdate,
                                ddad_enddate,
                                ddad_spatial
                            FROM
                                dp_dm2_auto_deploy
                        '''
        db_id = self._db_id
        dataset = CFactory().give_me_db(db_id).all_row(sql_query)


    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据服务发布'

        return info

    def access(self, obj_id, obj_name, obj_type, quality) -> str:
        """
        解析数管中识别出的对象, 与第三方模块的访问能力, 在本方法中进行处理
        返回的json格式字符串中, 是默认的CResult格式, 但是在其中还增加了Access属性, 通过它反馈当前对象是否满足第三方模块的应用要求
        注意: 一定要反馈Access属性
        :return:
        """
        result = self.__test_module_obj(obj_id, obj_name)
        if not CResult.result_success(result):
            return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)
        else:
            return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Pass)

    def sync(self, object_access, obj_id, obj_name, obj_type, quality) -> str:
        if CUtils.equal_ignore_case(self.DataAccess_Pass, object_access):
            pass
        else:
            pass

    def __test_module_obj(self, obj_id, obj_name):
        sql_query = '''
                    SELECT
                        dso_geo_bb_wgs84,
                        dso_geo_wgs84,
                        dso_center_wgs84,
                        dso_prj_proj4
                    FROM
                        dm2_storage_object
                    WHERE
                        dm2_storage_object.dsoid = '{0}'
                '''.format(obj_id)
        db_id = self._db_id
        data_space_set = CFactory().give_me_db(db_id).one_row(sql_query)
        dso_geo_bb_wgs84 = data_space_set.value_by_name(0, 'dso_geo_bb_wgs84',None)
        dso_geo_wgs84 = data_space_set.value_by_name(0, 'dso_geo_wgs84', None)
        dso_center_wgs84 = data_space_set.value_by_name(0, 'dso_center_wgs84', None)
        dso_prj_proj4 = data_space_set.value_by_name(0, 'dso_prj_proj4', None)
        if dso_geo_bb_wgs84 is not None \
           and dso_geo_wgs84 is not None \
            and dso_center_wgs84 is not None \
            and dso_prj_proj4 is not None:
            result = CResult.merge_result(self.Success, '数据的信息检查完成，数据{0}可以发布服务'.format(obj_name))
            return result
        else:
            if dso_geo_bb_wgs84 is None:
                message = '{0}为空'.format('{dso_geo_bb_wgs84}')
            if dso_geo_wgs84 is None:
                message = message + '{0}为空'.format('{dso_geo_wgs84}')
            if dso_center_wgs84 is None:
                message = message + '{0}为空'.format('{dso_center_wgs84}')
            if dso_prj_proj4 is None:
                message = message + '{0}为空'.format('{dso_prj_proj4}')
            result = CResult.merge_result(self.Exception, '数据的信息检查完成，不可以发布服务，具体异常信息为{0}'.format(message))
            return result