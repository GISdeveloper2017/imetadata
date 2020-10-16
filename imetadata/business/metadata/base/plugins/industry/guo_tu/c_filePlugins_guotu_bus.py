# -*- coding: utf-8 -*-
# @Time : 2020/10/16 14:15
# @Author : 赵宇飞
# @File : c_filePlugins_guotu_bus.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
import pypyodbc


class CFilePlugins_GUOTU_BUS(CFilePlugins_GUOTU):
    """
    国土行业文件入库插件-业务通用方法
    """

    def identify_dom_or_dem_metadata_bus_file(self) -> bool:
        """
          识别dom/dem的业务元数据文件（xls/xlsx/mat/mdb），并赋值到私有变量中
        """
        file_metadata_name_with_path = CFile.join_file(self.file_info.__file_path__,
                                                       self.file_info.__file_main_name__)
        check_file_metadata_name_exist = False
        ext_list = ['xls', 'xlsx', 'mat', 'mdb']
        for ext in ext_list:
            temp_metadata_bus_file = '{0}.{1}'.format(file_metadata_name_with_path, ext)
            if CFile.file_or_path_exist(temp_metadata_bus_file):
                check_file_metadata_name_exist = True
                self._metadata_bus_file_ext = ext
                self._metadata_bus_file_with_path = temp_metadata_bus_file
                break
        return check_file_metadata_name_exist

    def identify_21atxml_metadata_bus_file(self) -> bool:
        """
          TODO 王学谦 识别_21at.xml模式的业务元数据文件，并赋值到私有变量中
        """
        return False

    def mdb_to_xml(self, file_main_name, file_with_path, xml_obj):
        """
         TODO 王学谦 mdb文件转xml文件 by王学谦 初版，需要改进与调试
        :param file_main_name:文件主名，不带后缀名，同时也是mdb的表名
        :param file_with_path:文件全名，带路径
        :param xml_obj:进行转换的xml对象，一半在函数外提前定义
        :return: xml_obj:转换好的xml对象
        """
        tablename = file_main_name  # 暂时 表名为与文件名一样 by王学谦

        # conn = pypyodbc.connect('DSN=mdb'); #linux配置，需要配置mdbtools, unixODBC, libmdbodbc
        mdb = 'Driver={Microsoft Access Driver (*.mdb,*.accdb)};' + 'DBQ={0}'.format(file_with_path)  # win的驱动，需要安装
        conn = pypyodbc.win_connect_mdb(mdb)  # 安装pypyodbc插件，本插件为python写的，可全平台
        cur = conn.cursor()
        sql = "SELECT * FROM " + tablename
        cur.execute(sql)
        alldata = cur.fetchall()
        # total_rows = len(alldata)  # 行
        # total_cols = len(alldata[0])  # 列
        node_property = xml_obj.create_element(xml_obj.xpath_one('/root'), 'property')
        xml_obj.set_attr(node_property, 'tablename', tablename)
        for field_index, row_obj in enumerate(cur.description):
            if CUtils.equal_ignore_case(row_obj[0], 'shape'):  # 跳过shape字段
                continue
            node_item = xml_obj.create_element(node_property, 'item')
            xml_obj.set_attr(node_item, 'name', row_obj[0])
            xml_obj.set_element_text(node_item, alldata[0][field_index])
        cur.close()
        conn.close()
        return xml_obj
