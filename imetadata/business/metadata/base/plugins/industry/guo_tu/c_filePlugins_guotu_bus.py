# -*- coding: utf-8 -*-
# @Time : 2020/10/16 14:15
# @Author : 赵宇飞
# @File : c_filePlugins_guotu_bus.py
from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


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

    def mdb_to_xml(self):
        pass