# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : distribution_guotu.py
import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base
from imetadata.database.tools.c_table import CTable
import datetime


class distribution_satellite(distribution_base):
    """
    卫星即时服务的基础类
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '卫星数据'
        info['main_table_name'] = 'ap_product'
        info['metadata_table_name'] = 'ap_product_metadata'
        info['ndi_table_name'] = 'ap_product_ndi'
        return info

    def access(self) -> str:
        try:
            # quality_info_xml = self._quality_info  # 获取质检xml
            quality_summary = self._dataset.value_by_name(0, 'dso_quality_summary', '')
            quality_summary_json = CJson()
            quality_summary_json.load_obj(quality_summary)
            access_wait_flag = self.DB_False  # 定义等待标志，为True则存在检查项目为等待
            access_forbid_flag = self.DB_False  # 定义禁止标志，为True则存在检查项目为禁止
            message = ''

            # 文件与影像质检部分
            file_qa = quality_summary_json.xpath_one('total', '')
            image_qa = quality_summary_json.xpath_one('metadata.data', '')
            business_qa = quality_summary_json.xpath_one('metadata.business', '')
            if CUtils.equal_ignore_case(file_qa, self.QA_Result_Error) \
                    or CUtils.equal_ignore_case(image_qa, self.QA_Result_Error) \
                    or CUtils.equal_ignore_case(business_qa, self.QA_Result_Error):
                message = message + '[数据与其相关文件的质检存在error!请进行修正！]'
                access_forbid_flag = self.DB_True
            elif CUtils.equal_ignore_case(file_qa, self.QA_Result_Warn) \
                    or CUtils.equal_ignore_case(image_qa, self.QA_Result_Warn) \
                    or CUtils.equal_ignore_case(business_qa, self.QA_Result_Warn):
                message = message + '[数据与其相关文件的质检存在warn!请进行检查！]'
                access_wait_flag = self.DB_True
            else:
                pass

            # 数据库部分
            access_wait_flag, access_forbid_flag, message = \
                self.db_access_check(access_wait_flag, access_forbid_flag, message)

            # 开始进行检查的结果判断
            access_flag = self.DataAccess_Pass
            if access_forbid_flag:
                access_flag = self.DataAccess_Forbid
            elif access_wait_flag:
                access_flag = self.DataAccess_Wait
            if CUtils.equal_ignore_case(message, ''):
                message = '模块可以进行访问!'

            result = CResult.merge_result(
                self.Success,
                '模块[{0}.{1}]对对象[{2}]的访问能力已经分析完毕!分析结果为:{3}'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name,
                    message
                )
            )
            return CResult.merge_result_info(result, self.Name_Access, access_flag)
        except Exception as error:
            result = CResult.merge_result(
                self.Failure,
                '模块[{0}.{1}]对对象[{2}]的访问能力的分析存在异常!详细情况: {3}!'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name,
                    error.__str__()
                )
            )
            return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Forbid)

    def db_access_check(self, access_wait_flag, access_forbid_flag, message):
        temporary_dict = dict()
        temporary_dict['dso_time'] = self._dataset.value_by_name(0, 'dso_time', '')
        temporary_dict['dso_browser'] = self._dataset.value_by_name(0, 'dso_browser', '')
        temporary_dict['dso_thumb'] = self._dataset.value_by_name(0, 'dso_thumb', '')
        temporary_dict['dso_geo_wgs84'] = self._dataset.value_by_name(0, 'dso_geo_wgs84', '')
        for key, value in temporary_dict.items():
            if CUtils.equal_ignore_case(value, ''):
                message = message + '[数据{0}入库异常!请进行检查与修正！]'.format(key.replace('dso_', ''))
                access_forbid_flag = self.DB_True
        return access_wait_flag, access_forbid_flag, message

    def sync(self) -> str:
        try:
            main_result = self.process_main_table()
            metadata_result = self.process_metadata_table()
            ndi_result = self.process_ndi_table()

            if not CResult.result_success(main_result):
                return main_result
            elif not CResult.result_success(metadata_result):
                return metadata_result
            elif not CResult.result_success(ndi_result):
                return ndi_result
            else:
                return CResult.merge_result(
                    self.Success,
                    '对象[{0}]的同步成功! '.format(self._obj_name)
                )
        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '数据检索分发模块在进行数据同步时出现错误:同步的对象[{0}]在处理时出现异常, 详细情况: [{1}]!'.format(
                    self._obj_name,
                    error.__str__()
                )
            )

    def process_main_table(self):
        object_table_id = self._obj_id  # 获取oid
        object_table_data = self._dataset
        metadata_bus_dict = self.get_metadata_bus_dict()
        main_table_name = CUtils.dict_value_by_name(self.information(), 'main_table_name', 'ap_product')

        main_table = CTable()
        main_table.load_info(self._db_id, main_table_name)
        main_table.column_list.column_by_name('id').set_value(object_table_id)

        productname = CUtils.dict_value_by_name(metadata_bus_dict, 'productname', None)
        if CUtils.equal_ignore_case(productname, ''):
            productname = object_table_data.value_by_name(0, 'dsoobjectname', None)
        main_table.column_list.column_by_name('productname').set_value(productname)
        main_table.column_list.column_by_name('producttype').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'producttype', None)
        )
        main_table.column_list.column_by_name('regioncode').set_null()
        main_table.column_list.column_by_name('productattribute').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'productattribute', None)
        )

        centerlatitude = CUtils.dict_value_by_name(metadata_bus_dict, 'centerlatitude', None)
        centerlongitude = CUtils.dict_value_by_name(metadata_bus_dict, 'centerlongitude', None)
        centerlonlat = '{0},{1}'.format(centerlongitude, centerlatitude)
        main_table.column_list.column_by_name('centerlonlat').set_value(centerlonlat)

        main_table.column_list.column_by_name('geomwkt').set_sql(
            '''
            st_astext(
            (select dso_geo_wgs84 from dm2_storage_object where dsoid='{0}')
            )
            '''.format(object_table_id)
        )
        main_table.column_list.column_by_name('geomobj').set_sql(
            '''
            (select dso_geo_wgs84 from dm2_storage_object where dsoid='{0}')
            '''.format(object_table_id)
        )
        main_table.column_list.column_by_name('browserimg').set_value(
            object_table_data.value_by_name(0, 'dso_browser', None)
        )
        main_table.column_list.column_by_name('thumbimg').set_value(
            object_table_data.value_by_name(0, 'dso_thumb', None)
        )
        main_table.column_list.column_by_name('publishdate').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'publishdate', None)
        )
        main_table.column_list.column_by_name('copyright').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'copyright', None)
        )

        dso_time = object_table_data.value_by_name(0, 'dso_time', None)
        dso_time_json = CJson()
        dso_time_json.load_obj(dso_time)
        main_table.column_list.column_by_name('imgdate').set_value(
            dso_time_json.xpath_one('time', None)
        )
        main_table.column_list.column_by_name('starttime').set_value(
            dso_time_json.xpath_one('start_time', None)
        )
        main_table.column_list.column_by_name('endtime').set_value(
            dso_time_json.xpath_one('end_time', None)
        )
        resolution = CUtils.dict_value_by_name(metadata_bus_dict, 'resolution', None)
        if not CUtils.equal_ignore_case(resolution, ''):
            main_table.column_list.column_by_name('resolution').set_value(resolution)
        else:
            main_table.column_list.column_by_name('resolution').set_value(0)

        main_table.column_list.column_by_name('filesize').set_sql(
            '''
            (select sum(dodfilesize) from dm2_storage_obj_detail where dodobjectid='{0}')
            '''.format(object_table_id)
        )

        productid = CUtils.dict_value_by_name(metadata_bus_dict, 'productid', None)
        if CUtils.equal_ignore_case(productid, ''):
            object_type = object_table_data.value_by_name(0, 'dsodatatype', '')
            if CUtils.equal_ignore_case(object_type, self.Name_Dir):
                main_table.column_list.column_by_name('productid').set_value(
                    object_table_data.value_by_name(0, 'dsoobjectname', None)
                )
            elif CUtils.equal_ignore_case(object_type, self.Name_File):
                main_table.column_list.column_by_name('productid').set_sql(
                    '''
                    (SELECT dsffilename FROM dm2_storage_file WHERE dsf_object_id = '{0}')
                    '''.format(object_table_id)
                )
            else:
                main_table.column_list.column_by_name('productid').set_null()
        else:
            main_table.column_list.column_by_name('productid').set_value(productid)

        main_table.column_list.column_by_name('remark').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'remark', None)
        )
        main_table.column_list.column_by_name('extent').set_sql(
            '''
            (select dso_geo_bb_wgs84 from dm2_storage_object where dsoid='{0}')
            '''.format(object_table_id)
        )
        main_table.column_list.column_by_name('proj').set_null()  # 原始数据保持空

        main_table.column_list.column_by_name('dataid').set_null()  # ap_monitor_data表对应id(数据id)，目前不清楚怎么取
        main_table.column_list.column_by_name('shplog').set_null()

        if not main_table.if_exists():
            now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
            main_table.column_list.column_by_name('addtime').set_value(now_time)
            main_table.column_list.column_by_name('isdel').set_value(0)
            main_table.column_list.column_by_name('projectnames').set_value('productname')
        result = main_table.save_data()

        return result

    def process_metadata_table(self):
        object_table_id = self._obj_id  # 获取oid
        object_table_data = self._dataset
        metadata_bus_dict = self.get_metadata_bus_dict()
        metadata_table_name = CUtils.dict_value_by_name(
            self.information(), 'metadata_table_name', 'ap_product_metadata'
        )

        metadata_table = CTable()
        metadata_table.load_info(self._db_id, metadata_table_name)
        metadata_table.column_list.column_by_name('id').set_value(object_table_id)
        metadata_table.column_list.column_by_name('fid').set_value(object_table_id)
        dsometadataxml = object_table_data.value_by_name(0, 'dsometadataxml_bus', None)
        metadata_table.column_list.column_by_name('metaxml').set_value(dsometadataxml)

        otherxml = CUtils.dict_value_by_name(metadata_bus_dict, 'otherxml', None)
        if not CUtils.equal_ignore_case(otherxml, ''):
            view_path = settings.application.xpath_one(self.Path_Setting_MetaData_Dir_View, None)
            browser_path = CFile.file_path(self._dataset.value_by_name(0, 'dso_browser', None))
            file_list = CFile.file_or_dir_fullname_of_path(
                CFile.join_file(view_path, browser_path), False, otherxml, CFile.MatchType_Regex
            )
            if len(file_list) > 0:
                metadata_table.column_list.column_by_name('otherxml').set_value(
                    CFile.file_2_str(file_list[0])
                )

        if not metadata_table.if_exists():
            metadata_table.column_list.column_by_name('version').set_value('1.0')
            now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
            metadata_table.column_list.column_by_name('addtime').set_value(now_time)

        result = metadata_table.save_data()

        return result

    def process_ndi_table(self):
        object_table_id = self._obj_id  # 获取oid
        metadata_bus_dict = self.get_metadata_bus_dict()
        ndi_table_name = CUtils.dict_value_by_name(self.information(), 'ndi_table_name', 'ap_product_ndi')

        ndi_table = CTable()
        ndi_table.load_info(self._db_id, ndi_table_name)
        ndi_table.column_list.column_by_name('id').set_value(object_table_id)

        productname = CUtils.dict_value_by_name(metadata_bus_dict, 'productname', None)
        if CUtils.equal_ignore_case(productname, ''):
            productname = self._dataset.value_by_name(0, 'dsoobjectname', None)
        ndi_table.column_list.column_by_name('rid').set_value(productname)
        ndi_table.column_list.column_by_name('fid').set_value(object_table_id)
        ndi_table.column_list.column_by_name('satelliteid').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'satelliteid', None)
        )
        ndi_table.column_list.column_by_name('sensorid').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'sensorid', None)
        )
        ndi_table.column_list.column_by_name('topleftlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'topleftlatitude', None)
        )
        ndi_table.column_list.column_by_name('topleftlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'topleftlongitude', None)
        )
        ndi_table.column_list.column_by_name('toprightlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'toprightlatitude', None)
        )
        ndi_table.column_list.column_by_name('toprightlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'toprightlongitude', None)
        )
        ndi_table.column_list.column_by_name('bottomrightlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomrightlatitude', None)
        )
        ndi_table.column_list.column_by_name('bottomrightlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomrightlongitude', None)
        )
        ndi_table.column_list.column_by_name('bottomleftlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomleftlatitude', None)
        )
        ndi_table.column_list.column_by_name('bottomleftlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomleftlongitude', None)
        )
        ndi_table.column_list.column_by_name('centerlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'centerlatitude', None)
        )
        ndi_table.column_list.column_by_name('centerlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'centerlongitude', None)
        )

        transformimg = CUtils.dict_value_by_name(metadata_bus_dict, 'transformimg', None)
        if not CUtils.equal_ignore_case(transformimg, ''):
            view_path = settings.application.xpath_one(self.Path_Setting_MetaData_Dir_View, None)
            browser_path = CFile.file_path(self._dataset.value_by_name(0, 'dso_browser', None))
            file_list = CFile.file_or_dir_fullname_of_path(
                CFile.join_file(view_path, browser_path), False, transformimg, CFile.MatchType_Regex
            )
            if len(file_list) > 0:
                ndi_table.column_list.column_by_name('transformimg').set_value(
                    CFile.join_file(browser_path, CFile.file_name(file_list[0]))
                )

        ndi_table.column_list.column_by_name('filesize').set_sql(
            '''
            (select sum(dodfilesize) from dm2_storage_obj_detail where dodobjectid='{0}')
            '''.format(object_table_id)
        )
        ndi_table.column_list.column_by_name('dataexist').set_value(0)
        ndi_table.column_list.column_by_name('centertime').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'centertime', None)
        )

        resolution = CUtils.dict_value_by_name(metadata_bus_dict, 'resolution', None)
        if not CUtils.equal_ignore_case(resolution, ''):
            ndi_table.column_list.column_by_name('resolution').set_value(resolution)
        else:
            ndi_table.column_list.column_by_name('resolution').set_value(0)

        rollangle = CUtils.dict_value_by_name(metadata_bus_dict, 'rollangle', 0)
        if CUtils.equal_ignore_case(rollangle, ''):
            rollangle = 0
        ndi_table.column_list.column_by_name('rollangle').set_value(rollangle)
        cloudpercent = CUtils.dict_value_by_name(metadata_bus_dict, 'cloudpercent', 0)
        if CUtils.equal_ignore_case(cloudpercent, ''):
            cloudpercent = 0
        ndi_table.column_list.column_by_name('cloudpercent').set_value(cloudpercent)
        ndi_table.column_list.column_by_name('dataum').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'dataum', None)
        )
        ndi_table.column_list.column_by_name('acquisition_id').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'acquisition_id', None)
        )

        result = ndi_table.save_data()

        return result
