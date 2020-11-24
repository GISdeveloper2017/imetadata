# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 17:02
# @Author : 赵宇飞
# @File : distribution_dataset_ortho.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_dataset import \
    distribution_guotu_dataset


class distribution_dataset_ortho(distribution_guotu_dataset):
    """
    完成 数据检索分发模块对单景正射数据集类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '单景正射数据集'
        info['table_name'] = 'ap3_product_rsp_os_whole'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        object_table_id = self._obj_id
        object_table_data = self._dataset
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'aprowid', object_table_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datatype', object_table_data.value_by_name(0, 'dsodatatype', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', object_table_data.value_by_name(0, 'dsometadataxml_bus', ''))

        return sync_dict_list
