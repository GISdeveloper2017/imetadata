# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 11:30
# @Author : 赵宇飞
# @File : distribution_mng.py
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_dataset.distribution_dem_dataset import \
    distribution_dem_dataset
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_dataset.distribution_dom_dataset import \
    distribution_dom_dataset
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_dataset.distribution_guoqing_dataset import \
    distribution_guoqing_dataset
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_dataset.distribution_mosaic_dataset import \
    distribution_mosaic_dataset
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_dataset.distribution_ortho_dataset import \
    distribution_ortho_dataset
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_dataset.distribution_third_survey_dataset import \
    distribution_third_survey_dataset
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_default import \
    distribution_default
from imetadata.database.base.c_dataset import CDataSet
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_custom import \
    distribution_custom
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_dem import distribution_dem
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_dem_noframe import \
    distribution_dem_noframe
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_dom import distribution_dom
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_guoqing_frame import \
    distribution_guoqing_frame
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_guoqing_scene import \
    distribution_guoqing_scene
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_mosaic import \
    distribution_mosaic
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_ortho import \
    distribution_ortho
from imetadata.business.metadata.dataaccess.modules.distribution.guotu_object.distribution_third_survey import \
    distribution_third_survey


class distribution_mng(CResource):
    """
    同步第三方系统（即时服务系统数据库）的工厂处理，根据对象对应object_def表中的类型区分
    """

    @classmethod
    def give_me_distribution(cls, db_id: str, object_def_type: str, object_id: str, object_name: str,
                             quality: str, dataset: CDataSet):
        input_object_def_type = CUtils.any_2_str(object_def_type)
        # 1.独立对象（9个）
        if CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DOM):
            return distribution_dom(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DEM):
            return distribution_dem(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DEM_NoFrame):
            return distribution_dem_noframe(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Guoqing_Frame):
            return distribution_guoqing_frame(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Guoqing_Scene):
            return distribution_guoqing_scene(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Mosaic):
            return distribution_mosaic(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Ortho):
            return distribution_ortho(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Third_Survey):
            return distribution_third_survey(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Custom):
            return distribution_custom(db_id, object_id, object_name, quality, dataset)
        # 2.数据集对象（6个）
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_DOM):
            return distribution_dom_dataset(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_DEM) \
                or CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_DEM_Frame) \
                or CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_DEM_NoFrame):
            return distribution_dem_dataset(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_Guoqing) \
                or CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_Guoqing_Frame) \
                or CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_Guoqing_Scene):
            return distribution_guoqing_dataset(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_Mosaic):
            return distribution_mosaic_dataset(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_Ortho):
            return distribution_ortho_dataset(db_id, object_id, object_name, quality, dataset)
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_DataSet_Third_Survey):
            return distribution_third_survey_dataset(db_id, object_id, object_name, quality, dataset)
        # 3.通用影像对象raster ——即时服务中被认为是自定义影像
        elif CUtils.equal_ignore_case(input_object_def_type, cls.Object_Def_Type_Raster):
            return distribution_custom(db_id, object_id, object_name, quality, dataset)
        else:
            # 注意, 这里默认为默认处理的同步插件，先预留
            return distribution_default(db_id, object_id, object_name, quality, dataset)
