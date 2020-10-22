# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:00
# @Author : 赵宇飞
# @File : plugins_1020_ortho.py
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.base.c_result import CResult
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.base.c_xml import CXml


class plugins_1020_ortho(CFilePlugins_GUOTU):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '单景正射'
        information[self.Plugins_Info_Name] = 'ortho'

        return information

    def classified(self):
        """
        设计国土行业数据ortho的验证规则（单景正射）
        todo 负责人 王学谦 在这里检验ortho的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__  # 初始化需要的参数

        file_main_name_with_path = CFile.join_file(self.file_info.__file_path__, file_main_name)
        check_file_main_name_exist = \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Tif)) or \
            CFile.file_or_path_exist('{0}.{1}'.format(file_main_name_with_path, self.Name_Img))

        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self.__object_name__

        # 检查后缀名
        if CUtils.equal_ignore_case(file_ext, self.Name_Tif) or CUtils.equal_ignore_case(file_ext, self.Name_Img):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化ortho文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        todo 负责人 王学谦 在这里检验初始化ortho的质检列表
        """
        file_main_name = self.classified_object_name()
        file_ext = self.file_info.__file_ext__
        file_main_name_with_path = '{0}.{1}'.format(
            CFile.join_file(self.file_info.__file_path__, file_main_name), file_ext)  # 获取初始化需要的参数

        list_qa = list()
        list_qa.extend(self.init_qa_file_integrity_default_list(file_main_name_with_path))  # 调用默认的规则列表
        list_qa.extend([
            {
                self.Name_FileName: '{0}_21at.xml'.format(file_main_name),
                self.Name_ID: '_21at.xml',
                self.Name_Title: '业务元数据文件',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn,
                self.Name_Format: self.MetaDataFormat_XML
            }
        ])  # xml的配置

        return list_qa

    def init_qa_metadata_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return [
            {
                self.Name_XPath: 'pixelsize.width',
                self.Name_ID: 'pixelsize.width',
                self.Name_Title: '影像宽度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer_positive
            }
        ]

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml或json格式的业务元数据, 加载到parser的metadata对象中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

        file_main_name = self.file_info.__file_main_name__
        file_metadata_name_with_path = '{0}_21at.xml'.format(
            CFile.join_file(self.file_info.__file_path__, file_main_name)
        )  # 获取初始化需要的参数
        try:
            xml_str = CXml.file_2_str(file_metadata_name_with_path)
            if not CUtils.equal_ignore_case(xml_str, ''):
                parser.metadata.set_metadata_bus(
                    self.Success,
                    '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path),
                    self.MetaDataFormat_XML,
                    xml_str
                )

                return CResult.merge_result(
                    self.Success,
                    '元数据文件[{0}]成功加载! '.format(file_metadata_name_with_path)
                )
            else:
                raise
        except:
            parser.metadata.set_metadata_bus(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(file_metadata_name_with_path),
                self.MetaDataFormat_Text,
                ''
            )
            return CResult.merge_result(
                self.Exception,
                '元数据文件[{0}]格式不合法或解析异常, 无法处理! '.format(file_metadata_name_with_path)
            )

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[name='ProductName']",
                self.Name_ID: 'ProductName',
                self.Name_Title: 'ProductName',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "//item[name='ProduceDate']",
                self.Name_ID: 'ProduceDate',
                self.Name_Title: 'ProduceDate',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
                # self.Name_Width: 8
            }
        ]
