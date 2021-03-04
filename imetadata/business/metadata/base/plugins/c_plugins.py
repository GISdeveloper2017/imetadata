# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 16:24 
# @Author : 王西亚 
# @File : c_plugins.py

from abc import abstractmethod

import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.base.c_exceptions import FileContentWapperNotExistException
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser
from imetadata.business.metadata.base.parser.c_parserCustom import CParserCustom
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.database.c_factory import CFactory


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
    # 插件分组名称(英文)-内置
    Plugins_Info_Group = 'dsodgroup'
    # 插件分组名称(中文)-内置
    Plugins_Info_Group_Title = 'dsodgrouptitle'

    # 插件所属项目标识
    Plugins_Info_Project_ID = 'dsodprojectid'

    # 插件中文描述-内置
    Plugins_Info_Title = 'dsodtitle'
    # 插件大类-英文-内置
    Plugins_Info_Type = 'dsodtype'
    # 插件大类-中文-内置
    Plugins_Info_Type_Title = 'dsodtypetitle'
    # 插件英文编码-业务
    Plugins_Info_Type_Code = 'dsodtypecode'
    # 插件Catalog代码-业务
    Plugins_Info_Catalog = 'dsodcatalog'
    # 插件Catalog标题-业务
    Plugins_Info_Catalog_Title = 'dsodcatalogtitle'
    # 插件-对象是否允许包含子对象
    Plugins_Info_HasChildObj = 'dsod_has_child_obj'
    # 插件-对象是否允许包含子对象
    Plugins_Info_Is_Spatial = 'dsod_is_spatial'
    # 插件-对象是否允许包含子对象
    Plugins_Info_Is_Dataset = 'dsod_is_dataset'
    # 插件-是否需要质检空间信息
    Plugins_Info_Spatial_Qa = 'dsod_spatial_qa'
    # 插件-是否需要质检时间信息
    Plugins_Info_Time_Qa = 'dsod_time_qa'
    # 插件-是否需要质检可视信息
    Plugins_Info_Visual_Qa = 'dsod_visual_qa'

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

    _file_content: CVirtualContent = None
    __file_info: CDMFilePathInfoEx = None
    __metadata_rule_obj: CXml = None

    _object_confirm: int
    _object_detail_file_full_name_list: list

    metadata_bus_transformer_type = None
    metadata_bus_src_filename_with_path = None

    def __init__(self, file_info: CDMFilePathInfoEx):
        """
        :param file_info:  目标文件或路径的名称
        """
        self.__metadata_rule_obj = CXml()
        self.__file_info = file_info
        self._object_name = None
        self._object_detail_file_full_name_list = []

        # 在质检中或者在识别过程中, 需要明确元数据的类型, 和文件名!!!否则将被视为无业务数据集
        self.metadata_bus_transformer_type = None
        self.metadata_bus_src_filename_with_path = None
        if self.file_info is not None:
            self.__metadata_rule_obj.load_xml(self.file_info.rule_content)

    @property
    def file_content(self):
        return self._file_content

    @property
    def file_info(self):
        return self.__file_info

    def classified_object_confirm(self):
        return self._object_confirm

    def classified_object_name(self):
        return self._object_name

    def get_metadata_rule_type(self):
        default_rule_type = CXml.get_element_text(self.__metadata_rule_obj.xpath_one(self.Path_MD_Rule_Type))
        if CUtils.equal_ignore_case(default_rule_type, ''):
            default_rule_type = self.MetaData_Rule_Type_None
        return default_rule_type

    def get_information(self) -> dict:
        information = dict()
        information[self.Plugins_Info_ID] = self.get_id()
        information[self.Plugins_Info_Title] = information[self.Plugins_Info_ID]
        information[self.Plugins_Info_ViewEngine] = None
        information[self.Plugins_Info_SpatialEngine] = None
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_HasChildObj] = self.DB_False
        information[self.Plugins_Info_Group] = None
        information[self.Plugins_Info_Group_Title] = None
        information[self.Plugins_Info_TagsEngine] = None
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_Module_Distribute_Engine] = None  # 同步的引擎，值是发布同步用的类的名字
        information[self.Plugins_Info_Project_ID] = None
        information[self.Plugins_Info_Is_Spatial] = self.DB_False
        information[self.Plugins_Info_Is_Dataset] = self.DB_False
        information[self.Plugins_Info_Spatial_Qa] = self.DB_False
        information[self.Plugins_Info_Time_Qa] = self.DB_False
        information[self.Plugins_Info_Visual_Qa] = self.DB_False
        return information

    def get_id(self) -> str:
        return type(self).__name__

    @abstractmethod
    def classified(self):
        """
        对目标目录或文件进行分类
        . 注意: 可以在识别中, 直接将个别特殊的附属文件加入到_object_detail_file_full_name_list列表中, 后续在附属文件入库功能中, 将自动
            将该列表中的文件, 登记到对象附属文件中
            . 注意: _object_detail_file_full_name_list中存储的附属文件名称, 为包含完整路径的文件名, 注意!!!

        todo(注意) 对象识别过程中, 可以处理特殊的对象附属文件. 它与标准的对象附属文件处理逻辑不冲突, 最后结果为两者的并集!!!

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

        return CResult.merge_result(self.Success, '标签处理完毕!')

    # @property  # 本属性存在问题，谨慎使用
    def object_detail_file_full_name_list(self) -> list:
        return self._object_detail_file_full_name_list

    def parser_detail(self, parser: CParser) -> str:
        """
        对目标目录或文件的详情进行解析
        :return:
        """
        if not isinstance(parser, CParserCustom):
            return parser.process()

        return CResult.merge_result(self.Success, '附属文件处理完毕!')

    def create_file_content(self):
        pass

    def create_virtual_content(self) -> bool:
        if self._file_content is None:
            self.create_file_content()

        if self._file_content is None:
            raise FileContentWapperNotExistException()

        if not self._file_content.virtual_content_valid():
            return self._file_content.create_virtual_content()
        else:
            return True

    def destroy_virtual_content(self):
        if self._file_content is None:
            self.create_file_content()

        if self._file_content is None:
            raise FileContentWapperNotExistException()

        if self._file_content.virtual_content_valid():
            self._file_content.destroy_virtual_content()

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
        try:
            result = parser.process()

            # 首先要判断和验证与数据质量相关的核心内容
            if CResult.result_success(result):
                self.parser_metadata_with_qa(parser)
                result = parser.save_metadata_data_and_bus()
            else:
                return result

            # 其次, 根据合法的数据\元数据\业务元数据内容, 提取其他元数据内容, 如果其中出现异常, 则写入质检结果中
            if CResult.result_success(result):
                result = self.parser_metadata_after_qa(parser)
            else:
                return result

            # 上述内容都处理完毕后, 再执行自定义的元数据解析
            if CResult.result_success(result):
                result = self.parser_metadata_custom(parser)
            else:
                return result

            # 自定义的元数据质检
            if CResult.result_success(result):
                self.qa_custom(parser)
                result = parser.save_quality()
            else:
                return result

            if CResult.result_success(result):
                return CResult.merge_result(
                    self.Success,
                    '数据[{0}]的全部元数据解析完毕! '.format(
                        self.file_info.file_name_with_full_path
                    )
                )
            else:
                return result

        except Exception as error:
            return CResult.merge_result(
                self.Failure,
                '数据[{0}]的元数据解析过程出现错误! 详细信息为: [{1}]'.format(
                    self.file_info.file_name_with_full_path,
                    error.__str__()
                )
            )

    def qa_custom(self, parser: CMetaDataParser):
        """
        自定义的质检方法, 发生在元数据解析之后
        :param parser:
        :return:
        """
        # 空间信息质检
        Spatial_Qa = CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Spatial_Qa, '')
        if not CUtils.equal_ignore_case(Spatial_Qa, self.DB_False):
            sql_select_spatial = """
            select dso_prj_proj4,dso_prj_coordinate from dm2_storage_object
                where dsoid = '{0}'""".format(parser.object_id)
            record_select_spatial = CFactory().give_me_db(self.file_info.db_server_id).one_row(sql_select_spatial)
            dso_prj_proj4 = record_select_spatial.value_by_name(0, 'dso_prj_proj4', '')
            dso_prj_coordinate = record_select_spatial.value_by_name(0, 'dso_prj_coordinate', '')
            if not CUtils.equal_ignore_case(dso_prj_proj4, ''):
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'proj4',
                        self.Name_Title: '坐标投影-proj4',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Pass,
                        self.Name_Message: '{0}的坐标投影-proj4信息提取成功，完成入库'.format(parser.object_name)
                    }
                )
            else:
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'proj4',
                        self.Name_Title: '坐标投影-proj4',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Message: '{0}的坐标投影-proj4信提取失败，未能成功入库，请检查！'.format(parser.object_name)
                    }
                )
            if not CUtils.equal_ignore_case(dso_prj_coordinate, ''):
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'coordinate',
                        self.Name_Title: '坐标投影-坐标系',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Pass,
                        self.Name_Message: '{0}的坐标投影-坐标系信息提取成功，完成入库'.format(parser.object_name)
                    }
                )
            else:
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'coordinate',
                        self.Name_Title: '坐标投影-坐标系',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Message: '{0}的坐标投影-坐标系信息提取失败，未能成功入库，请检查！'.format(parser.object_name)

                    }
                )
        # 可视信息质检
        Visual_Qa = CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Visual_Qa, '')
        if not CUtils.equal_ignore_case(Visual_Qa, self.DB_False):
            sql_select_visual = """
                select dso_browser,dso_thumb from dm2_storage_object
                where dsoid = '{0}'""".format(parser.object_id)
            record_select_visual = CFactory().give_me_db(self.file_info.db_server_id).one_row(sql_select_visual)
            dso_browser = record_select_visual.value_by_name(0, 'dso_browser', '')
            dso_thumb = record_select_visual.value_by_name(0, 'dso_thumb', '')
            if not CUtils.equal_ignore_case(dso_browser, ''):
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'browser',
                        self.Name_Title: '快视图',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Pass,
                        self.Name_Message: '{0}的快视图信息提取成功，完成入库'.format(parser.object_name)
                    }
                )
            else:
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'browser',
                        self.Name_Title: '快视图',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Message: '{0}的快视图信提取失败，未能成功入库，请检查！'.format(parser.object_name)
                    }
                )
            if not CUtils.equal_ignore_case(dso_thumb, ''):
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'thumb',
                        self.Name_Title: '拇指图',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Pass,
                        self.Name_Message: '{0}的拇指图信息提取成功，完成入库'.format(parser.object_name)
                    }
                )
            else:
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'thumb',
                        self.Name_Title: '拇指图',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Message: '{0}的拇指图信息提取失败，未能成功入库，请检查！'.format(parser.object_name)

                    }
                )
        # 时间信息质检
        Time_Qa = CUtils.dict_value_by_name(self.get_information(), self.Plugins_Info_Time_Qa, '')
        if not CUtils.equal_ignore_case(Time_Qa, self.DB_False):
            sql_select_time = """
                select dso_time from dm2_storage_object where dsoid = '{0}'""".format(parser.object_id)
            dso_time = CFactory().give_me_db(self.file_info.db_server_id).one_value(sql_select_time)
            if not CUtils.equal_ignore_case(dso_time, ''):
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'time',
                        self.Name_Title: '时间',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Pass,
                        self.Name_Message: '{0}的时间信息提取成功，完成入库'.format(parser.object_name)
                    }
                )
            else:
                parser.metadata.quality.append_metadata_bus_quality(
                    {
                        self.Name_ID: 'time',
                        self.Name_Title: '时间',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Error,
                        self.Name_Message: '{0}的时间信息提取失败，未能成功入库，请检查！'.format(parser.object_name)

                    }
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
                metadata_format = CResult.result_info(result, self.Name_Format, None)
                if metadata_format is None:
                    parser.metadata.set_metadata(
                        self.DB_True,
                        '无实体元数据',
                        self.MetaDataFormat_Text,
                        None
                    )
                    return CResult.merge_result(self.Success, '该类型数据无实体元数据! ')

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
                    return CResult.merge_result(
                        self.Exception,
                        '元数据文件[{0}]创建失败, 原因不明! '.format(file_metadata_name_with_path)
                    )

                try:
                    parser.metadata.set_metadata_file(
                        self.DB_True,
                        '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path),
                        metadata_format,
                        file_metadata_name_with_path
                    )
                    return CResult.merge_result(
                        self.Success,
                        '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path)
                    )
                except Exception as error:
                    parser.metadata.set_metadata(
                        self.DB_False,
                        '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(file_metadata_name_with_path, error.__str__()),
                        self.MetaDataFormat_Text,
                        ''
                    )
                    return CResult.merge_result(self.Exception,
                                                '元数据文件[{0}]格式不合法, 无法处理! '.format(file_metadata_name_with_path))
            else:
                return result
        else:
            parser.metadata.set_metadata(self.Not_Support, '不支持解析实体元数据! ', self.MetaDataFormat_Text, None)
            return CResult.merge_result(self.Success, '不支持解析实体元数据! ')

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml或json格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        parser.metadata.set_metadata_bus(self.Not_Support, '不支持解析业务元数据! ', self.MetaDataFormat_Text, None)
        return CResult.merge_result(self.Success, '不支持解析业务元数据! ')

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
                    self.file_info.file_name_with_full_path,
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
                    self.file_info.file_name_with_full_path,
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
                    self.file_info.file_name_with_full_path,
                    error.__str__()
                )
            )
        finally:
            parser.save_metadata_view()

        return CResult.merge_result(
            self.Success,
            '数据[{0}]的时间, 空间, 和可视元数据解析完毕! '.format(
                self.file_info.file_name_with_full_path,
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

    def default_qa_metadata_json_list_raster(self, object_name: str) -> list:
        """
        默认的影像实体元数据质检
        :param object_name:
        :return:
        """
        return []

    def default_qa_metadata_json_list_vector(self, object_name: str) -> list:
        """
        默认的矢量实体元数据质检
        :param object_name:
        :return:
        """
        return []

    def parser_metadata_time_after_qa(self, parser: CMetaDataParser) -> str:
        """
        继承本方法, 对详细的时间元数据信息进行处理
        todo(全体) 继承本方法, 对详细的时间元数据信息进行处理, 一般包括具体的time, start_time, end_time进行设置, 示例:
            parser.metadata.set_metadata_time(self.Success, '', self.Name_Time, CTime.now())
            parser.metadata.set_metadata_time(self.Success, '', self.Name_Start_Time, CTime.now())
            parser.metadata.set_metadata_time(self.Success, '', self.Name_End_Time, CTime.now())
        :param parser:
        :return:
        """
        metadata_time_parser_list = self.parser_metadata_time_list(parser)
        if len(metadata_time_parser_list) > 0:
            for metadata_time_item in metadata_time_parser_list:
                src = CUtils.dict_value_by_name(metadata_time_item, self.Name_Source, self.Name_Business)
                src_format = CUtils.dict_value_by_name(metadata_time_item, self.Name_Format, self.MetaDataFormat_XML)
                if CUtils.equal_ignore_case(src, self.Name_Data):
                    if CUtils.equal_ignore_case(src_format, self.MetaDataFormat_XML):
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                            CUtils.dict_value_by_name(metadata_time_item, self.Name_ID, self.Name_Time),
                            CXml.get_element_text(
                                parser.metadata.metadata_xml().xpath_one(
                                    CUtils.dict_value_by_name(metadata_time_item, self.Name_XPath, '')
                                )
                            )
                        )
                    else:
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                            CUtils.dict_value_by_name(metadata_time_item, self.Name_ID, self.Name_Time),
                            parser.metadata.metadata_json().xpath_one(
                                CUtils.dict_value_by_name(metadata_time_item, self.Name_XPath, ''),
                                None
                            )
                        )
                else:
                    if CUtils.equal_ignore_case(src_format, self.MetaDataFormat_XML):
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                            CUtils.dict_value_by_name(metadata_time_item, self.Name_ID, self.Name_Time),
                            self.get_parser_time_when_metadata_bus_xml(parser, metadata_time_item)
                        )
                    else:
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                            CUtils.dict_value_by_name(metadata_time_item, self.Name_ID, self.Name_Time),
                            parser.metadata.metadata_bus_json().xpath_one(
                                CUtils.dict_value_by_name(metadata_time_item, self.Name_XPath, ''),
                                None
                            )
                        )

            # 从metadata中重新提取时间time_information, 获取time的值, 然后对time, start_time和end_time进行修正
            time_json = parser.metadata.time_information
            time_text = time_json.xpath_one(self.Name_Time, '')
            start_time_text = time_json.xpath_one(self.Name_Start_Time, '')
            end_time_text = time_json.xpath_one(self.Name_End_Time, '')

            # 当3个时间都为空时候，取文件的修改时间
            if CUtils.equal_ignore_case(time_text, '') \
                    and CUtils.equal_ignore_case(start_time_text, '') \
                    and CUtils.equal_ignore_case(end_time_text, ''):
                return self.get_default_metadata_time(parser)

            # 先存在原始的时间值（time_source，start_time_source和end_time_source）
            parser.metadata.set_metadata_time(
                self.Success,
                '原始时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                self.Name_Time_Native,
                time_text)
            parser.metadata.set_metadata_time(
                self.Success,
                '原始时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                self.Name_Start_Time_Native,
                start_time_text)
            parser.metadata.set_metadata_time(
                self.Success,
                '原始时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                self.Name_End_Time_Native,
                end_time_text)

            # 监测time_text是否是合法的日期，开始结束时间是否为空值
            if (not CUtils.equal_ignore_case(time_text, '')) \
                    and (not CUtils.text_is_datetime(time_text)) \
                    and (not CUtils.text_is_date_day(time_text)) \
                    or (CUtils.equal_ignore_case(start_time_text, '')) \
                    or (CUtils.equal_ignore_case(end_time_text, '')):
                # 从数据库中查询为标准格式（2020，202009，2020Q1），如2020-09，2020/09,2020.09,2020年09月，2020，2020年，2020Q1
                # time_text_temp = time_text.replace('-', '').replace('/', '').replace('\\', '').replace('.', '').replace('年', '').replace('月', '')
                time_text_standard = CUtils.standard_datetime_format(time_text, time_text)
                if not CUtils.equal_ignore_case(time_text_standard, ''):
                    time_text_temp = CUtils.any_2_str(time_text_standard).replace('-', '')
                    # 从配置中读取时间信息查询的SQL语句, 获取对应的开始时间、结束时间
                    sql = settings.application.xpath_one(self.Path_Setting_MetaData_Time_Query, None)
                    db_server_id = settings.application.xpath_one(self.Path_Setting_MetaData_Time_Server,
                                                                  self.file_info.db_server_id)
                    if CUtils.equal_ignore_case(sql, ''):
                        parser.metadata.set_metadata_time(
                            self.Failure,
                            '系统设置中, 缺少时间信息解析的内容, 请修正后重试! '
                        )
                        return CResult.merge_result(
                            self.Failure,
                            '系统设置中, 缺少时间信息解析的内容, 请修正后重试! '
                        )

                    ds_time = CFactory().give_me_db(db_server_id).one_row(sql, {self.Name_Value: time_text_temp})
                    starttime = ds_time.value_by_name(0, 'starttime', None)
                    endtime = ds_time.value_by_name(0, 'endtime', None)
                    if starttime is not None:
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功从ro_global_dim_time表中解析',
                            self.Name_Time,
                            starttime)
                    if CUtils.equal_ignore_case(start_time_text, ''):
                        if starttime is not None:
                            parser.metadata.set_metadata_time(
                                self.Success,
                                '时间信息[{0}]成功从ro_global_dim_time表中解析',
                                self.Name_Start_Time,
                                starttime)
                    if CUtils.equal_ignore_case(end_time_text, ''):
                        if endtime is not None:
                            parser.metadata.set_metadata_time(
                                self.Success,
                                '时间信息[{0}]成功从ro_global_dim_time表中解析',
                                self.Name_End_Time,
                                endtime)

            # 监测start_time_text是否是合法的日期
            if (not CUtils.equal_ignore_case(start_time_text, '')) \
                    and (not CUtils.text_is_datetime(start_time_text)) \
                    and (not CUtils.text_is_date_day(start_time_text)):
                # 从数据库中查询为标准格式（2020，202009，2020Q1），如2020-09，2020/09,2020.09,2020年09月，2020，2020年，2020Q1
                # time_text_temp = time_text.replace('-', '').replace('/', '').replace('\\', '').replace('.', '').replace('年', '').replace('月', '')
                time_text_standard = CUtils.standard_datetime_format(start_time_text, start_time_text)
                if not CUtils.equal_ignore_case(time_text_standard, ''):
                    time_text_temp = CUtils.any_2_str(time_text_standard).replace('-', '')
                    # 从配置中读取时间信息查询的SQL语句, 获取对应的开始时间、结束时间
                    sql = settings.application.xpath_one(self.Path_Setting_MetaData_Time_Query, None)
                    db_server_id = settings.application.xpath_one(self.Path_Setting_MetaData_Time_Server,
                                                                  self.file_info.db_server_id)
                    if CUtils.equal_ignore_case(sql, ''):
                        parser.metadata.set_metadata_time(
                            self.Failure,
                            '系统设置中, 缺少时间信息解析的内容, 请修正后重试! '
                        )
                        return CResult.merge_result(
                            self.Failure,
                            '系统设置中, 缺少时间信息解析的内容, 请修正后重试! '
                        )

                    ds_time = CFactory().give_me_db(db_server_id).one_row(sql, {self.Name_Value: time_text_temp})
                    starttime = ds_time.value_by_name(0, 'starttime', None)
                    # endtime = ds_time.value_by_name(0, 'endtime', None)
                    if starttime is not None:
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功从ro_global_dim_time表中解析',
                            self.Name_Start_Time,
                            starttime)

            # 监测end_time_text是否是合法的日期
            if (not CUtils.equal_ignore_case(end_time_text, '')) \
                    and (not CUtils.text_is_datetime(end_time_text)) \
                    and (not CUtils.text_is_date_day(end_time_text)):
                # 从数据库中查询为标准格式（2020，202009，2020Q1），如2020-09，2020/09,2020.09,2020年09月，2020，2020年，2020Q1
                # time_text_temp = time_text.replace('-', '').replace('/', '').replace('\\', '').replace('.', '').replace('年', '').replace('月', '')
                time_text_standard = CUtils.standard_datetime_format(end_time_text, end_time_text)
                if not CUtils.equal_ignore_case(time_text_standard, ''):
                    time_text_temp = CUtils.any_2_str(time_text_standard).replace('-', '')
                    # 从配置中读取时间信息查询的SQL语句, 获取对应的开始时间、结束时间
                    sql = settings.application.xpath_one(self.Path_Setting_MetaData_Time_Query, None)
                    db_server_id = settings.application.xpath_one(self.Path_Setting_MetaData_Time_Server,
                                                                  self.file_info.db_server_id)
                    if CUtils.equal_ignore_case(sql, ''):
                        parser.metadata.set_metadata_time(
                            self.Failure,
                            '系统设置中, 缺少时间信息解析的内容, 请修正后重试! '
                        )
                        return CResult.merge_result(
                            self.Failure,
                            '系统设置中, 缺少时间信息解析的内容, 请修正后重试! '
                        )

                    ds_time = CFactory().give_me_db(db_server_id).one_row(sql, {self.Name_Value: time_text_temp})
                    starttime = ds_time.value_by_name(0, 'starttime', None)
                    # endtime = ds_time.value_by_name(0, 'endtime', None)
                    if starttime is not None:
                        parser.metadata.set_metadata_time(
                            self.Success,
                            '时间信息[{0}]成功从ro_global_dim_time表中解析',
                            self.Name_End_Time,
                            starttime)

            # 将time, start_time和end_time进行格式化到日的修正处理（如2020变为20200101，202009变为20200901，其他的不变）
            # 再次从json中获取（可能从ro_global_dim_time取值过了）
            time_json = parser.metadata.time_information
            time_text = time_json.xpath_one(self.Name_Time, '')
            start_time_text = time_json.xpath_one(self.Name_Start_Time, '')
            end_time_text = time_json.xpath_one(self.Name_End_Time, '')
            # 格式化处理
            time_text_day = CUtils.to_day_format(time_text, time_text)
            start_time_text_day = CUtils.to_day_format(start_time_text, start_time_text)
            end_time_text_day = CUtils.to_day_format(end_time_text, end_time_text)
            # 会写到时间json对象中
            parser.metadata.set_metadata_time(
                self.Success,
                '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                self.Name_Time,
                time_text_day)
            parser.metadata.set_metadata_time(
                self.Success,
                '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                self.Name_Start_Time,
                start_time_text_day)
            parser.metadata.set_metadata_time(
                self.Success,
                '时间信息[{0}]成功解析! '.format(self.file_info.file_name_with_full_path),
                self.Name_End_Time,
                end_time_text_day)
            return CResult.merge_result(
                self.Success,
                '数据文件[{0}]的时间信息解析成功! '.format(self.file_info.file_name_with_full_path)
            )
        else:
            return self.get_default_metadata_time(parser)

    def get_default_metadata_time(self, parser: CMetaDataParser) -> str:
        parser.metadata.set_metadata_time(self.Success, '', self.Name_Time, self.file_info.file_create_time)
        parser.metadata.set_metadata_time(self.Success, '', self.Name_Start_Time, self.file_info.file_create_time)
        parser.metadata.set_metadata_time(self.Success, '', self.Name_End_Time, self.file_info.file_create_time)

        return CResult.merge_result(
            self.Success,
            '数据文件[{0}]的时间信息解析成功! '.format(self.file_info.file_name_with_full_path)
        )

    def get_parser_time_when_metadata_bus_xml(self, parser: CMetaDataParser, metadata_time_item):
        """
        因卫星部分插件存在多xml的情况，故而扩展出接口对卫星插件的情况做特殊处理
        """
        return CXml.get_element_text(
            parser.metadata.metadata_bus_xml().xpath_one(
                CUtils.dict_value_by_name(metadata_time_item, self.Name_XPath, '')
            )
        )

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        示例:
        return [
            {
                self.Name_ID: self.Name_Time,
                self.Name_XPath: '/ProductMetaData/CenterTime'
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: '/ProductMetaData/StartTime'
            },
            {
                self.Name_Source: self.Name_Data,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: '/ProductMetaData/EndTime'
            }
        ]
        self.Name_Source
        1. self.Name_Business: 表示从数据的业务xml元数据中取(默认, 可以不设置)
        1. self.Name_Data: 表示从数据的xml元数据中取
        :param parser:
        :return:
        """
        return []

    def parser_metadata_spatial_after_qa(self, parser: CMetaDataParser):
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
                    dict_spatial_metadata_type = {
                        self.Name_Native_Center: self.Spatial_MetaData_Type_Native_Center,
                        self.Name_Native_BBox: self.Spatial_MetaData_Type_Native_BBox,
                        self.Name_Native_Geom: self.Spatial_MetaData_Type_Native_Geom,
                        self.Name_Wgs84_Center: self.Spatial_MetaData_Type_Wgs84_Center,
                        self.Name_Wgs84_BBox: self.Spatial_MetaData_Type_Wgs84_BBox,
                        self.Name_Wgs84_Geom: self.Spatial_MetaData_Type_Wgs84_Geom,
                        self.Name_Prj_Wkt: self.Spatial_MetaData_Type_Prj_Wkt,
                        self.Name_Prj_Proj4: self.Spatial_MetaData_Type_Prj_Proj4,
                        self.Name_Prj_Project: self.Spatial_MetaData_Type_Prj_Project,
                        self.Name_Prj_Coordinate: self.Spatial_MetaData_Type_Prj_Coordinate,
                        self.Name_Prj_Degree: self.Spatial_MetaData_Type_Prj_Degree,
                        self.Name_Prj_Zone: self.Spatial_MetaData_Type_Prj_Zone,
                        self.Name_Prj_Source: self.Spatial_MetaData_Type_Prj_Source
                    }
                    for type_name, type_value in dict_spatial_metadata_type.items():
                        parser.metadata.set_metadata_spatial(
                            self.DB_True,
                            '元数据文件[{0}]成功加载! '.format(self.file_info.file_name_with_full_path),
                            type_value,
                            CResult.result_info(result, type_name, '')
                        )
                    return CResult.merge_result(self.Success,
                                                '元数据文件[{0}]成功加载! '.format(self.file_info.file_name_with_full_path))
                except Exception as error:
                    parser.metadata.set_metadata_spatial(
                        self.DB_False,
                        '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(self.file_info.file_name_with_full_path,
                                                                   error.__str__()),
                        self.MetaDataFormat_Text,
                        '')
                    return CResult.merge_result(self.Exception,
                                                '元数据文件[{0}]格式不合法, 无法处理! '.format(
                                                    self.file_info.file_name_with_full_path))
            else:
                parser.metadata.set_metadata_spatial(
                    self.DB_False,
                    CResult.result_message(result)
                )
                return result
        else:
            parser.metadata.set_metadata_spatial(
                self.Not_Support,
                '不支持解析空间元数据! '
            )
            return CResult.merge_result(self.Success, '不支持解析空间元数据! ')

    def parser_metadata_view_after_qa(self, parser: CMetaDataParser):
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
                        '文件[{0}]的预览图成功加载! '.format(self.file_info.file_name_with_full_path),
                        self.View_MetaData_Type_Browse,
                        metadata_view_browse
                    )
                    parser.metadata.set_metadata_view(
                        self.DB_True,
                        '文件[{0}]的拇指图成功加载! '.format(self.file_info.file_name_with_full_path),
                        self.View_MetaData_Type_Thumb,
                        metadata_view_thumb
                    )
                    return CResult.merge_result(
                        self.Success,
                        '文件[{0}]的可视元数据成功加载! '.format(self.file_info.file_name_with_full_path)
                    )
                except Exception as error:
                    parser.metadata.set_metadata(
                        self.DB_False,
                        '元数据文件[{0}]格式不合法, 无法处理! 详细错误为: {1}'.format(self.file_info.file_name_with_full_path,
                                                                   error.__str__()),
                        self.MetaDataFormat_Text,
                        '')
                    return CResult.merge_result(
                        self.Exception,
                        '元数据文件[{0}]格式不合法, 无法处理! '.format(self.file_info.file_name_with_full_path))
            else:
                parser.metadata.set_metadata_view(
                    self.DB_False,
                    CResult.result_message(result)
                )
                return result
        else:
            parser.metadata.set_metadata_view(
                self.Not_Support,
                '不支持解析快视图元数据! '
            )
            return CResult.merge_result(self.Success, '不支持解析快视图元数据! ')

    def parser_metadata_with_qa(self, parser: CMetaDataParser):
        """
        进行质量检验, 保证数据实体的可读性, 并处理好元数据和业务元数据, 保证后续的其他元数据解析的通畅和无误!!!
        :param parser:
        :return:
        """
        parser.batch_qa_file(self.init_qa_file_list(parser))
        # 自定义的文件完整性质检
        self.qa_file_custom(parser)

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
            if parser.metadata.metadata_bus_type == self.MetaDataFormat_XML:
                parser.batch_qa_metadata_bus_xml_item(self.init_qa_metadata_bus_xml_list(parser))
            elif parser.metadata.metadata_bus_type == self.MetaDataFormat_Json:
                parser.batch_qa_metadata_bus_json_item(self.init_qa_metadata_bus_json_list(parser))
        else:
            parser.metadata.set_metadata_bus(
                self.DB_False, CResult.result_message(result), self.MetaDataFormat_Text, '')

        self.qa_metadata_custom(parser)

    def qa_metadata_custom(self, parser: CMetaDataParser):
        """
        自定义的质检方法, 发生在元数据解析之后
        :param parser:
        :return:
        """
        pass

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        :param parser:
        :return:
        """
        pass

    def init_qa_file_integrity_default_list(self, file_name_with_full_path: str):
        """
        完成 赵宇飞  常用的文件对象校验列表集合（img/tif/bil/tiff/shp）,tiff暂无
        @param file_name_with_full_path: 文件的全文件名（img/tif/tiff/shp）
        @return: 返回常用文件完整性的质检列表，如果是主文件，会有一个格式的项，用于质检文件的打开可读性
        """
        file_ext = CFile.file_ext(file_name_with_full_path)
        if CUtils.equal_ignore_case(file_ext, self.Name_Img):
            return self.init_qa_file_integrity_img_list(file_name_with_full_path)
        elif CUtils.equal_ignore_case(file_ext, self.Name_Tif):
            return self.init_qa_file_integrity_tif_list(file_name_with_full_path)
        elif CUtils.equal_ignore_case(file_ext, self.Name_Tiff):
            return self.init_qa_file_integrity_tiff_list(file_name_with_full_path)
        elif CUtils.equal_ignore_case(file_ext, self.Name_Bil):
            return self.init_qa_file_integrity_bil_list(file_name_with_full_path)
        elif CUtils.equal_ignore_case(file_ext, self.Name_Shp):
            return self.init_qa_file_integrity_shp_list(file_name_with_full_path)
        return []

    def init_qa_file_integrity_img_list(self, file_name_with_full_path: str):
        """
        完成 赵宇飞 对img数据进行完整性质检，并返回检查结果列表
            xxx.img	文件	栅格数据可读	错误
            xxx.ige	文件	img小于1M时必须存在	警告
            xxx.rrd	文件	是否有金字塔，内置和外置金字塔文件	警告
            xxx.rde	文件	rrd大于2G时存在	警告
        @param file_name_with_full_path: img的全文件名
        @return: 返回img的质检列表,如果是主文件img，会有一个格式的项，用于质检文件的打开可读性
        """
        file_main_name = CFile.file_main_name(file_name_with_full_path)
        file_ext = CFile.file_ext(file_name_with_full_path)
        file_path = CFile.file_path(file_name_with_full_path)

        result_list = list()
        if CUtils.equal_ignore_case(file_ext, self.Name_Img):
            result_list.extend([
                {
                    self.Name_FileName: '{0}.img'.format(file_main_name),
                    self.Name_ID: 'img',
                    self.Name_Title: 'IMG影像',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Format: self.DataFormat_Raster_File
                }, {
                    self.Name_FileName: '{0}.rrd'.format(file_main_name),
                    self.Name_ID: 'rrd',
                    self.Name_Title: '金字塔文件',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                }
            ])

            file_size = CFile.file_size(file_name_with_full_path)
            if file_size < 1024 * 1024:
                """img小于1M时必须存在 xxx.ige"""
                result_list.extend([
                    {
                        self.Name_FileName: '{0}.ige'.format(file_main_name),
                        self.Name_ID: 'ige',
                        self.Name_Title: 'ige文件',
                        self.Name_Group: self.QA_Group_Data_Integrity,
                        self.Name_Result: self.QA_Result_Warn
                    }
                ])

            rrd_file_with_path = CFile.join_file(file_path, '{0}.{1}'.format(file_main_name, self.Name_rrd))
            if CFile.file_or_path_exist(rrd_file_with_path):
                rrd_file_size = CFile.file_size(rrd_file_with_path)
                if rrd_file_size > 1024 * 1024 * 1024 * 2:
                    """xxx.rde	文件	rrd大于2G时存在"""
                    result_list.extend([
                        {
                            self.Name_FileName: '{0}.rde'.format(file_main_name),
                            self.Name_ID: 'rde',
                            self.Name_Title: 'rde文件',
                            self.Name_Group: self.QA_Group_Data_Integrity,
                            self.Name_Result: self.QA_Result_Warn
                        }
                    ])
        return result_list

    def init_qa_file_integrity_tif_list(self, file_name_with_full_path: str):
        """
        完成 赵宇飞 对tif数据进行完整性质检，并返回检查结果列表
            可用性	xxx.tif	文件	栅格数据可读	错误
            完整性	xxx.tfw	文件	投影信息文件	警告
        @param file_name_with_full_path: tif的全文件名
        @return: 返回img的质检列表,如果是主文件tif，会有一个格式的项，用于质检文件的打开可读性
        """
        file_main_name = CFile.file_main_name(file_name_with_full_path)
        file_ext = CFile.file_ext(file_name_with_full_path)
        # file_path = CFile.file_path(file_name_with_full_path)

        result_list = list()
        if CUtils.equal_ignore_case(file_ext, self.Name_Tif):
            result_list.extend([
                {
                    self.Name_FileName: '{0}.tif'.format(file_main_name),
                    self.Name_ID: 'tif',
                    self.Name_Title: 'TIF影像',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Format: self.DataFormat_Raster_File
                }, {
                    self.Name_FileName: '{0}.tfw'.format(file_main_name),
                    self.Name_ID: 'tfw',
                    self.Name_Title: 'TFW投影文件',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                }
            ])
        return result_list

    def init_qa_file_integrity_tiff_list(self, file_name_with_full_path: str):
        """
        完成 赵宇飞 对tiff数据进行完整性质检，并返回检查结果列表
            可用性	xxx.tiff	文件	栅格数据可读	错误
        @param file_name_with_full_path: tif的全文件名
        @return: 返回tiff的质检列表,如果是主文件tiff，会有一个格式的项，用于质检文件的打开可读性
        """
        file_main_name = CFile.file_main_name(file_name_with_full_path)
        file_ext = CFile.file_ext(file_name_with_full_path)
        # file_path = CFile.file_path(file_name_with_full_path)

        result_list = list()
        if CUtils.equal_ignore_case(file_ext, self.Name_Tiff):
            result_list.extend([
                {
                    self.Name_FileName: '{0}.tiff'.format(file_main_name),
                    self.Name_ID: 'tiff',
                    self.Name_Title: 'TIFF影像',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Format: self.DataFormat_Raster_File
                }
            ])
        return result_list

    def init_qa_file_integrity_bil_list(self, file_name_with_full_path: str):
        """
        完成 赵宇飞 对bil数据进行完整性质检，并返回检查结果列表
            可用性	xxx.bil	文件	栅格数据可读	错误
            完整性	xxx.blw	文件	投影信息文件	警告
        @param file_name_with_full_path: bil的全文件名
        @return: 返回img的质检列表,如果是主文件bil，会有一个格式的项，用于质检文件的打开可读性
        """
        file_main_name = CFile.file_main_name(file_name_with_full_path)
        file_ext = CFile.file_ext(file_name_with_full_path)
        # file_path = CFile.file_path(file_name_with_full_path)

        result_list = list()
        if CUtils.equal_ignore_case(file_ext, self.Name_Bil):
            result_list.extend([
                {
                    self.Name_FileName: '{0}.bil'.format(file_main_name),
                    self.Name_ID: 'bil',
                    self.Name_Title: 'bil影像',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Format: self.DataFormat_Raster_File
                }, {
                    self.Name_FileName: '{0}.blw'.format(file_main_name),
                    self.Name_ID: 'blw',
                    self.Name_Title: 'blw投影文件',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                }
            ])
        return result_list

    def init_qa_file_integrity_shp_list(self, file_name_with_full_path: str):
        """
        完成 赵宇飞 对shp数据进行完整性质检，并返回检查结果列表
        @param file_name_with_full_path: img的全文件名
        @return: 返回img的质检列表,如果是主文件shp，会有一个格式的项，用于质检文件的打开可读性
        """
        file_main_name = CFile.file_main_name(file_name_with_full_path)
        return [
            {
                self.Name_FileName: '{0}.shp'.format(file_main_name),
                self.Name_ID: 'shp',
                self.Name_Title: 'shp文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Format: self.DataFormat_Vector_File,
                self.Name_Result: self.QA_Result_Error
            }, {
                self.Name_FileName: '{0}.dbf'.format(file_main_name),
                self.Name_ID: 'dbf',
                self.Name_Title: '属性数据文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }, {
                self.Name_FileName: '{0}.prj'.format(file_main_name),
                self.Name_ID: 'prj',
                self.Name_Title: '投影文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            }, {
                self.Name_FileName: '{0}.shx'.format(file_main_name),
                self.Name_ID: 'shx',
                self.Name_Title: '索引文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def parser_metadata_custom(self, parser: CMetaDataParser) -> str:
        """
        自定义的元数据解析, 在所有质检和其他处理之后触发
        :param parser:
        :return:
        """
        return CResult.merge_result(
            self.Success,
            '数据[{0}]的自定义元数据解析完毕! '.format(
                self.file_info.file_name_with_full_path
            )
        )

    def get_metadata_bus_configuration_list(self) -> list:
        return list()

    def metadata_bus_xml_to_dict(
            self, metadata_bus_xml: CXml, multiple_metadata_bus_filename_dict=None, space_flag=False
    ):
        return CResult.merge_result(self.Success, '数据的业务元数据的详细内容无需解析!'), dict()

    def get_multiple_metadata_bus_filename_with_path(self, file_path):
        """
        获取复数的业务元数据字典
        :return:
        """
        return dict()
