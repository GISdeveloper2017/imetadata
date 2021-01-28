# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 12:03 
# @Author : 王西亚 
# @File : c_viewCreatorRaster.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_processUtils import CProcessUtils
from imetadata.base.c_result import CResult
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
                 file_content: CVirtualContent, transform_file, view_path):
        self.__transform_file = transform_file
        self.__view_path = view_path
        super().__init__(object_id, object_name, file_info, file_content)

    @property
    def transform_file(self):
        return self.__transform_file

    @property
    def view_path(self):
        return self.__view_path

    def process(self) -> str:
        """
        """
        browse_full_path = CFile.join_file(self.view_path, '{0}_browse.png'.format(self.object_id))
        thumb_full_path = CFile.join_file(self.view_path, '{0_thumb.jpg'.format(self.object_id))
        geotiff_full_path = CFile.join_file(self.view_path, '{0}_browse.tiff'.format(self.object_id))

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
            result = CResult.merge_result_info(result, self.Name_Browse, CFile.file_name(browse_full_path))
            result = CResult.merge_result_info(result, self.Name_Thumb, CFile.file_name(thumb_full_path))
            result = CResult.merge_result_info(result, self.Name_Browse_GeoTiff, CFile.file_name(geotiff_full_path))
        else:
            result = result_view
        return result
