# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:23
# @Author : 赵宇飞
# @File : distribution_guotu_dataset.py
import datetime

from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import \
    distribution_guotu


class distribution_guotu_dataset(distribution_guotu):
    """"
    数据集对象处理基类（即时服务）
    """

    def information(self) -> dict:
        info = super().information()
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 指明配置的是更新还是插入，-1时为插入，0为更新
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        return self.get_sync_predefined_dict_list(insert_or_updata)

    def get_sync_predefined_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 指明配置的是更新还是插入，-1时为插入，0为更新
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        datacount:数据数量 secrecylevel:密级 colormodel:色彩模式
        piexldepth:像素位数
        """
        sync_dict_list = list()
        object_table_id = self._obj_id
        object_table_data = self._dataset
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'aprid', object_table_id)

        dsometadataxml = object_table_data.value_by_name(0, 'dsometadataxml', '')
        dsometadataxml_xml = CXml()
        dsometadataxml_xml.load_xml(dsometadataxml)  # 加载查询出来的xml
        self.add_value_to_sync_dict_list(  # 通过本方法配置需要的字典集合
            sync_dict_list, 'productname',  # 配置字段名
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/DSName'))  # 配置字段值
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producttype', object_table_data.value_by_name(0, 'dsodcode', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsodatatype', object_table_data.value_by_name(0, 'dsodatatype', ''))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/BeginDate'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/EndDate'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Date'))
        # datacount:数据数量
        # secrecylevel:密级
        regioncode = dsometadataxml_xml.get_element_text_by_xpath_one('/root/RegionCode')
        self.add_value_to_sync_dict_list(  # regioncode:行政区码
            sync_dict_list, 'regioncode', regioncode)
        self.add_value_to_sync_dict_list(  # regionname:行政区
            sync_dict_list, 'regionname',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/RegionName'))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerx',
            "(select centerx from ro_global_dim_space "
            "where gdscode='{0}')".format(regioncode), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centery',
            "(select centery from ro_global_dim_space "
            "where gdscode='{0}')".format(regioncode), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomwkt',
            "st_astext("
            "(select gdsgeometry from ro_global_dim_space where gdscode='{0}')"
            ")".format(regioncode), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'geomobj',
            "(select gdsgeometry from ro_global_dim_space where gdscode='{0}')".format(regioncode),
            self.DB_False)

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'browserimg', object_table_data.value_by_name(0, 'dso_browser', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'thumbimg', object_table_data.value_by_name(0, 'dso_thumb', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'producetime',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Date'))
        now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'addtime', now_time)
        self.add_value_to_sync_dict_list(  # resolution:分辨率
            sync_dict_list, 'resolution',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Resolution'))

        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imgsize',
            "(select round((sum(dodfilesize)/1048576),2) from dm2_storage_obj_detail "
            "where dodobjectid in "
            "(select dsoid FROM dm2_storage_object WHERE dsoparentobjid='{0}')"
            ")".format(object_table_id),
            self.DB_False)
        # colormodel:交插件处理
        # piexldepth:交插件处理
        if insert_or_updata:
            self.add_value_to_sync_dict_list(sync_dict_list, 'isdel', '0')
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'extent',
            "(select gds_geo_bbox from ro_global_dim_space where gdscode='{0}')".format(regioncode),
            self.DB_False)
        # self.add_value_to_sync_dict_list(
        #     sync_dict_list, 'proj', object_table_data.value_by_name(0, 'dso_prj_coordinate', ''), self.DB_True)
        # remark:暂时为空
        # ispublishservice:暂时为空
        if insert_or_updata:
            self.add_value_to_sync_dict_list(sync_dict_list, 'queryable', '1')
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'mainrssource',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/MajorSource'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'scale',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/ScaleDenominator'))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsdid', object_table_data.value_by_name(0, 'query_directory_id', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsfid', object_table_data.value_by_name(0, 'query_file_id', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedatetag',
            dsometadataxml_xml.get_element_text_by_xpath_one('/root/Date').replace(r'[-/\.年月日]', '')[:8])

        return sync_dict_list
