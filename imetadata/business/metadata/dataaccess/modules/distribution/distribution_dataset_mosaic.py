# -*- coding: utf-8 -*-
# @Time : 2020/11/17 17:00
# @Author : 赵宇飞
# @File : distribution_dataset_mosaic.py
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_dataset import \
    distribution_guotu_dataset


class distribution_dataset_mosaic(distribution_guotu_dataset):
    """
    完成 数据检索分发模块对镶嵌影像数据集类型数据
    镶嵌影像数据集不进行数据检索分发操作
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '镶嵌影像数据集'
        info['table_name'] = 'ap3_product_rsp_mosaic_whole'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        sync_dict_list = list()
        return sync_dict_list
