# -*- coding: utf-8 -*- 
# @Time : 2020/11/17 10:51
# @Author : 赵宇飞
# @File : distribution_object_dem.py
from imetadata.base.c_json import CJson
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu_object import \
    distribution_guotu_object


class distribution_object_dem(distribution_guotu_object):
    """
    李宪 数据检索分发模块对DEM类型数据
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = 'DEM'
        info['table_name'] = 'ap3_product_rsp_sdem_detail'
        return info

    def access_check_dict(self) -> dict:  # 预留的方法，sync写完后再调
        object_name = self._obj_name
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        xml = CXml()
        xml.load_xml(dsometadataxml_bus)  # 初始化xml
        dsometadataxml_bus_type = '{0}'.format(xml.xpath_one("/root/@type"))  # 查询业务元数据类别
        if object_name is not None:
            if dsometadataxml_bus_type is not None:
                if CUtils.equal_ignore_case(dsometadataxml_bus_type, 'mdb'):
                    return self.access_check_dict_mdb()
                elif CUtils.equal_ignore_case(dsometadataxml_bus_type, 'mat'):
                    return self.access_mdb_check_dict_mat()
                elif CUtils.equal_ignore_case(dsometadataxml_bus_type, 'xls') \
                        or CUtils.equal_ignore_case(dsometadataxml_bus_type, 'xlsx'):
                    return self.access_mdb_check_dict_xls()
                else:
                    return []

    def get_sync_dict_list(self, insert_or_updata) -> list:
        """
        insert_or_updata 中 self.DB_True为insert，DB_False为updata
        本方法的写法为强规则，调用add_value_to_sync_dict_list配置
        第一个参数为list，第二个参数为字段名，第三个参数为字段值，第四个参数为特殊配置
        """
        dsometadataxml_bus = self._dataset.value_by_name(0, 'dsometadataxml_bus', '')
        xml = CXml()
        xml.load_xml(dsometadataxml_bus)
        dsometadataxml_bus_type = '{0}'.format(xml.xpath_one("/root/@type"))
        if self._obj_name is not None:
            if dsometadataxml_bus_type is not None:
                if CUtils.equal_ignore_case(dsometadataxml_bus_type, 'mdb'):
                    return self.get_sync_mdb_dict_list(insert_or_updata)
                elif CUtils.equal_ignore_case(dsometadataxml_bus_type, 'mat'):
                    return self.get_sync_mat_dict_list(insert_or_updata)
                elif CUtils.equal_ignore_case(dsometadataxml_bus_type, 'xls') \
                        or CUtils.equal_ignore_case(dsometadataxml_bus_type, 'xlsx'):
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
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprsdid', object_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprswid', self._dataset.value_by_name(0, 'dsoparentobjid', ''))
        # sync_dict['fname']     #为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'fno', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='th']"))
        '''
                object_name[0:1]    100万图幅行号为字母
                object_name[1:3]    100万图幅列号为数字
                object_name[3:4]    比例尺代码为字母
                object_name[4:7]    图幅行号为数字
                object_name[7:10]   图幅列号为数字
                '''
        if CUtils.text_is_alpha(object_name[0:1]):
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hrowno', object_name[0:1])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hcolno', object_name[1:3])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'scalecode', object_name[3:4])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'rowno', object_name[4:7])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'colno', object_name[7:10])
        # sync_dict['expandextent']  # 为空
        # sync_dict['pupdatedate']  # 为空
        # sync_dict['pversion']  # 为空
        # sync_dict['publishdate']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjgs']"))
        # sync_dict['maindatasource']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'createrorganize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjscdwm']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'submitorganize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjbqdwm']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'copyrightorgnize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='sjcbdwm']"))
        # sync_dict['supplyorganize']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'colormodel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='yxscms']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'piexldepth', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='xsws']"))
        # sync_dict['scale']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'mainrssource', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='wxmc']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'metafilename', '{0}.mdb'.format(object_name))
        # sync_dict_list, 'networksize'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'projinfo', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='dtty']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'zonetype', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='zyzwx']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerline', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='fdfs']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'zoneno',
            CUtils.to_integer(metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='gsklgtydh']"), None))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'coordinateunit', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='zbdw']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'demname', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='gcxtm']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'demstandard', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='gcjz']"))
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='mj']"))
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='dmfbl']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')))
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
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprsdid', object_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprswid', self._dataset.value_by_name(0, 'dsoparentobjid', ''))
        # sync_dict['fname']     # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'fno', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='图号']"))
        '''
                object_name[0:1]    100万图幅行号为字母
                object_name[1:3]    100万图幅列号为数字
                object_name[3:4]    比例尺代码为字母
                object_name[4:7]    图幅行号为数字
                object_name[7:10]   图幅列号为数字
                '''
        if CUtils.text_is_alpha(object_name[0:1]):
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hrowno', object_name[0:1])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hcolno', object_name[1:3])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'scalecode', object_name[3:4])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'rowno', object_name[4:7])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'colno', object_name[7:10])
        # sync_dict['expandextent']  # 为空
        # sync_dict['pupdatedate']  # 为空
        # sync_dict['pversion']  # 为空
        # sync_dict['publishdate']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据格式']"))
        # sync_dict['maindatasource']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'createrorganize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据生产单位名']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'submitorganize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据版权单位名']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'copyrightorgnize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据出版单位名']"))
        # sync_dict['supplyorganize']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'colormodel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='影像色彩模式']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'piexldepth', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='像素位数']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'scale', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='航摄比例尺分母']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'mainrssource', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='卫星名称']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'metafilename', '{0}.mat'.format(object_name))
        # sync_dict_list, 'networksize'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'projinfo', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='地图投影']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'zonetype', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='中央子午线']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerline', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='分带方式']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'zoneno',
            CUtils.to_integer(metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='高斯-克吕格投影带号']"), None))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'coordinateunit', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='坐标单位']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'demname', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='高程系统名']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'demstandard', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='高程基准']"))
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='密级']"))
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='地面分辨率']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')))
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
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprsdid', object_id)
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'aprswid', self._dataset.value_by_name(0, 'dsoparentobjid', ''))
        # sync_dict['fname']     # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'fno', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='图号']"))
        '''
                object_name[0:1]    100万图幅行号为字母
                object_name[1:3]    100万图幅列号为数字
                object_name[3:4]    比例尺代码为字母
                object_name[4:7]    图幅行号为数字
                object_name[7:10]   图幅列号为数字
                '''
        if CUtils.text_is_alpha(object_name[0:1]):
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hrowno', object_name[0:1])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'hcolno', object_name[1:3])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'scalecode', object_name[3:4])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'rowno', object_name[4:7])
            self.add_value_to_sync_dict_list(
                sync_dict_list, 'colno', object_name[7:10])
        # sync_dict['expandextent']  # 为空
        # DATE数据未进行质检，可能会错误#sync_dict['pupdatedate'] '产品更新日期'
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'pversion', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品的版本']"))
        # DATE数据未进行质检，可能会错误#sync_dict['publishdate'] '出版日期'
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dataformat', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='数据格式']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'maindatasource',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='主要数据源']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'dsometadatajson', self._dataset.value_by_name(0, 'dsometadataxml_bus', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'createrorganize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品生产单位名称']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'submitorganize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品所有权权单位名称']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'copyrightorgnize',
            metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='产品出版单位名称']"))
        # sync_dict['supplyorganize']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'colormodel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='影像色彩']"))
        # sync_dict['piexldepth']    # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'scale', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='比例尺分母']"))
        # sync_dict['mainrssource']   # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'metafilename', '{0}.{1}'.format(object_name, metadataxml_bus_xml.xpath_one("/root/@type")))
        # sync_dict_list, 'networksize'  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'projinfo', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='地图投影名称']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'zonetype', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='中央子午线']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'centerline', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='分带方式']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'zoneno',
            CUtils.to_integer(metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='高斯-克吕格投影带号']"), None))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'coordinateunit', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='坐标单位']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'demname', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='高程系统名']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'demstandard', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='高程基准']"))
        # 插件处理字段
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'datacount', self._dataset.value_by_name(0, 'dso_volumn_now', ''))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'secrecylevel', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='密级']"))
        # sync_dict['regioncode']  # 为空
        # sync_dict['regionname']  # 为空
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'resolution', metadataxml_bus_xml.get_element_text_by_xpath_one("//item[@name='影像地面分辨率']"))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'imagedate',
            CUtils.to_day_format(dso_time_json.xpath_one('time', ''), dso_time_json.xpath_one('time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'begdate',
            CUtils.to_day_format(dso_time_json.xpath_one('start_time', ''), dso_time_json.xpath_one('start_time', '')))
        self.add_value_to_sync_dict_list(
            sync_dict_list, 'enddate',
            CUtils.to_day_format(dso_time_json.xpath_one('end_time', ''), dso_time_json.xpath_one('end_time', '')))
        return sync_dict_list

    def access_check_dict_mdb(self) -> dict:
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        check_dict['th'] = 'th'
        check_dict['sjgs'] = 'sjgs'
        check_dict['sjscdwm'] = 'sjscdwm'
        check_dict['sjbqdwm'] = 'sjbqdwm'
        check_dict['sjcbdwm'] = 'sjcbdwm'
        check_dict['yxscms'] = 'yxscms'
        check_dict['xsws'] = 'xsws'
        check_dict['wxmc'] = 'wxmc'
        check_dict['dtty'] = 'dtty'
        check_dict['zyzwx'] = 'zyzwx'
        check_dict['fdfs'] = 'fdfs'
        check_dict['gsklgtydh'] = 'gsklgtydh'
        check_dict['gcxtm'] = 'gcxtm'
        check_dict['gcjz'] = 'gcjz'
        check_dict['mj'] = 'mj'
        check_dict['dmfbl'] = 'dmfbl'
        return check_dict

    def access_mdb_check_dict_mat(self) -> dict:
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        check_dict['图号'] = '图号'
        check_dict['数据格式'] = '数据格式'
        check_dict['数据生产单位名'] = '数据生产单位名'
        check_dict['数据版权单位名'] = '数据版权单位名'
        check_dict['数据出版单位名'] = '数据出版单位名'
        check_dict['影像色彩模式'] = '影像色彩模式'
        check_dict['像素位数'] = '像素位数'
        check_dict['航摄比例尺分母'] = '航摄比例尺分母'
        check_dict['卫星名称'] = '卫星名称'
        check_dict['地图投影'] = '地图投影'
        check_dict['中央子午线'] = '中央子午线'
        check_dict['分带方式'] = '分带方式'
        check_dict['高斯-克吕格投影带号'] = '高斯-克吕格投影带号'
        check_dict['坐标单位'] = '坐标单位'
        check_dict['高程系统名'] = '高程系统名'
        check_dict['高程基准'] = '高程基准'
        check_dict['密级'] = '密级'
        check_dict['地面分辨率'] = '地面分辨率'
        return check_dict

    def access_mdb_check_dict_xls(self) -> dict:
        check_dict = dict()  # 如果有其他需要，则可以升级为json
        check_dict['图号'] = '图号'
        check_dict['产品更新日期'] = '产品更新日期'
        check_dict['产品的版本'] = '产品的版本'
        check_dict['出版日期'] = '出版日期'
        check_dict['数据格式'] = '数据格式'
        check_dict['主要数据源'] = '主要数据源'
        check_dict['产品生产单位名称'] = '产品生产单位名称'
        check_dict['产品所有权权单位名称'] = '产品所有权权单位名称'
        check_dict['产品出版单位名称'] = '产品出版单位名称'
        check_dict['影像色彩'] = '影像色彩'
        check_dict['比例尺分母'] = '比例尺分母'
        check_dict['地图投影名称'] = '地图投影名称'
        check_dict['中央子午线'] = '中央子午线'
        check_dict['分带方式'] = '分带方式'
        check_dict['高斯-克吕格投影带号'] = '高斯-克吕格投影带号'
        check_dict['坐标单位'] = '坐标单位'
        check_dict['高程系统名'] = '高程系统名'
        check_dict['高程基准'] = '高程基准'
        check_dict['密级'] = '密级'
        check_dict['影像地面分辨率'] = '影像地面分辨率'
        return check_dict