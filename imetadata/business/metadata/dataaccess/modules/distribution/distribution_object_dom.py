# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 15:30
# @Author : 赵宇飞
# @File : distribution_object_dom.py
from imetadata.base.c_json import CJson
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_dom(distribution_guotu_object):
    """
    李宪 数据检索分发模块对DOM类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'DOM'
        info['table_name'] = 'ap3_product_rsp_sdom_detail'
        return info

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        xml = CXml()
        xml.load_xml(dsometadataxml_bus)    # 初始化xml
        dsometadataxml_bus_type = '{0}'.format(xml.xpath_one("/root/@type"))    # 查询业务元数据类别
        if object_name is not None:
            if dsometadataxml_bus_type is not None:
                if CUtils.equal_ignore_case(dsometadataxml_bus_type,'mdb'):
                    return self.get_sync_mdb_dict_list(insert_or_updata)
                elif CUtils.equal_ignore_case(dsometadataxml_bus_type,'mat'):
                    return self.get_sync_mat_dict_list(insert_or_updata)
                elif CUtils.equal_ignore_case(dsometadataxml_bus_type,'xls')\
                        or CUtils.equal_ignore_case(dsometadataxml_bus_type,'xlsx'):
                    return self.get_sync_xls_dict_list(insert_or_updata)
                else:
                    return []

    def get_sync_mdb_dict_list(self, insert_or_updata) -> list:
        """
                insert_or_updata 中 self.DB_True为insert，DB_False为updata
                本方法的写法为强规则，调用add_value_to_sync_dict_list配置
                第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
                """
        object_id = self._obj_id
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        dso_time = self._dataset.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()  # 时间数据json
        dso_time_json.load_obj(dso_time)
        metadataxml_bus_xml = CXml()  # 业务元数据xml
        metadataxml_bus_xml.load_xml(dsometadataxml_bus)

        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list,'aprsdid', object_id,self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprswid', self._dataset.value_by_name(0, 'dsoparentobjid', ''), self.DB_True)
        # sync_dict['fname']   #为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'fno', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='th']"), self.DB_True)
        '''
                object_name[0:1]    100万图幅行号为字母
                object_name[1:3]    100万图幅列号为数字
                object_name[3:4]    比例尺代码为字母
                object_name[4:7]    图幅行号为数字
                object_name[7:10]   图幅列号为数字
                '''
        if CUtils.text_is_alpha(object_name[0:1]):
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hrowno', object_name[0:1], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hcolno', object_name[1:3], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'scalecode', object_name[3:4], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'rowno', object_name[4:7], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'colno', object_name[7:10], self.DB_True)
        # sync_dict['expandextent']  # 为空
        # sync_dict['pupdatedate']  # 为空
        # sync_dict['pversion']  # 为空
        # sync_dict['publishdate']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjgs']"), self.DB_True)
        # sync_dict['maindatasource']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'createrorganize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjscdwm']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'submitorganize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjbqdwm']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'copyrightorgnize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjcbdwm']"), self.DB_True)
        # sync_dict['supplyorganize']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'colormodel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='yxscms']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'piexldepth', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='xsws']"), self.DB_True)
        # sync_dict['scale']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'mainrssource', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='wxmc']"), self.DB_True)
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='mj']"), self.DB_True)
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='dmfbl']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')),
            self.DB_True)
        return sync_dict_list

    def get_sync_mat_dict_list(self, insert_or_updata) -> list:
        """
                insert_or_updata 中 self.DB_True为insert，DB_False为updata
                本方法的写法为强规则，调用add_value_to_sync_dict_list配置
                第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
                """
        object_id = self._obj_id
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        dso_time = self._dataset.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()  # 时间数据json
        dso_time_json.load_obj(dso_time)
        metadataxml_bus_xml = CXml()  # 业务元数据xml
        metadataxml_bus_xml.load_xml(dsometadataxml_bus)

        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'aprsdid', object_id, self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprswid', self._dataset.value_by_name(0, 'dsoparentobjid', ''), self.DB_True)
        # sync_dict['fname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'fno', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='图号']"), self.DB_True)
        '''
                object_name[0:1]    100万图幅行号为字母
                object_name[1:3]    100万图幅列号为数字
                object_name[3:4]    比例尺代码为字母
                object_name[4:7]    图幅行号为数字
                object_name[7:10]   图幅列号为数字
                '''
        if CUtils.text_is_alpha(object_name[0:1]):
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hrowno', object_name[0:1], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hcolno', object_name[1:3], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'scalecode', object_name[3:4], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'rowno', object_name[4:7], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'colno', object_name[7:10], self.DB_True)
        # sync_dict['expandextent']  # 为空
        # sync_dict['pupdatedate']  # 为空
        # sync_dict['pversion']  # 为空
        # sync_dict['publishdate']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据格式']"), self.DB_True)
        # sync_dict['maindatasource']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'createrorganize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据生产单位名']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'submitorganize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据版权单位名']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'copyrightorgnize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据出版单位名']"), self.DB_True)
        # sync_dict['supplyorganize']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'colormodel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='影像色彩模式']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'piexldepth', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='像素位数']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'scale', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='航摄比例尺分母']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'mainrssource', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='卫星名称']"), self.DB_True)
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='密级']"), self.DB_True)
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='地面分辨率']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate', CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate', CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate', CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')), self.DB_True)
        return sync_dict_list

    def get_sync_xls_dict_list(self, insert_or_updata) -> list:
        """
                insert_or_updata 中 self.DB_True为insert，DB_False为updata
                本方法的写法为强规则，调用add_value_to_sync_dict_list配置
                第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
                """
        object_id = self._obj_id
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        dso_time = self._dataset.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()  # 时间数据json
        dso_time_json.load_obj(dso_time)
        metadataxml_bus_xml = CXml()  # 业务元数据xml
        metadataxml_bus_xml.load_xml(dsometadataxml_bus)

        sync_dict_list = self.get_sync_predefined_dict_list(insert_or_updata)
        if insert_or_updata:
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'aprsdid', object_id, self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprswid', self._dataset.value_by_name(0, 'dsoparentobjid', ''), self.DB_True)
        # sync_dict['fname']   # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'fno', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='图号']"), self.DB_True)
        '''
                object_name[0:1]    100万图幅行号为字母
                object_name[1:3]    100万图幅列号为数字
                object_name[3:4]    比例尺代码为字母
                object_name[4:7]    图幅行号为数字
                object_name[7:10]   图幅列号为数字
                '''
        if CUtils.text_is_alpha(object_name[0:1]):
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hrowno', object_name[0:1], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hcolno', object_name[1:3], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'scalecode', object_name[3:4], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'rowno', object_name[4:7], self.DB_True)
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'colno', object_name[7:10], self.DB_True)
        # sync_dict['expandextent']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'pupdatedate', CUtils.to_day_format(
                metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品更新日期']"),
                metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品更新日期']")
            ),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'pversion', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品的版本']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'publishdate', CUtils.to_day_format(
                metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='出版日期']"),
                metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='出版日期']")
            ),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据格式']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'maindatasource', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='主要数据源']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'createrorganize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品生产单位名称']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'submitorganize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品所有权权单位名称']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'copyrightorgnize', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品出版单位名称']"), self.DB_True)
        # sync_dict['supplyorganize']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'colormodel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='影像色彩']"), self.DB_True)
        # sync_dict['piexldepth']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'scale', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='比例尺分母']"), self.DB_True)
        # sync_dict['mainrssource']  # 为空
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''), self.DB_False)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='密级']"), self.DB_True)
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='影像地面分辨率']"), self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')),
            self.DB_True)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')),
            self.DB_True)
        return sync_dict_list
