# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 16:24 
# @Author : 王西亚 
# @File : c_plugins.py

from abc import abstractmethod

from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.base.exceptions import FileContentWapperNotExistException
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser


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
            . 对象的元数据优化: 需要打开数据实体
        . 后处理:
            . 与业务系统的接口
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
    # 插件-对象是否允许包含子对象
    Plugins_Info_HasChildObj = 'dsod_has_child_obj'

    # 插件处理引擎-内置-元数据处理
    Plugins_Info_MetaDataEngine = 'dsod_metadata_engine'
    # 插件处理引擎-内置-业务元数据处理
    Plugins_Info_BusMetaDataEngine = 'dsod_bus_metadata_engine'
    # 插件处理引擎-内置-对象详情处理
    Plugins_Info_DetailEngine = 'dsod_detail_engine'
    # 插件处理引擎-内置-标签处理
    Plugins_Info_TagsEngine = 'dsod_tags_engine'
    # 插件处理引擎-内置-快视图处理
    Plugins_Info_ViewEngine = 'dsod_view_engine'
    # 插件处理引擎-内置-空间处理
    Plugins_Info_SpatialEngine = 'dsod_spatial_engine'

    MetaData_Rule_Type_None = 'none'

    __file_content__: CVirtualContent = None
    __file_info__: CDMFilePathInfoEx = None
    __metadata_rule_obj__: CXml = None

    __object_confirm__: int
    __object_name__: str

    def __init__(self, file_info: CDMFilePathInfoEx):
        """
        :param file_info:  目标文件或路径的名称
        """
        self.__metadata_rule_obj__ = CXml()
        self.__file_info__ = file_info
        if self.file_info is not None:
            self.__metadata_rule_obj__.load_xml(self.file_info.__rule_content__)

    @property
    def file_content(self):
        return self.__file_content__

    @property
    def file_info(self):
        return self.__file_info__

    def classified_object_confirm(self):
        return self.__object_confirm__

    def classified_object_name(self):
        return self.__object_name__

    def get_metadata_rule_type(self):
        default_rule_type = CXml.get_element_text(self.__metadata_rule_obj__.xpath_one(self.Path_MD_Rule_Type))
        if CUtils.equal_ignore_case(default_rule_type, ''):
            default_rule_type = self.MetaData_Rule_Type_None
        return default_rule_type

    def get_information(self) -> dict:
        information = dict()
        information[self.Plugins_Info_ID] = self.get_id()
        information[self.Plugins_Info_ViewEngine] = None
        information[self.Plugins_Info_SpatialEngine] = None
        information[self.Plugins_Info_HasChildObj] = self.DB_False

        return information

    def get_id(self) -> str:
        return type(self).__name__

    @abstractmethod
    def classified(self):
        """
        对目标目录或文件进行分类
        :return: 返回两个结果
        .[0]: 概率, 0-不知道;1-可能是;-1确认是;2-确定不是
        .[1]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        """
        pass

    def parser_tags(self, parser: CParser) -> str:
        """
        对目标目录或文件的标签进行解析
        :return:
        """
        if not isinstance(parser, CParserCustom):
            return parser.process()

        return CResult.merge_result(self.Success, '处理完毕!')

    def parser_detail(self, parser: CParser) -> str:
        """
        对目标目录或文件的详情进行解析
        :return:
        """
        if not isinstance(parser, CParserCustom):
            return parser.process()

        return CResult.merge_result(self.Success, '处理完毕!')

    def create_file_content(self):
        pass

    def create_virtual_content(self) -> bool:
        if self.__file_content__ is None:
            self.create_file_content()

        if self.__file_content__ is None:
            raise FileContentWapperNotExistException()

        if not self.__file_content__.virtual_content_valid():
            return self.__file_content__.create_virtual_content()
        else:
            return True

    def destroy_virtual_content(self):
        if self.__file_content__ is None:
            self.create_file_content()

        if self.__file_content__ is None:
            raise FileContentWapperNotExistException()

        if self.__file_content__.virtual_content_valid():
            self.__file_content__.destroy_virtual_content()

    def parser_metadata(self, parser: CMetaDataParser) -> str:
        """
        对目标目录或文件的元数据进行提取
        本方法禁止出现异常! 所有的异常都应该控制在代码中!
        1. 首先进行预定义的质检
            1. 预定义的质检包括两类:
                1. 附属文件缺项检测
                1. XML元数据数据项检测
        :return: 返回
        """
        parser.process()

        # 首先要判断和验证与数据质量相关的核心内容
        self.parser_metadata_with_qa(parser)

        # 其次, 根据合法的数据\元数据\业务元数据内容, 提取其他元数据内容, 如果其中出现异常, 则写入质检结果中
        self.parser_metadata_after_qa(parser)

        # 这里应该永远都是成功信息
        return CResult.merge_result(
            self.Success,
            '数据[{0}]的全部元数据解析完毕! '.format(
                self.file_info.__file_name_with_full_path__,
            )
        )

    def parser_last_process(self, parser: CParser) -> str:
        """
        后处理
        :return: 返回
        """
        if not isinstance(parser, CParserCustom):
            return parser.process()

        return CResult.merge_result(self.Success, '处理完毕!')

    def init_metadata(self, parser: CMetaDataParser) -> str:
        """
        提取xml或json格式的元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        default_metadata_engine = CUtils.dict_value_by_name(
            self.get_information(),
            self.Plugins_Info_MetaDataEngine,
            None)
        if default_metadata_engine is not None:
            result = parser.process_default_metadata(default_metadata_engine)
            if CResult.result_success(result):
                metadata_format = CResult.result_info(result, self.Name_Format, self.MetaDataFormat_Text)

                file_metadata_name_with_path = CFile.join_file(self.file_content.work_root_dir, self.FileName_MetaData)
                metadata_filename = CResult.result_info(result, self.Name_FileName, None)
                if metadata_filename is not None:
                    file_metadata_name_with_path = metadata_filename

                if not CFile.file_or_path_exist(file_metadata_name_with_path):
                    parser.metadata.set_metadata(
                        self.DB_False,
                        '元数据文件[{0}]创建失败, 原因不明! '.format(file_metadata_name_with_path),
                        self.MetaDataFormat_Text,
                        '')
                    return CResult.merge_result(self.Exception,
                                                '元数据文件[{0}]创建失败, 原因不明! '.format(file_metadata_name_with_path))

                try:
                    parser.metadata.set_metadata_file(self.DB_True,
                                                      '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path),
                                                      metadata_format, file_metadata_name_with_path)
                    return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path))
                except Exception as error:
                    parser.metadata.set_metadata(
                        self.DB_False,
                        '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(file_metadata_name_with_path, error.__str__()),
                        self.MetaDataFormat_Text,
                        '')
                    return CResult.merge_result(self.Exception,
                                                '元数据文件[{0}]格式不合法, 无法处理! '.format(file_metadata_name_with_path))
            else:
                return result
        else:
            return CResult.merge_result(self.Success, '元数据引擎未设置, 将在子类中自行实现! ')

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml或json格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        return CResult.merge_result(self.Success, '元数据引擎未设置, 将在子类中自行实现! ')

    def parser_metadata_after_qa(self, parser: CMetaDataParser):
        """
        在质检完成之后, 对时间, 空间和可视化元数据信息进行解析
        :param parser:
        :return:
        """
        # 根据质检结果, 处理详细的时间信息
        try:
            self.parser_metadata_time_after_qa(parser)
        except Exception as error:
            parser.metadata.set_metadata_time(
                self.Exception,
                '数据[{0}]时间元数据解析出现异常, 详细错误信息为: [{1}]'.format(
                    self.file_info.__file_name_with_full_path__,
                    error.__str__()
                )
            )
        finally:
            parser.save_metadata_time()

        # 根据质检结果, 处理详细的空间信息
        try:
            self.parser_metadata_spatial_after_qa(parser)
        except Exception as error:
            parser.metadata.set_metadata_spatial(
                self.Exception,
                '数据[{0}]空间元数据解析出现异常, 详细错误信息为: [{1}]'.format(
                    self.file_info.__file_name_with_full_path__,
                    error.__str__()
                )
            )
        finally:
            parser.save_metadata_spatial()

        # 根据质检结果, 处理详细的可视化信息
        try:
            self.parser_metadata_view_after_qa(parser)
        except Exception as error:
            parser.metadata.set_metadata_view(
                self.Exception,
                '数据[{0}]空间元数据解析出现异常, 详细错误信息为: [{1}]'.format(
                    self.file_info.__file_name_with_full_path__,
                    error.__str__()
                )
            )
        finally:
            parser.save_metadata_view()

        return CResult.merge_result(
            self.Success,
            '数据[{0}]的时间, 空间, 和可视元数据解析完毕! '.format(
                self.file_info.__file_name_with_full_path__,
            )
        )

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 文件的质检列表
        质检项目应包括并不限于如下内容:
        1. 实体数据的附属文件是否完整, 实体数据是否可以正常打开和读取
        1. 元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        1. 业务元数据是否存在并完整, 格式是否正确, 是否可以正常打开和读取
        示例:
        return [
            {self.Name_FileName: '{0}-PAN1.tiff'.format(self.classified_object_name()), self.Name_ID: 'pan_tif',
             self.Name_Title: '全色文件', self.Name_Type: self.QualityAudit_Type_Error}
            , {self.Name_FileName: '{0}-MSS1.tiff'.format(self.classified_object_name()), self.Name_ID: 'mss_tif',
               self.Name_Title: '多光谱文件', self.Name_Type: self.QualityAudit_Type_Error}
        ]
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_bus_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式业务元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return []

    def parser_metadata_time_after_qa(self, parser) -> str:
        """
        继承本方法, 对详细的时间元数据信息进行处理
        todo(全体) 继承本方法, 对详细的时间元数据信息进行处理, 一般包括具体的time, start_time, end_time进行设置, 示例:
            parser.metadata.set_metadata_time(self.Success, '', self.Name_Time, CTime.now())
            parser.metadata.set_metadata_time(self.Success, '', self.Name_Start_Time, CTime.now())
            parser.metadata.set_metadata_time(self.Success, '', self.Name_End_Time, CTime.now())
        :param parser:
        :return:
        """
        pass

    def parser_metadata_spatial_after_qa(self, parser):
        """
        继承本方法, 对详细的空间元数据信息进行处理
        todo(全体) 继承本方法, 对详细的空间元数据信息进行处理, 一般包括原生的中心点, 外包框, 外边框, 以及Wgs84的中心点, 外包框, 外边框, 示例:
            parser.metadata.set_metadata_spatial(self.Success, '', self.Spatial_MetaData_Type_Native_Center, 'Point(0 0)')
        :param parser:
        :return:
        """
        default_engine = CUtils.dict_value_by_name(
            self.get_information(),
            self.Plugins_Info_SpatialEngine,
            None)
        if default_engine is not None:
            result = parser.process_default_spatial(default_engine)
            if CResult.result_success(result):
                try:
                    parser.metadata.set_metadata_spatial(
                        self.DB_True,
                        '元数据文件[{0}]成功加载! '.format(self.file_info.__file_name_with_full_path__),
                        self.Name_Native_Center,
                        None
                    )
                    return CResult.merge_result(self.Success, '元数据文件[{0}]成功加载! '.format(self.file_info.__file_name_with_full_path__))
                except Exception as error:
                    parser.metadata.set_metadata(
                        self.DB_False,
                        '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(self.file_info.__file_name_with_full_path__, error.__str__()),
                        self.MetaDataFormat_Text,
                        '')
                    return CResult.merge_result(self.Exception,
                                                '元数据文件[{0}]格式不合法, 无法处理! '.format(self.file_info.__file_name_with_full_path__))
            else:
                return result
        else:
            return CResult.merge_result(self.Success, '元数据引擎未设置, 将在子类中自行实现! ')

    def parser_metadata_view_after_qa(self, parser):
        """
        继承本方法, 对详细的可视元数据信息进行处理
        todo(全体) 继承本方法, 对详细的可视元数据信息进行处理, 一般包括拇指图, 快视图等等, 示例:
            parser.metadata.set_metadata_view(self.Success, '', self.View_MetaData_Type_Thumb, '/aa/bb.png')
        :param parser:
        :return:
        """
        default_engine = CUtils.dict_value_by_name(
            self.get_information(),
            self.Plugins_Info_ViewEngine,
            None)
        if default_engine is not None:
            result = parser.process_default_view(default_engine)
            if CResult.result_success(result):
                metadata_view_browse = CResult.result_info(result, self.Name_Browse, None)
                metadata_view_thumb = CResult.result_info(result, self.Name_Thumb, None)

                try:
                    parser.metadata.set_metadata_view(
                        self.DB_True,
                        '文件[{0}]的预览图成功加载! '.format(self.file_info.__file_name_with_full_path__),
                        self.Name_Browse,
                        metadata_view_browse
                    )
                    parser.metadata.set_metadata_view(
                        self.DB_True,
                        '文件[{0}]的拇指图成功加载! '.format(self.file_info.__file_name_with_full_path__),
                        self.Name_Thumb,
                        metadata_view_thumb
                    )
                    return CResult.merge_result(
                        self.Success,
                        '文件[{0}]的可视元数据成功加载! '.format(self.file_info.__file_name_with_full_path__)
                    )
                except Exception as error:
                    parser.metadata.set_metadata(
                        self.DB_False,
                        '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(self.file_info.__file_name_with_full_path__,
                                                                   error.__str__()),
                        self.MetaDataFormat_Text,
                        '')
                    return CResult.merge_result(
                        self.Exception,
                        '元数据文件[{0}]格式不合法, 无法处理! '.format(self.file_info.__file_name_with_full_path__))
            else:
                return result
        else:
            return CResult.merge_result(self.Success, '可视元数据引擎未设置, 将在子类中自行实现! ')

    def parser_metadata_with_qa(self, parser: CMetaDataParser) -> str:
        """
        进行质量检验, 保证数据实体的可读性, 并处理好元数据和业务元数据, 保证后续的其他元数据解析的通畅和无误!!!
        :param parser:
        :return:
        """
        parser.batch_qa_file(self.init_qa_file_list(parser))

        # 这里将结果信息丢弃不用, 因为在提取元数据的方法中, 已经将异常信息记录到质检数据中
        result = self.init_metadata(parser)
        if CResult.result_success(result):
            if parser.metadata.metadata_type == self.MetaDataFormat_XML:
                parser.batch_qa_metadata_xml(self.init_qa_metadata_xml_list(parser))
            elif parser.metadata.metadata_type == self.MetaDataFormat_Json:
                parser.batch_qa_metadata_json_item(self.init_qa_metadata_json_list(parser))
        else:
            parser.metadata.set_metadata(
                self.DB_False, CResult.result_message(result), self.MetaDataFormat_Text, '')

        # 这里将结果信息丢弃不用, 因为在提取业务元数据的方法中, 已经将异常信息记录到质检数据中
        result = self.init_metadata_bus(parser)
        if CResult.result_success(result):
            if parser.metadata.metadata_type == self.MetaDataFormat_XML:
                parser.batch_qa_metadata_bus_xml_item(self.init_qa_metadata_bus_xml_list(parser))
            elif parser.metadata.metadata_type == self.MetaDataFormat_Json:
                parser.batch_qa_metadata_bus_json_item(self.init_qa_metadata_bus_json_list(parser))
        else:
            parser.metadata.set_metadata_bus(
                self.DB_False, CResult.result_message(result), self.MetaDataFormat_Text, '')

        return parser.save_metadata_data_and_bus()
