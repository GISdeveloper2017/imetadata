# -*- coding: utf-8 -*- 
# @Time : 2020/9/18 09:56 
# @Author : 王西亚 
# @File : c_vectorMDReader.py
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.tool.mdreader.c_mdreader import CMDReader
from osgeo import ogr
import gdal

from test.method import aa


class CVectorMDReader(CMDReader):
    """
    矢量数据文件的元数据读取器
    """

    def get_metadata_2_file(self, file_name_with_path: str):
        print('你的任务: 将文件{0}的元数据信息, 提取出来, 存储到文件{1}中'.format(self.__file_name_with_path__, file_name_with_path))
        vector_ds = None
        json_vector = None
        try:
            result_success = abs(self.Success)  # 成功的标记，元数据json中的为1，而系统常量为-1，暂采用绝对值

            gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
            gdal.SetConfigOption("SHAPE_ENCODING", "GBK")

            # 定义矢量的json对象
            json_vector = CJson()

            vector_ds = ogr.Open(self.__file_name_with_path__)
            if vector_ds is None:
                message = '文件[{0}]打开失败!'.format(self.__file_name_with_path__)
                json_vector.set_value_of_name('result', self.Failure)
                json_vector.set_value_of_name('message', message)
                json_vector.to_file(file_name_with_path)
                #return CMetaDataUtils.merge_result(CMetaDataUtils.Failure,
                #                                   '文件[{0}]打开失败!'.format(self.__file_name_with_path__))
            shp_lyr = vector_ds.GetLayer(0)
            if shp_lyr is None:
                message = '文件[{0}]读取图层失败!'.format(self.__file_name_with_path__)
                json_vector.set_value_of_name('result', self.Failure)
                json_vector.set_value_of_name('message', message)
                json_vector.to_file(file_name_with_path)
                #return CMetaDataUtils.merge_result(CMetaDataUtils.Failure,
                #                                   '文件[{0}]读取图层失败!'.format(self.__file_name_with_path__))
            driver = vector_ds.GetDriver()
            if driver is None:
                message = '文件[{0}]读取驱动失败!'.format(self.__file_name_with_path__)
                json_vector.set_value_of_name('result', self.Failure)
                json_vector.set_value_of_name('message', message)
                json_vector.to_file(file_name_with_path)
                #return CMetaDataUtils.merge_result(CMetaDataUtils.Failure,
                #                                   '文件[{0}]读取驱动失败!'.format(self.__file_name_with_path__))


            # 定义datasource子节点,并添加到矢量json对象中
            json_datasource = CJson()
            json_datasource.set_value_of_name('name', self.__file_name_with_path__)
            json_datasource.set_value_of_name('description', driver.name)
            json_vector.set_value_of_name('datasource', json_datasource.__json_obj__)
            #print(driver.name)

            json_vector.set_value_of_name('layer_count', 1)  # shp图层只有1个
            json_vector.set_value_of_name('result', result_success)

            layer_count_real, layer_list = self.get_vector_layercount_and_layers(vector_ds)
            # print('共{0}个有效图层'.format(layer_count_real))
            # print(layer_list)

            # 定义layers子节点,并添加到矢量json对象中
            json_layers = CJson()
            if layer_count_real == 0:
                json_vector.set_value_of_name('layers', [])
            else:
                list_json_layers = []
                for layer_temp in layer_list:
                    layer_name = layer_temp.GetName()
                    json_layer = CJson()
                    list_json_layers.append(json_layer.__json_obj__)
                    # name节点
                    json_layer.set_value_of_name("name", layer_name)
                    #print(layer_name)
                    # projwkt 节点
                    json_proj_wkt = self.get_projwkt_by_layer(layer_temp)
                    json_layer.set_value_of_name("wkt", json_proj_wkt.__json_obj__)
                    # features节点
                    json_features = CJson()
                    feature_count = layer_temp.GetFeatureCount()
                    json_features.set_value_of_name("count", feature_count)
                    json_layer.set_value_of_name("features", json_features.__json_obj__)
                    # geometry节点
                    json_geometry = self.get_geometry_by_vectorlayer(layer_temp)
                    json_layer.set_value_of_name("geometry", json_geometry.__json_obj__)
                    # extent节点
                    json_extent = self.get_extent_by_vectorlayer(layer_temp)
                    json_layer.set_value_of_name("extent", json_extent.__json_obj__)
                    # attributes节点
                    json_attributes = self.get_attributes_by_vectorlayer(layer_temp)
                    json_layer.set_value_of_name("attributes", json_attributes.__json_obj__)
                json_vector.set_value_of_name('layers', list_json_layers)
            json_shp_str = json_vector.to_json()
            print(json_shp_str)
            json_vector.to_file(file_name_with_path)
            CLogger().info('文件[{0}]元数据信息读取成功!'.format(self.__file_name_with_path__))
            #return CMetaDataUtils.merge_result(CMetaDataUtils.Success,
            #                                   '文件[{0}]元数据信息读取成功!'.format(self.__file_name_with_path__))
        except Exception as error:
            CLogger().info('get_metadata_2_file解析错误：{0}'.format(error))
            message = 'get_metadata_2_file解析错误：文件：｛0｝,错误信息为{1}'.format(self.__file_name_with_path__, error)
            json_vector.set_value_of_name('result', self.Failure)
            json_vector.set_value_of_name('message', message)
            json_vector.to_file(file_name_with_path)
            #return CMetaDataUtils.merge_result(CMetaDataUtils.Failure,
            #                                   '文件[{0}]读取异常!｛1｝'.format(self.__file_name_with_path__,error))
        finally:
            if vector_ds is not None:
                vector_ds.Destroy()

    def get_attributes_by_vectorlayer(self, layer) -> CJson:
        '''
          构建图层字段属性的josn对象
        @param layer:
        @return:
        '''
        json_attributes = CJson()
        layer_defn = layer.GetLayerDefn()
        columns_list = []
        field_count = layer_defn.GetFieldCount()
        if field_count >0 :
            for i in range(field_count):
                field_defn = layer_defn.GetFieldDefn(i)
                name = field_defn.GetName()
                type_code = field_defn.GetType()
                width = field_defn.GetWidth()
                precision = field_defn.GetPrecision()
                type_name = field_defn.GetFieldTypeName(type_code)
                # 构建单个字段的json对象
                json_column = CJson()
                json_column.set_value_of_name("name", name)
                json_column.set_value_of_name("type", type_code)
                json_column.set_value_of_name("width", width)
                json_column.set_value_of_name("precision", precision)
                json_column.set_value_of_name("type_name", type_name)
                columns_list.append(json_column.__json_obj__)  # 添加到集合中
        json_attributes.set_value_of_name("columns", columns_list)
        return json_attributes

    def get_extent_by_vectorlayer(self, layer) -> CJson:
        '''
          构建图层四至范围的json对象
        @param layer:
        @return:
        '''
        json_extent = CJson()
        extent = layer.GetExtent()
        #print('extent:', extent)
        if extent is not None:
            # print('ul:', extent[0], extent[3])
            # print('lr:', extent[1], extent[2])
            json_extent.set_value_of_name("minx", extent[0])
            json_extent.set_value_of_name("maxx", extent[1])
            json_extent.set_value_of_name("miny", extent[2])
            json_extent.set_value_of_name("maxy", extent[3])
        return json_extent

    def get_geometry_by_vectorlayer(self, layer) -> CJson:
        '''
          构建图层图形类型的json对象
        @param layer:
        @return:
        '''
        json_geometry = CJson()
        geomtype = layer.GetGeomType()  # 数字
        json_geometry.set_value_of_name("type", geomtype)
        feature_count = layer.GetFeatureCount()
        if feature_count > 0:
            for i in range(feature_count):
                feature = layer.GetFeature(i)
                if feature is not None:
                    geom = feature.geometry()
                    if geom is not None:
                        geom_name = geom.GetGeometryName()
                        json_geometry.set_value_of_name("name", geom_name)
                        return json_geometry;
        return json_geometry

    def get_projwkt_by_layer(self, layer) -> CJson:
        '''
            根据图层对象获取空间参考的wkt对象节点
        @param layer:
        @return:
        '''
        json_proj_wkt = CJson()
        spatialRef = layer.GetSpatialRef()
        if spatialRef is None:
            json_proj_wkt.set_value_of_name('valid', False)
            json_proj_wkt.set_value_of_name('data', None)
        else:
            proj_wkt = spatialRef.ExportToWkt()
            json_proj_wkt.set_value_of_name('valid', True)
            json_proj_wkt.set_value_of_name('data', proj_wkt)
        return json_proj_wkt

    def get_vector_layercount_and_layers(self, datasource) -> (int, []):
        """
            获取矢量数据的图层个数和名称集合
        @param datasource:
        @return:
        """
        layer_count_real = 0
        layer_list = []
        driver = datasource.GetDriver()
        if driver is None:
            return layer_count_real, layer_list
        # gdb数据层里有一些是内置的拓扑检查的图层, 不要列入这部分为好
        shp_ds = datasource
        iLayerCount = shp_ds.GetLayerCount()
        #print("iLayerCount:" + str(iLayerCount))
        for i in range(iLayerCount):
            layer = shp_ds.GetLayer(i)
            layer_name = layer.GetName()
            # print('第{0}个图层：{1}'.format(i,layer_name))
            if driver.name == 'OpenFileGDB':
                if layer_name.startswith('T_1_'):
                    continue
            layer_count_real = layer_count_real + 1
            layer_list.append(layer)
        return layer_count_real, layer_list

    def test_json(self):
        json_shp = CJson()
        json_datasource = CJson()
        json_datasource.set_value_of_name('name', r'镶嵌影像\\石嘴山市-3xq.shp')
        json_datasource.set_value_of_name('description', 'ESRI Shapefile')
        json_datasource_str = json_datasource.to_json()
        print(json_datasource_str)
        json_shp.set_value_of_name('datasource', json_datasource.__json_obj__)
        json_shp.set_value_of_name('layer_count', '1')

        list_layers = []
        list_layers.append(json_datasource.__json_obj__)
        json_shp.set_value_of_name('layers', list_layers)
        json_shp.set_value_of_name('valid', True)

        json_shp_str = json_shp.to_json()
        json_shp.to_file(r'c:\app\aa.txt')
        print(json_shp_str)


if __name__ == '__main__':
    # CVectorMDReader('/aa/bb/cc1.shp').get_metadata_2_file('/aa/bb/cc1.json')
    # CVectorMDReader('/aa/bb/cc2.gdb').get_metadata_2_file('/aa/bb/cc2.json')
    # CVectorMDReader(r'D:\data\0生态审计\少量数据测试_修改后\重大工程项目_曲靖市_2019.shp').get_metadata_2_file(r'C:\app\cc1.json')
     CVectorMDReader(r'D:\data\0生态审计\其他\新建文件夹2333\gdb测试\gdb\FileGeodb.gdb').get_metadata_2_file(r'C:\app\cc4.json')
    # CVectorMDReader(r'D:\data\0test\jbnt_2010.shp').test_json()
