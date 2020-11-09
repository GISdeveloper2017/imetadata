# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:57 
# @Author : 王西亚 
# @File : c_mdExtractor.py
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.metadata.c_metadata import CMetaData


class CSpatialExtractor(CParser):
    __file_content: CVirtualContent = None

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx, file_content: CVirtualContent,
                 metadata: CMetaData):
        self.__file_content = file_content
        self.__meta_data = metadata
        super().__init__(object_id, object_name, file_info)

    @property
    def file_content(self):
        return self.__file_content

    @property
    def metadata(self):
        return self.__meta_data

    def get_prj_degree_zone(self, spatial_ref):
        """
        由投影坐标系名称获取分带情况。
        Beijing_1954_3_Degree_GK_CM_75E
        Xian 1980 / 3-degree Gauss-Kruger zone 25
        Xian 1980 / 3-degree Gauss-Kruger CM 84E
        CGCS2000 / 3-degree Gauss-Kruger zone 43
        CGCS2000 / 3 degree Gauss-Kruger zone 43
        @param:spatial_ref
        @return:
        """
        native_degree = None
        native_zone = None
        # 读取坐标系名称
        project_cs = spatial_ref.GetAttrValue('PROJCS')
        # 3度分带
        if ('3-degree' in project_cs.lower()) \
                or ('3_degree' in project_cs.lower()) \
                or ('3 degree' in project_cs.lower()):
            native_degree = 3
            # 判断连字符类型
            link_real = None
            link_list = [' ', '-', '_']
            for link in link_list:
                if link in project_cs:
                    link_real = link
                    break
            project_cs = project_cs.split(link_real)
            for i in range(len(project_cs)):
                # 直接给出带号
                if project_cs[i].lower() == 'zone':
                    native_zone = project_cs[i + 1]
                    break
                # 由中央经线计算带号
                elif project_cs[i].lower() == 'cm':
                    meridian = project_cs[i + 1].split('E')[0]
                    meridian = CUtils.to_decimal(meridian)
                    native_zone = CUtils.to_integer((meridian + 1.5) / 3)
                    break
        # 6度分带
        elif ('6-degree' in project_cs.lower()) \
                or ('6_degree' in project_cs.lower()) \
                or ('6 degree' in project_cs.lower()):
            native_degree = 6
            # 判断连字符类型
            link_real = None
            link_list = [' ', '-', '_']
            for link in link_list:
                if link in project_cs:
                    link_real = link
                    break
            project_cs = project_cs.split(link_real)

            for i in range(len(project_cs)):
                # 直接给出带号
                if project_cs[i].lower() == 'zone':
                    native_zone = project_cs[i + 1]
                    break
                # 由中央经线计算带号
                elif project_cs[i].lower() == 'cm':
                    meridian = project_cs[i + 1].split('E')[0]
                    meridian = CUtils.to_decimal(meridian)
                    native_zone = CUtils.to_integer((meridian + 6) / 6)
                    break
        # 没有分带
        else:
            native_degree = None
            native_zone = None
        return native_degree, native_zone

    # def get_prj_zone(self, spatial_ref, pixel_size):
    #     """
    #     获取数据所在的带区，函数预留
    #     """
    #     meridian = spatial_ref.GetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN)
    #     meridian = CUtils.to_decimal(meridian)
    #     pixel = CUtils.to_decimal(pixel_size)
    #     scale = pixel / ((1 / 96) * (25.4 / 1000))
    #     if scale < 25000:
    #         number_zone = CUtils.to_integer((meridian + 1.5) / 3)
    #     else:
    #         number_zone = CUtils.to_integer((meridian + 6) / 6)
    #     return number_zone
