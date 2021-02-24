# -*- coding: utf-8 -*- 
# @Time : 2020/11/23 15:51
# @Author : 赵宇飞
# @File : distribution_dataset_gdb.py
import datetime

from imetadata.base.c_json import CJson
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import distribution_guotu
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_vector_with_layers_object import \
    distribution_vector_with_layers_object


class distribution_dataset_gdb(distribution_vector_with_layers_object):
    """
    完成 王学谦 数据检索分发模块对mdb数据集类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'MDB数据集'
        info['table_name'] = 'ap3_product_rsp_vp_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 指明配置的是更新还是插入，-1时为插入，0为更新
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        object_table_data = self._dataset
        # 时间信息
        dso_time = object_table_data.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()
        dso_time_json.load_obj(dso_time)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate', dso_time_json.xpath_one('start_time', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate', dso_time_json.xpath_one('end_time', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producetime',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedatetag',
            self.transform_time_to_imagedatetag(
                CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
            )
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'isdel', '1')
        return sync_dict_list
