# -*- coding: utf-8 -*- 
# @Time : 2020/11/13 18:56 
# @Author : 王西亚 
# @File : module_data2service.py
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_time import CTime
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
                        ddad_datatype ->> 'dsodid' AS dsodid,
                        ddad_datatype ->> 'dsodtype' AS dsodtype,
                        ddad_datatype ->> 'dsodgroup' AS dsodgroup,
                        ddad_datatype ->> 'dsodcatalog' AS dsodcatalog,
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
            sql_query = '''
                                    SELECT
                                    ddad_id,
                                    ddad_title,
                                    ddad_datatype ->> 'dsodid' AS dsodid,
                                    ddad_datatype ->> 'dsodtype' AS dsodtype,
                                    ddad_datatype ->> 'dsodgroup' AS dsodgroup,
                                    ddad_datatype ->> 'dsodcatalog' AS dsodcatalog,
                                    ddad_startdate,
                                    ddad_enddate,
                                    ddad_spatial 
                                    FROM
            	                    dp_dm2_auto_deploy
                                    '''
            db_id = self._db_id
            dataset = CFactory().give_me_db(db_id).all_row(sql_query)
            sql_query = '''
                                        SELECT
                                            dso_time ->> 'start_time' AS dm2_start_time,
                                            dso_time ->> 'end_time' AS dm2_end_time,
                                            dso_geo_wgs84 AS dpservicegeom,
                                            dso_prj_wkt AS dpproject
                                        FROM
                                            dm2_storage_object
                                        WHERE 
                                            dsoid = '{0}'
                                    '''.format(obj_id)
            objectset = CFactory().give_me_db(db_id).one_row(sql_query)
            dm2_start_time = objectset.value_by_name(0, 'dm2_start_time', None)
            dm2_end_time = objectset.value_by_name(0, 'dm2_end_time', None)
            # dm2_start_time = CTime.from_datetime_str(dm2_start_time, '%Y-%m-%d %H:%M:%S')
            # dm2_end_time = CTime.from_datetime_str(dm2_end_time, '%Y-%m-%d %H:%M:%S')
            dm2_dpproject = objectset.value_by_name(0, 'dpproject', None)
            dm2_dpservicegeom = objectset.value_by_name(0, 'dpservicegeom', None)
            sql_query = '''
                                                   SELECT
                                                       dsodid AS dsodid,
                                                       dsodtype AS dsodtype,
                                                       dsodgroup AS dsodgroup,
                                                       dsodcatalog AS dsodcatalog
                                                   FROM
                                                       dm2_storage_object_def
                                                   WHERE 
                                                       dsodid = '{0}'
                                               '''.format(obj_type)
            object_def_set = CFactory().give_me_db(db_id).one_row(sql_query)
            dsodid = object_def_set.value_by_name(0, 'dsodid', '')
            dsodtype = object_def_set.value_by_name(0, 'dsodtype', '')
            dsodgroup = object_def_set.value_by_name(0, 'dsodgroup', '')
            dsodcatalog = object_def_set.value_by_name(0, 'dsodcatalog', '')
            obj_type_list = []
            obj_type_list.append(dsodid)
            obj_type_list.append(dsodtype)
            obj_type_list.append(dsodgroup)
            obj_type_list.append(dsodcatalog)
            sql_query = '''
                            SELECT
                                *
                            FROM
                                dp_v_qfg
                            WHERE 
                                dptitle = '{0}'
                        '''.format(obj_id)
            dp_v_qfg_set = CFactory().give_me_db(db_id).all_row(sql_query)
            if not dataset.is_empty():
                for data_index in range(dataset.size()):
                    ddad_dsodid = dataset.value_by_name(data_index, 'dsodid', '')
                    ddad_dsodtype = dataset.value_by_name(data_index, 'dsodtype', '')
                    ddad_dsodgroup = dataset.value_by_name(data_index, 'dsodgroup', '')
                    ddad_dsodcatalog = dataset.value_by_name(data_index, 'dsodcatalog', '')
                    if ddad_dsodid is not None:
                        ddad_datatype = ddad_dsodid
                    elif ddad_dsodtype is not None:
                        ddad_datatype = ddad_dsodtype
                    elif ddad_dsodgroup is not None:
                        ddad_datatype = ddad_dsodgroup
                    elif ddad_dsodcatalog is not None:
                        ddad_datatype = ddad_dsodcatalog
                    else:
                        ddad_datatype = None
                    # ddad_id = dataset.value_by_name(data_index, 'ddad_id', '')
                    ddad_startdate = dataset.value_by_name(data_index, 'ddad_startdate', None)
                    # ddad_startdate = CTime.from_datetime_str(ddad_startdate, '%Y-%m-%d %H:%M:%S')
                    ddad_enddate = dataset.value_by_name(data_index, 'ddad_enddate', None)
                    # ddad_enddate = CTime.from_datetime_str(ddad_enddate, '%Y-%m-%d %H:%M:%S')
                    # ddad_spatial = dataset.value_by_name(data_index, 'ddad_spatial', '')
                    if ddad_datatype in obj_type_list \
                            or ddad_startdate > dm2_start_time \
                            or ddad_enddate < dm2_end_time:
                        if dp_v_qfg_set.is_empty():
                            dpid = CUtils.one_id()
                            layer_dpid = CUtils.one_id()
                            CFactory().give_me_db(db_id).execute(
                                '''
                                insert into dp_v_qfg(
                                dpid, 
                                dpstatus, 
                                dpprocesstype, 
                                dpschemaid,
                                dptitle, 
                                dpname, 
                                dpdeploydir, 
                                dpproject, 
                                dpservicetype, 
                                dpservicegeom
                                ) 
                                values(
                                :dpid, 
                                :dpstatus, 
                                :dpprocesstype, 
                                :dpschemaid,
                                :dptitle, 
                                :dpname,
                                :dpdeploydir,
                                :dpproject,
                                :dpservicetype,
                                :dpservicegeom
                                )
                                ''',
                                {
                                    'dpid': dpid,
                                    'dpstatus': 5,
                                    'dpprocesstype': 'new',
                                    'dpschemaid': '',
                                    'dptitle': obj_id,
                                    'dpname': obj_name,
                                    'dpdeploydir': None,
                                    'dpproject': dm2_dpproject,
                                    'dpservicetype': None,
                                    'dpservicegeom': dm2_dpservicegeom
                                }
                            )
                            CFactory().give_me_db(self._db_id).execute(
                                '''
                                insert into dp_v_qfg_layer(
                                dpid, 
                                dpservice_id, 
                                dplayerschema_id,
                                dpprocesstype, 
                                dplayer_id, 
                                dplayer_name,
                                dplayer_datatype,
                                dplayer_resultfields
                                ) 
                                values(
                                :dpid, 
                                :dpservice_id, 
                                :dplayerschema_id,
                                :dpprocesstype, 
                                :dplayer_id, 
                                :dplayer_name,
                                :dplayer_datatype,
                                :dplayer_resultfields
                                )
                                ''',
                                {
                                    'dpid': layer_dpid,
                                    'dpservice_id': dpid,
                                    'dplayerschema_id': '',
                                    'dpprocesstype': 'new',
                                    'dplayer_id': obj_id,
                                    'dplayer_name': obj_name,
                                    'dplayer_datatype': 'Raster',
                                    'dplayer_resultfields': ''
                                }
                            )
                            CFactory().give_me_db(self._db_id).execute(
                                '''
                                insert into dp_v_qfg_layer_file(
                                dpdf_id, 
                                dpdf_layer_id, 
                                dpdf_object_id, 
                                dpdf_service_filepath, 
                                dpdf_processtype,
                                dpdf_publish_filename
                                ) 
                                values(
                                :dpdf_id,
                                :dpdf_layer_id, 
                                :dpdf_object_id, 
                                :dpdf_service_filepath, 
                                :dpdf_processtype,
                                :dpdf_publish_filename
                                )
                                ''',
                                {
                                    'dpdf_id': CUtils.one_id(),
                                    'dpdf_layer_id': layer_dpid,
                                    'dpdf_object_id': obj_id,
                                    'dpdf_service_filepath': None,
                                    'dpdf_processtype': 'new',
                                    'dpdf_publish_filename': obj_name
                                }
                            )
                        else:
                            CFactory().give_me_db(db_id).execute(
                                '''
                                update dp_v_qfg 
                                set dpstatus = 5,
                                dpprocesstype = :dpprocesstype,
                                dpproject = :dm2_dpproject,
                                dpservicetype = dpservicetype,
                                dpservicegeom = :dm2_dpservicegeom
                                where dptitle = :obj_id
                                ''',
                                {'dpprocesstype': 'updata', 'dm2_dpproject': dm2_dpproject, 'dpservicetype': None,
                                 'dm2_dpservicegeom': dm2_dpservicegeom,
                                 'obj_id': obj_id}
                            )
                            CFactory().give_me_db(db_id).execute(
                                '''
                                update dp_v_qfg_layer 
                                set 
                                dpprocesstype = :dpprocesstype
                                where dplayer_id = :obj_id 
                                ''',
                                {'dpprocesstype': 'updata', 'obj_id': obj_id}
                            )
                            CFactory().give_me_db(db_id).execute(
                                '''
                                update dp_v_qfg_layer_file 
                                set 
                                dpdf_service_filepath = :dpdf_service_filepath, 
                                dpdf_processtype = :dpprocesstype,
                                dpdf_publish_filename = :obj_name
                                where dpdf_object_id = :obj_id
                                ''',
                                {'dpdf_service_filepath': None, 'dpprocesstype': 'updata', 'obj_name': obj_name,
                                 'obj_id': obj_id}
                            )
            else:
                message = '没有对应的规则, 直接通过!'
                result = CResult.merge_result(self.Success, message)
                return result
        else:
            pass

    def __service_release(self):
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
        dso_geo_bb_wgs84 = data_space_set.value_by_name(0, 'dso_geo_bb_wgs84', None)
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
