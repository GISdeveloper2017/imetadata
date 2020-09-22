# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 16:24 
# @Author : 王西亚 
# @File : c_plugins.py

from abc import abstractmethod

from imetadata.base.Exceptions import FileContentWapperNotExistException
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent


class CPlugins(CResource):
    """
    数据识别插件
        处理数据识别和元数据处理的标准模式:
            . 是不是对象
            . 对象的类型
            . 对象的详情: 附属文件
            . 对象的标签: 基于对象的相对路径, 文件名等信息, 进行自动的词库识别, 初步定义对象的归类
            . 对象的质检: 对对象的质量进行检验
            . 对象的基础元数据: 基于对象的数据格式, 提取的对象的元数据, 如矢量, 影像, 图片Exif, 文档, 其中包括空间地理方面的属性
            . 对象的业务元数据: 基于对象的行业标准规范, 提取的对象的业务元数据, 如三调, 地理国情, 单景正射影像
            . 对象的可视元数据: 快视, 缩略图
            . 对象的优化:
                . 影像: 空间外包框 -> 影像外边框
        根据处理效率:
            . 是不是对象: 快
            . 对象的类型: 快
            . 对象的标签: 快
            . 对象的详情: 快
            . 对象的质检: 慢
            . 对象的基础元数据:
                . 成果数据: 快
                . 卫星数据: 慢
            . 对象的业务元数据: 快
            . 对象的可视元数据: 慢
            . 对象的元数据优化: 慢
        根据处理阶段:
            . 是不是对象: 第一阶段, 可以分类统计+浏览+检索
            . 对象的类型: 第一阶段, 可以分类统计+浏览+检索
            . 对象的标签: 第一阶段, 可以分类统计+浏览+检索

            . 对象的详情: 第二阶段, 可以查看详情+高级检索
            . 对象的基础元数据: 第二阶段, 可以查看详情+高级检索
            . 对象的业务元数据: 第二阶段, 可以查看详情+高级检索
            . 对象的可视元数据: 第三阶段, 可以查看快视
            . 对象的元数据优化: 第三阶段, 可以查看更好的快视效果
            . 对象的质检: 第三阶段, 可以查看质量信息
        根据处理所需条件:
            . 是不是对象: 无需打开数据实体
            . 对象的类型: 无需打开数据实体
            . 对象的标签: 无需打开数据实体
            . 对象的详情: 无需打开数据实体
            . 对象的业务元数据: 无需打开数据实体

            . 对象的基础元数据: 需要打开数据实体
            . 对象的可视元数据: 需要打开数据实体
            . 对象的元数据优化: 需要打开数据实体
            . 对象的质检: 需要打开数据实体

        根据上述分析, 确定插件的处理分为如下步骤:
        . 识别-classified:
            . 是不是对象: 无需打开数据实体
            . 对象的类型: 无需打开数据实体
        . 标签解析:
            . 对象的标签: 无需打开数据实体
        . 详情解析:
            . 对象的详情: 无需打开数据实体
        . 元数据解析:
            . 对象的业务元数据: 无需打开数据实体
            . 对象的基础元数据: 需要打开数据实体
            . 对象的质检: 需要打开数据实体
            . 对象的可视元数据: 需要打开数据实体
        . 后处理:
            . 对象的元数据优化: 需要打开数据实体
    """
    # 插件标识-内置
    Plugins_Info_ID = 'dsodid'
    # 插件英文描述-内置
    Plugins_Info_Name = 'dsodname'
    # 插件中文描述-内置
    Plugins_Info_Title = 'dsodtitle'
    # 插件英文编码-业务
    Plugins_Info_Code = 'dsodcode'
    # 插件中文编码-业务
    Plugins_Info_Catalog = 'dsodcatalog'
    # 插件大类-英文-内置
    Plugins_Info_Type = 'dsodtype'
    # 插件大类-中文-内置
    Plugins_Info_Type_Title = 'dsodtype_title'

    # 插件处理引擎-内置-元数据处理
    Plugins_Info_MetaDataEngine = 'dsod_metadata_engine'
    # 插件处理引擎-内置-业务元数据处理
    Plugins_Info_BusMetaDataEngine = 'dsod_bus_metadata_engine'
    # 插件处理引擎-内置-对象详情处理
    Plugins_Info_DetailEngine = 'dsod_detail_engine'
    # 插件处理引擎-内置-标签处理
    Plugins_Info_TagsEngine = 'dsod_tags_engine'
    # 插件处理引擎-内置-对象质检
    Plugins_Info_QCEngine = 'dsod_check_engine'

    MetaDataEngine_Raster = 'raster'
    MetaDataEngine_Vector = 'vector'
    MetaDataEngine_Document = 'document'
    MetaDataEngine_21AT_MBTiles = '21at_mbtiles'
    MetaDataEngine_Custom = 'custom'

    DetailEngine_Same_File_Main_Name = 'same_file_main_name'
    DetailEngine_File_Of_Same_Dir = 'file_of_same_dir'
    DetailEngine_All_File_Of_Same_Dir = 'all_file_of_same_dir'
    DetailEngine_File_Of_Dir = 'file_of_dir'
    DetailEngine_All_File_Of_Dir = 'all_file_of_dir'

    TagEngine_Global_Dim_In_RelationName = 'global_dim_in_relation_name'
    TagEngine_Global_Dim_In_MainName = 'global_dim_in_main_name'

    MetaData_Rule_Type_None = 'none'

    __file_content__: CVirtualContent = None
    __file_info__: CFileInfoEx = None
    __metadata_rule_obj__: CXml = None

    __object_confirm__: int
    __object_name__: str

    def __init__(self, file_info: CFileInfoEx):
        """
        :param file_info:  目标文件或路径的名称
        """
        self.__metadata_rule_obj__ = CXml()
        self.__file_info__ = file_info
        if self.__file_info__ is not None:
            self.__metadata_rule_obj__.load_xml(self.__file_info__.__rule_content__)

    def get_classified_object_confirm(self):
        return self.__object_confirm__

    def get_classified_object_name(self):
        return self.__object_name__

    def get_metadata_rule_type(self):
        default_rule_type = CXml.get_element_text(self.__metadata_rule_obj__.xpath_one(self.Path_MD_Rule_Type))
        if CUtils.equal_ignore_case(default_rule_type, ''):
            default_rule_type = self.MetaData_Rule_Type_None
        return default_rule_type

    def get_information(self) -> dict:
        information = dict()
        information[self.Plugins_Info_ID] = self.get_id()
        return information

    def get_id(self) -> str:
        return type(self).__name__

    @abstractmethod
    def classified(self):
        """
        对目标目录或文件进行分类
        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        pass

    def parser_tags(self) -> list:
        """
        对目标目录或文件的标签进行解析
        :return:
        """
        pass

    def parser_detail(self) -> str:
        """
        对目标目录或文件的详情进行解析
        :return:
        """
        pass

    def parser_metadata(self):
        """
        对目标目录或文件的元数据进行提取
        :return: 返回
        """
        if self.__file_content__ is None:
            raise FileContentWapperNotExistException()

        if not self.__file_content__.virtual_content_valid():
            self.__file_content__.create_virtual_content()

    def quality_evaluate(self) -> list:
        """
        对目标目录或文件的质量评估
        :return:
        """
        if self.__file_content__ is None:
            raise FileContentWapperNotExistException()

        if not self.__file_content__.virtual_content_valid():
            self.__file_content__.create_virtual_content()

    def parser_last_process(self):
        """
        后处理
        :return: 返回
        """
        if self.__file_content__ is None:
            raise FileContentWapperNotExistException()

        if not self.__file_content__.virtual_content_valid():
            self.__file_content__.create_virtual_content()
