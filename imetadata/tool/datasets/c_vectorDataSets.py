# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 16:10 
# @Author : 王西亚 
# @File : CVectorDataSets.py
from osgeo import gdal
from osgeo import ogr

from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.exceptions import FileCanNotOpenException
from imetadata.tool.datasets.base.c_datasets_base import CDataSetsBase
from imetadata.tool.datasets.base.vector.c_vector_dataset import CVectorDataSet


class CVectorDataSets(CDataSetsBase):

    def __init__(self, data_file_or_path: str):
        super().__init__()
        self._active = False
        self._data_obj = None
        self._data_file_or_path = data_file_or_path

    @property
    def data_file_or_path(self):
        return self._data_file_or_path

    @property
    def active(self):
        return self._active

    @property
    def data_obj(self):
        return self._data_obj

    def open(self, encoding: str = 'UTF-8'):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        # gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
        gdal.SetConfigOption("SHAPE_ENCODING", encoding)
        # 注册所有的驱动
        ogr.RegisterAll()
        self._active = False
        if not CFile.file_or_path_exist(self.data_file_or_path):
            raise FileNotFoundError(self.data_file_or_path)

        self._data_obj = ogr.Open(self.data_file_or_path, 0)

        if self._data_obj is None:
            raise FileCanNotOpenException(self.data_file_or_path)

        self._active = True

        self._parser_datasets()

    def close(self):
        self.clear()
        self._active = False
        self._data_obj = None

    def layer_by_index(self, index) -> CVectorDataSet:
        return self.item_by_index(index)

    def layer_by_name(self, name) -> CVectorDataSet:
        for layer_index in range(self.size()):
            dataset = self.layer_by_index(layer_index)
            if CUtils.equal_ignore_case(dataset.dataset_name, name):
                return dataset

        return None

    def _parser_datasets(self):
        layer_count = self._data_obj.GetLayerCount()
        for i in range(layer_count):
            layer_obj = self._data_obj.GetLayerByIndex(i)

            if layer_obj is None:
                continue

            if not self._layer_is_dataset(layer_obj):
                continue

            vector_dataset = CVectorDataSet(layer_obj)
            self.add(vector_dataset)

    def _layer_is_dataset(self, layer_obj) -> bool:
        """
        判断一个层是否是合法的数据集
        :param layer_obj:
        :return:
        """
        driver = self._data_obj.GetDriver()
        if driver is None:
            return True

        layer_name = CUtils.any_2_str(layer_obj.GetName())

        if CUtils.equal_ignore_case(driver.name, 'OpenFileGDB'):
            if layer_name.upper().startswith('T_1_'):
                return False
        elif CUtils.equal_ignore_case(driver.name, 'PGeo'):
            if layer_name.upper().endswith('_SHAPE_INDEX'):
                return False
            elif CUtils.equal_ignore_case(layer_name, 'Selections'):
                return False
            elif CUtils.equal_ignore_case(layer_name, 'SelectedObjects'):
                return False

        return True


if __name__ == '__main__':
    # file_name = '/Users/wangxiya/Documents/我的测试数据/31.混合存储/测试数据/通用数据/矢量数据集/生态治理和水土保持监测数据库_黑岱沟露天煤矿_10017699_2020d1_2020-01-01.mdb'
    file_name = '/Users/wangxiya/Documents/我的测试数据/31.混合存储/测试数据/通用数据/矢量/矢量数据/正确数据/生态治理和水土保持监测数据库_利民煤矿_10017574_2020d1_2020-08-05/取排口.shp'
    cpg_file_name = CFile.change_file_ext(file_name, 'cpg')
    encoding = CResource.Encoding_GBK
    if CFile.file_or_path_exist(cpg_file_name):
        encoding = CFile.file_2_str(cpg_file_name)
    vector_datasets = CVectorDataSets(file_name)
    vector_datasets.open(encoding)
    for vector_layer_index in range(vector_datasets.size()):
        vector_dataset = vector_datasets.layer_by_index(vector_layer_index)
        print('*' * 30)
        print('{0}-{1}'.format(vector_dataset.dataset_name, vector_dataset.size()))
        print('*' * 10)
        for field_index in range(vector_dataset.field_count()):
            print('{0}.{1}'.format(vector_dataset.dataset_name, vector_dataset.field_name_by_index(field_index)))

    vector_dataset = vector_datasets.layer_by_index(0)
    print('*' * 30)
    print('{0}-{1}'.format(vector_dataset.dataset_name, vector_dataset.size()))
    print('*' * 10)
    if vector_dataset.first():
        while True:
            print('*' * 20)
            for field_index in range(vector_dataset.field_count()):
                print(
                    '{0}.{1}={2}'.format(
                        vector_dataset.dataset_name,
                        vector_dataset.field_name_by_index(field_index),
                        vector_dataset.value_by_index(field_index, '')
                    )
                )
            if not vector_dataset.next():
                break

    vector_datasets.close()
