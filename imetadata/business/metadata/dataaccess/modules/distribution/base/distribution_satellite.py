# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:21
# @Author : 赵宇飞
# @File : distribution_guotu.py
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_base import distribution_base
from imetadata.database.c_factory import CFactory
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
            access_Wait_flag = self.DB_False  # 定义等待标志，为True则存在检查项目为等待
            access_Forbid_flag = self.DB_False  # 定义禁止标志，为True则存在检查项目为禁止
            message = ''

            # 文件与影像质检部分
            file_qa = quality_summary_json.xpath_one('total', '')
            image_qa = quality_summary_json.xpath_one('metadata.data', '')
            business_qa = quality_summary_json.xpath_one('metadata.business', '')
            if CUtils.equal_ignore_case(file_qa, self.QA_Result_Error) \
                    or CUtils.equal_ignore_case(image_qa, self.QA_Result_Error) \
                    or CUtils.equal_ignore_case(business_qa, self.QA_Result_Error):
                message = message + '[数据与其相关文件的质检存在error!请进行修正！]'
                access_Forbid_flag = self.DB_True
            elif CUtils.equal_ignore_case(file_qa, self.QA_Result_Warn) \
                    or CUtils.equal_ignore_case(image_qa, self.QA_Result_Warn) \
                    or CUtils.equal_ignore_case(business_qa, self.QA_Result_Warn):
                message = message + '[数据与其相关文件的质检存在warn!请进行检查！]'
                access_Wait_flag = self.DB_True
            else:
                pass

            # 数据库部分
            access_Wait_flag, access_Forbid_flag, message = \
                self.db_access_check(access_Wait_flag, access_Forbid_flag, message)

            # 开始进行检查的结果判断
            access_flag = self.DataAccess_Pass
            if access_Forbid_flag:
                access_flag = self.DataAccess_Forbid
            elif access_Wait_flag:
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

    def db_access_check(self, access_Wait_flag, access_Forbid_flag, message):
        return access_Wait_flag, access_Forbid_flag, message

    def sync(self) -> str:
        try:
            main_table_name = CUtils.dict_value_by_name(self.information(), 'main_table_name', 'ap_product')
            metadata_sql_check = '''
            select id from {0} where id='{1}'
            '''.format(main_table_name, self._obj_id)
            main_record_cheak = CFactory().give_me_db(self._db_id).one_row(metadata_sql_check).size()  # 查找记录数

            if main_record_cheak == 0:  # 记录数为0则拼接插入语句
                insert_or_updata = self.DB_True
            elif main_record_cheak > 0:  # 记录数不为0则拼接更新语句
                insert_or_updata = self.DB_False
            else:
                return CResult.merge_result(
                    self.Failure,
                    '数据检索分发模块在进行数据同步时出现错误:同步的对象[{0}]在处理时出现异常, 详细情况: [{1}]!'.format(
                        self._obj_name,
                        '数据库中在存在异常数据，可能是垃圾数据未清理干净'
                    )
                )

            main_result = self.process_main_table(insert_or_updata)
            metadata_result = self.process_metadata_table(insert_or_updata)
            ndi_result = self.process_ndi_table(insert_or_updata)

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

    def process_main_table(self, insert_or_updata):
        object_table_id = self._obj_id  # 获取oid
        object_table_data = self._dataset
        main_table_name = CUtils.dict_value_by_name(self.information(), 'main_table_name', 'ap_product')

        main_table = CTable()
        main_table.load_info(self._db_id, main_table_name)
        main_table.column_list.column_by_name('id').set_value(object_table_id)
        main_table.column_list.column_by_name('productname').set_value(
            object_table_data.value_by_name(0, 'dsoobjectname', '')
        )
        main_table.column_list.column_by_name('producttype').set_value(self._obj_type_code)
        main_table.column_list.column_by_name('regioncode').set_null()

        if insert_or_updata:
            result = main_table.insert_data()
        else:
            result = main_table.update_data()

        return result

    def process_metadata_table(self, insert_or_updata):
        object_table_id = self._obj_id  # 获取oid
        object_table_data = self._dataset
        metadata_table_name = CUtils.dict_value_by_name(
            self.information(), 'metadata_table_name', 'ap_product_metadata'
        )

        metadata_table = CTable()
        metadata_table.load_info(self._db_id, metadata_table_name)
        metadata_table.column_list.column_by_name('id').set_value(object_table_id)
        metadata_table.column_list.column_by_name('fid').set_value(object_table_id)
        dsometadataxml = object_table_data.value_by_name(0, 'dsometadataxml_bus', '')
        metadata_table.column_list.column_by_name('metaxml').set_value(dsometadataxml)
        now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
        metadata_table.column_list.column_by_name('addtime').set_value(now_time)
        metadata_table.column_list.column_by_name('version').set_null()

        if insert_or_updata:
            result = metadata_table.insert_data()
        else:
            result = metadata_table.update_data()

        return result

    def process_ndi_table(self, insert_or_updata):
        object_table_id = self._obj_id  # 获取oid
        object_table_data = self._dataset
        metadata_bus_dict = self.get_metadata_bus_dict()
        ndi_table_name = CUtils.dict_value_by_name(self.information(), 'ndi_table_name', 'ap_product_ndi')

        ndi_table = CTable()
        ndi_table.load_info(self._db_id, ndi_table_name)
        ndi_table.column_list.column_by_name('id').set_value(object_table_id)
        ndi_table.column_list.column_by_name('rid').set_value(object_table_id)
        ndi_table.column_list.column_by_name('satelliteid').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'satelliteid', '')
        )
        ndi_table.column_list.column_by_name('sensorid').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'sensorid', '')
        )
        # ndi_table.column_list.column_by_name('centerlatitude').set_value(
        #     CUtils.dict_value_by_name(metadata_bus_dict, 'centerlatitude', '')
        # )
        # ndi_table.column_list.column_by_name('centerlongitude').set_value(
        #     CUtils.dict_value_by_name(metadata_bus_dict, 'centerlongitude', '')
        # )
        ndi_table.column_list.column_by_name('topleftlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'topleftlatitude', '')
        )
        ndi_table.column_list.column_by_name('topleftlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'topleftlongitude', '')
        )
        ndi_table.column_list.column_by_name('toprightlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'toprightlatitude', '')
        )
        ndi_table.column_list.column_by_name('toprightlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'toprightlongitude', '')
        )
        ndi_table.column_list.column_by_name('bottomrightlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomrightlatitude', '')
        )
        ndi_table.column_list.column_by_name('bottomrightlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomrightlongitude', '')
        )
        ndi_table.column_list.column_by_name('bottomleftlatitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomleftlatitude', '')
        )
        ndi_table.column_list.column_by_name('bottomleftlongitude').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'bottomleftlongitude', '')
        )
        ndi_table.column_list.column_by_name('transformimg').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'transformimg', '')
        )
        # ndi_table.column_list.column_by_name('filesize').set_value(
        #     CUtils.dict_value_by_name(metadata_bus_dict, 'filesize', '')
        # )
        ndi_table.column_list.column_by_name('dataexist').set_value(0)
        ndi_table.column_list.column_by_name('centertime').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'centertime', '')
        )
        ndi_table.column_list.column_by_name('resolution').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'resolution', '')
        )
        ndi_table.column_list.column_by_name('rollangle').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'rollangle', '')
        )
        ndi_table.column_list.column_by_name('cloudpercent').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'cloudpercent', '')
        )
        ndi_table.column_list.column_by_name('dataum').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'dataum', '')
        )
        ndi_table.column_list.column_by_name('acquisition_id').set_value(
            CUtils.dict_value_by_name(metadata_bus_dict, 'acquisition_id', '')
        )

        if insert_or_updata:
            result = ndi_table.insert_data()
        else:
            result = ndi_table.update_data()

        return result
