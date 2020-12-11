# -*- coding: utf-8 -*- 
# @Time : 2020/9/18 09:56 
# @Author : 王西亚 
# @File : c_vectorMDReader.py

import psutil
from osgeo import ogr, osr, gdal

from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_logger import CLogger
from imetadata.base.c_result import CResult
from imetadata.tool.mdreader.c_mdreader import CMDReader


class CVectorMDReader(CMDReader):
    """
    矢量数据文件的元数据读取器
    """

    def get_metadata_2_file(self, file_name_with_path: str):
        # print('你的任务: 将文件{0}的元数据信息, 提取出来, 存储到文件{1}中'.format(self.__file_name_with_path__, file_name_with_path))
        vector_ds = None
        json_vector = None
        # os.environ['PROJ_LIB'] = r'C:\APP\Python\Python38\Lib\site-packages\osgeo\data\proj' 环境变量中设置

        # result_success = abs(self.Success)  # 成功的标记，元数据json中的为1，而系统常量为-1，暂采用绝对值
        result_success = self.Success  # 成功的标记-1

        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        # gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
        gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")

        # 定义矢量的json对象
        json_vector = CJson()

        vector_ds = ogr.Open(self.__file_name_with_path__)
        if vector_ds is None:
            message = '文件[{0}]打开失败!'.format(self.__file_name_with_path__)
            json_vector.set_value_of_name('result', self.Failure)
            json_vector.set_value_of_name('message', message)
            # 判断路径是否存在，不存在则创建
            if CFile.check_and_create_directory(file_name_with_path):
                json_vector.to_file(file_name_with_path)
            return CResult.merge_result(CResult.Failure,
                                        '文件[{0}]打开失败!'.format(self.__file_name_with_path__))

        try:
            layer_count = vector_ds.GetLayerCount()
            if layer_count == 0:
                message = '文件[{0}]没有图层!'.format(self.__file_name_with_path__)
                json_vector.set_value_of_name('result', self.Failure)
                json_vector.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_vector.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]没有图层!'.format(self.__file_name_with_path__))

            shp_lyr = vector_ds.GetLayer(0)
            if shp_lyr is None:
                message = '文件[{0}]读取图层失败!'.format(self.__file_name_with_path__)
                json_vector.set_value_of_name('result', self.Failure)
                json_vector.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_vector.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取图层失败!'.format(self.__file_name_with_path__))
            driver = vector_ds.GetDriver()
            if driver is None:
                message = '文件[{0}]读取驱动失败!'.format(self.__file_name_with_path__)
                json_vector.set_value_of_name('result', self.Failure)
                json_vector.set_value_of_name('message', message)
                # 判断路径是否存在，不存在则创建
                if CFile.check_and_create_directory(file_name_with_path):
                    json_vector.to_file(file_name_with_path)
                return CResult.merge_result(CResult.Failure,
                                            '文件[{0}]读取驱动失败!'.format(self.__file_name_with_path__))

            # 定义datasource子节点,并添加到矢量json对象中
            json_datasource = CJson()
            json_datasource.set_value_of_name('name', self.__file_name_with_path__)
            json_datasource.set_value_of_name('description', driver.name)
            json_vector.set_value_of_name('datasource', json_datasource.json_obj)
            # print(driver.name)

            layer_count_real, layer_list = self.get_vector_layercount_and_layers(vector_ds)
            # print('共{0}个有效图层'.format(layer_count_real))
            # print(layer_list)

            json_vector.set_value_of_name('layer_count', layer_count_real)  # shp图层只有1个，gdb有多个
            json_vector.set_value_of_name('result', result_success)

            # 定义layers子节点,并添加到矢量json对象中
            json_layers = CJson()
            if layer_count_real == 0:
                json_vector.set_value_of_name('layers', [])
            else:
                list_json_layers = []
                for layer_temp in layer_list:
                    print('图层对象: {0}'.format(layer_temp))
                    layer_name = layer_temp.GetName()
                    json_layer = CJson()
                    list_json_layers.append(json_layer.json_obj)
                    # name节点
                    json_layer.set_value_of_name("name", layer_name)
                    json_layer.set_value_of_name("description", layer_name)
                    # print(layer_name)
                    # projwkt 节点
                    json_proj_wkt = self.get_projwkt_by_layer(layer_temp)
                    json_layer.set_value_of_name("wkt", json_proj_wkt.json_obj)
                    # features节点
                    json_features = CJson()
                    feature_count = layer_temp.GetFeatureCount()
                    json_features.set_value_of_name("count", feature_count)
                    json_layer.set_value_of_name("features", json_features.json_obj)
                    # geometry节点
                    json_geometry = self.get_geometry_by_vectorlayer(layer_temp)
                    json_layer.set_value_of_name("geometry", json_geometry.json_obj)
                    # extent节点
                    json_extent = self.get_extent_by_vectorlayer(layer_temp)
                    json_layer.set_value_of_name("extent", json_extent.json_obj)
                    # attributes节点
                    json_attributes = self.get_attributes_by_vectorlayer(layer_temp)
                    json_layer.set_value_of_name("attributes", json_attributes.json_obj)
                    # wgs84节点
                    json_wgs84 = self.transform_to_WGS84(layer_temp)
                    json_layer.set_value_of_name('wgs84', json_wgs84.json_obj)
                json_vector.set_value_of_name('layers', list_json_layers)
            json_shp_str = json_vector.to_json()
            # print(json_shp_str)
            # 判断路径是否存在，不存在则创建
            if CFile.check_and_create_directory(file_name_with_path):
                json_vector.to_file(file_name_with_path)
            CLogger().info('文件[{0}]元数据信息读取成功!'.format(self.__file_name_with_path__))
            return CResult.merge_result(CResult.Success,
                                        '文件[{0}]元数据信息读取成功!'.format(self.__file_name_with_path__))
        except Exception as error:
            CLogger().info('get_metadata_2_file解析错误：{0}'.format(error))
            message = 'get_metadata_2_file解析错误：文件：｛0｝,错误信息为{1}'.format(self.__file_name_with_path__, error)
            json_vector.set_value_of_name('result', self.Failure)
            json_vector.set_value_of_name('message', message)
            # 判断路径是否存在，不存在则创建
            if CFile.check_and_create_directory(file_name_with_path):
                json_vector.to_file(file_name_with_path)
            return CResult.merge_result(CResult.Failure,
                                        '文件[{0}]读取异常!{1}'.format(self.__file_name_with_path__, error.__str__()))
        finally:
            vector_ds.Destroy()
            vector_ds = None

    def transform_to_WGS84(self, layer) -> CJson:
        """
        wgs84坐标系转换结果（wgs84节点）
        :param layer:
        :return:
        """
        json_wgs84 = CJson()
        spatial_ref = osr.SpatialReference()
        spatial_ref.SetWellKnownGeogCS('WGS84')
        wgs84_wkt = spatial_ref.ExportToWkt()
        wgs84_proj4 = spatial_ref.ExportToProj4()
        spatial_ref.MorphToESRI()
        wgs84_esri = spatial_ref.ExportToWkt()
        json_wgs84_coordinate = CJson()
        json_wgs84_coordinate.set_value_of_name('wkt', wgs84_wkt)
        json_wgs84_coordinate.set_value_of_name('proj4', wgs84_proj4)
        json_wgs84_coordinate.set_value_of_name('esri', wgs84_esri)
        json_wgs84.set_value_of_name('coordinate', json_wgs84_coordinate.json_obj)

        spatialRef = layer.GetSpatialRef()
        if spatialRef is None:
            json_wgs84.set_value_of_name('msg',
                                         'extent四至范围从原坐标系转wgs_84坐标系转换失败！失败原因：文件读取空间参考失败！')
        else:
            proj_wkt = spatialRef.ExportToWkt()
            extent = layer.GetExtent()
            rb = (0, 0)
            lu = (0, 0)
            if proj_wkt.strip() != '':
                source_projection = osr.SpatialReference(wkt=proj_wkt)
                source = source_projection.GetAttrValue('GEOGCS', 0)
                prosrs = osr.SpatialReference()
                prosrs.ImportFromWkt(proj_wkt)
                geosrs = prosrs.CloneGeogCS()
                ct = osr.CreateCoordinateTransformation(prosrs, geosrs)
                if ct is not None:
                    rb = ct.TransformPoint(extent[1], extent[2])
                    lu = ct.TransformPoint(extent[0], extent[3])
                    json_bounding = CJson()
                    json_bounding.set_value_of_name('minx', lu[0])
                    json_bounding.set_value_of_name('maxy', lu[1])
                    json_bounding.set_value_of_name('maxx', rb[0])
                    json_bounding.set_value_of_name('miny', rb[1])
                    json_wgs84.set_value_of_name('extent', json_bounding.json_obj)
                    json_wgs84.set_value_of_name('msg', 'extent四至范围从{0}坐标系转wgs_84坐标系转换成功！'.format(source))
                else:
                    json_wgs84.set_value_of_name('msg',
                                                 'extent四至范围从{0}坐标系转wgs_84坐标系转换失败！失败原因：构建坐标转换关系失败！可能是地方坐标系，无法转换。'.format(
                                                     source))
            else:
                json_wgs84.set_value_of_name('msg',
                                             'extent四至范围从原坐标系转wgs_84坐标系转换失败！失败原因：文件不存在wkt信息！')
        return json_wgs84

    def get_attributes_by_vectorlayer(self, layer) -> CJson:
        """
        构建图层字段属性的josn对象
        @param layer:
        @return:
        """
        json_attributes = CJson()
        layer_defn = layer.GetLayerDefn()
        columns_list = []
        field_count = layer_defn.GetFieldCount()
        if field_count > 0:
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
                columns_list.append(json_column.json_obj)  # 添加到集合中
        json_attributes.set_value_of_name("columns", columns_list)
        layer_defn = None
        return json_attributes

    def get_extent_by_vectorlayer(self, layer) -> CJson:
        '''
          构建图层四至范围的json对象
        @param layer:
        @return:
        '''
        json_extent = CJson()
        extent = layer.GetExtent()
        # print('extent:', extent)
        if extent is not None:
            # print('ul:', extent[0], extent[3])
            # print('lr:', extent[1], extent[2])
            json_extent.set_value_of_name("minx", extent[0])
            json_extent.set_value_of_name("maxx", extent[1])
            json_extent.set_value_of_name("miny", extent[2])
            json_extent.set_value_of_name("maxy", extent[3])
        extent = None
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
                        return json_geometry
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
            json_proj_wkt.set_value_of_name('proj4', None)
            json_proj_wkt.set_value_of_name('esri', None)
        else:
            proj_wkt = spatialRef.ExportToWkt()
            proj4 = spatialRef.ExportToProj4()
            spatialRef.MorphToESRI()
            proj_esri = spatialRef.ExportToWkt()
            json_proj_wkt.set_value_of_name('valid', True)
            json_proj_wkt.set_value_of_name('data', proj_wkt)
            json_proj_wkt.set_value_of_name('proj4', proj4)
            json_proj_wkt.set_value_of_name('esri', proj_esri)
            spatialRef = None
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
        # print("iLayerCount:" + str(iLayerCount))
        for i in range(iLayerCount):
            layer = shp_ds.GetLayer(i)
            layer_name = layer.GetName()
            # print('第{0}个图层：{1}'.format(i, layer_name))
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
        json_shp.set_value_of_name('datasource', json_datasource.json_obj)
        json_shp.set_value_of_name('layer_count', '1')

        list_layers = []
        list_layers.append(json_datasource.json_obj)
        json_shp.set_value_of_name('layers', list_layers)
        json_shp.set_value_of_name('valid', True)

        json_shp_str = json_shp.to_json()
        json_shp.to_file(r'c:\app\aa.txt')
        print(json_shp_str)

    def getMemSize(self, pid):
        '''
            根据进程号来获取进程的内存大小 MB
        @param pid:
        @return:
        '''
        process = psutil.Process(pid)
        memInfo = process.memory_full_info()
        return memInfo.uss / 1024 / 1024


if __name__ == '__main__':
    # CVectorMDReader('/aa/bb/cc1.shp').get_metadata_2_file('/aa/bb/cc1.json')
    # CVectorMDReader('/aa/bb/cc2.gdb').get_metadata_2_file('/aa/bb/cc2.json')
    # CVectorMDReader(r'D:\data\0生态审计\少量数据测试_修改后\重大工程项目_曲靖市_2019.shp').get_metadata_2_file(r'C:\app\cc1.json')
    CVectorMDReader(
        r'/Users/wangxiya/Documents/我的测试数据/31.混合存储/测试数据/通用数据/矢量数据集/生态治理和水土保持监测数据库_黑岱沟露天煤矿_10017699_2020d1_2020-01-01.mdb').get_metadata_2_file(
        r'/Users/wangxiya/Documents/我的测试数据/31.混合存储/测试数据/通用数据/矢量数据集/生态治理和水土保持监测数据库_黑岱沟露天煤矿_10017699_2020d1_2020-01-01.json')
    # CVectorMDReader(r'D:\data\0生态审计\其他\新建文件夹2333\gdb测试\gdb\FileGeodb.gdb').get_metadata_2_file(r'C:\app2\cc4.json')
    # CVectorMDReader(r'D:\data\0生态审计\其他\新建文件夹2333\gdb测试\gdb\FileGeodb_noLayer.gdb').get_metadata_2_file(r'M:\app\cc4.json')
    # CVectorMDReader(r'D:\data\0生态审计\其他\新建文件夹2333\gdb测试\gdb\FileGeodb_error.gdb').get_metadata_2_file(r'C:\app\cc6.json')
    # CVectorMDReader(r'D:\data\0生态审计\其他\新建文件夹2333\基本农田保护_藤县_error\基本农田保护_藤县_2010_21.shp').get_metadata_2_file(r'C:\app\cc6.json')
    # CVectorMDReader(r'D:\data\0test\jbnt_2010.shp').test_json()

    # 循环测试内存占用情况
    # process_id = CSys.get_execute_process_id()
    # print("process_id:{0}".format(process_id))
    # time.sleep(2)
    # pVectorMDReader = CVectorMDReader(r'D:\data\0生态审计\其他\新建文件夹2333\gdb测试\gdb\FileGeodb.gdb')
    # # pVectorMDReader = CVectorMDReader(r'D:\data\0生态审计\少量数据测试_修改后\重大工程项目_曲靖市_2019.shp')
    # for i in range(15000):
    #     meta_file = r'C:\app4\cc{0}.json'.format(str(i))
    #     pVectorMDReader.get_metadata_2_file(meta_file)
    #     mem_size = pVectorMDReader.getMemSize(process_id)
    #     print("完成第{0}个数据！,python.exe【process_id:{1}】的内存大小:{2}MB".format(i, process_id, mem_size))
    #     # time.sleep(0.05)
