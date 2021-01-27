# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 12:03 
# @Author : 王西亚 
# @File : c_viewCreatorRaster.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_object import CObject
from imetadata.base.c_processUtils import CProcessUtils
from imetadata.base.c_result import CResult
from imetadata.base.c_time import CTime
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.metadata.view.c_viewCreatorRaster import CViewCreatorRaster


class CViewCreatorSatRaster(CViewCreatorRaster):
    """
    by 王学谦
    仅用于卫星影像转换的工具包，由于卫星情况较为特殊，本类不作为公共工具方法使用
    本工具会将转换图片放置到工作目录下，在运行卫星数据预览图方法时，会移动到相关目录，而后销毁工作
    """

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx,
                 file_content: CVirtualContent, transform_file):
        self.__transform_file = transform_file
        super().__init__(object_id, object_name, file_info, file_content)

    @property
    def transform_file(self):
        return self.__transform_file

    def process(self) -> str:
        """
        """
        # 获取对象类型
        type = 'default'
        group = 'default'
        catalog = 'default'
        # 构建数据对象object对应的识别插件，获取get_information里面的信息
        class_classified_obj = CObject.get_plugins_instance_by_object_id(self.file_info.db_server_id, self.object_id)
        if class_classified_obj is not None:
            plugins_info = class_classified_obj.get_information()
            type = CUtils.dict_value_by_name(plugins_info, class_classified_obj.Plugins_Info_Type, 'default')
            group = CUtils.dict_value_by_name(plugins_info, class_classified_obj.Plugins_Info_Group, 'default')
            catalog = CUtils.dict_value_by_name(plugins_info, class_classified_obj.Plugins_Info_Catalog, 'default')
        create_time = CTime.today()
        create_format_time = CTime.format_str(create_time, '%Y%m%d')
        year = CTime.format_str(create_time, '%Y')
        month = CTime.format_str(create_time, '%m')
        day = CTime.format_str(create_time, '%d')
        sep = CFile.sep()  # 操作系统的不同处理分隔符不同
        sep_list = [catalog, group, type, year, month, day]
        relative_path_part = sep.join(sep_list)  # 相对路径格式
        view_relative_path_browse = r'{2}{0}{2}{1}_browse.png'.format(relative_path_part, self.object_id, sep)
        view_relative_path_thumb = r'{2}{0}{2}{1}_thumb.jpg'.format(relative_path_part, self.object_id, sep)
        view_relative_path_geotiff = r'{2}{0}{2}{1}_browse.tiff'.format(relative_path_part, self.object_id, sep)

        browse_full_path = CFile.join_file(self.file_content.work_root_dir, view_relative_path_browse)
        thumb_full_path = CFile.join_file(self.file_content.work_root_dir, view_relative_path_thumb)
        geotiff_full_path = CFile.join_file(self.file_content.work_root_dir, view_relative_path_geotiff)

        # 进程调用模式
        json_out_view = CJson()
        json_out_view.set_value_of_name('image_path', self.transform_file)
        json_out_view.set_value_of_name('browse_full_path', browse_full_path)
        json_out_view.set_value_of_name('thumb_full_path', thumb_full_path)
        json_out_view.set_value_of_name('geotiff_full_path', geotiff_full_path)

        result_view = CProcessUtils.processing_method(self.create_view_json, json_out_view)
        # result_view = self.create_view(self.file_info.file_name_with_full_path, browse_full_path, thumb_full_path,
        #                                geotiff_full_path)
        # result_view = self.create_view_json(json_out_view)
        if CResult.result_success(result_view):
            result = CResult.merge_result(self.Success, '处理完毕!')
            result = CResult.merge_result_info(result, self.Name_Browse, view_relative_path_browse)
            result = CResult.merge_result_info(result, self.Name_Thumb, view_relative_path_thumb)
            result = CResult.merge_result_info(result, self.Name_Browse_GeoTiff, view_relative_path_geotiff)
        else:
            result = result_view
        return result
