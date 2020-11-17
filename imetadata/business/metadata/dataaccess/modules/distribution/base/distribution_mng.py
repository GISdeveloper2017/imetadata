# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:30
# @Author : 赵宇飞
# @File : distribution_mng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_dem import distribution_dem
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_dem_noframe import \
    distribution_dem_noframe
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_dom import distribution_dom
from imetadata.database.base.c_dataset import CDataSet


class distribution_mng(CResource):
    @classmethod
    def give_me_distribution(cls, db_id: str, object_def_type: str, object_id: str, object_name: str,
                             quality: str, dataset: CDataSet):
        input_object_def_type = CUtils.any_2_str(object_def_type)

        if CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DOM):
            return distribution_dom(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DEM):
            return distribution_dem(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DEM_NoFrameM):
            return distribution_dem_noframe(db_id, object_id, object_name, quality, dataset)
        # elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DOM):
        #     return distribution_dom(db_id, object_id, object_name, quality, dataset)
        # elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DOM):
        #     return distribution_dom(db_id, object_id, object_name, quality, dataset)
        # else:
        #     # 注意, 这里改为基类了, 因为基类中将默认的处理清除已有附属文件的逻辑
        #     return CDetailParser(object_id, object_name, file_info, file_custom_list)

        # if distribution_obj_real is None:
        #     pass    # TODO 采用默认的处理方式（分对象，数据集）