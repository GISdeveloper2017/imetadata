# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:21
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_third_survey.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerThirdSurvey import \
    CMDTransformerThirdSurvey
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU
from imetadata.database.c_factory import CFactory


class CFilePlugins_GUOTU_Third_Survey(CFilePlugins_GUOTU):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '三调影像'
        information[self.Plugins_Info_Type_Title] = information[self.Plugins_Info_Type]
        information[self.Plugins_Info_Type_Code] = '020104'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_third_survey'
        return information

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        file_path = self.file_info.file_path
        file_main_name = self.file_info.file_main_name
        file_name_before_six = file_main_name[0:6]  # 截取前六位行政区划代码
        # 查询行政区划代码对应的名称并拼接
        try:
            db = CFactory().give_me_db(self.file_info.db_server_id)
            file_name_before_six_name = db.one_row("select gdstitle from ro_global_dim_space "
                                                   "where gdsid = '{0}'".format(file_name_before_six)) \
                .value_by_name(0, 'gdstitle', None)
        except:
            file_name_before_six_name = ''
        file_metadata_name = '{0}{1}'.format(file_name_before_six, file_name_before_six_name)
        check_file_metadata_bus_exist = False
        ext = self.Transformer_DOM_MDB  # 后缀名

        metadata_main_name_with_path = CFile.join_file(file_path, file_metadata_name)
        # 拼接好元数据文件名称，并检查其是否存在
        temp_metadata_bus_file = '{0}.{1}'.format(metadata_main_name_with_path, ext)
        if CFile.file_or_path_exist(temp_metadata_bus_file):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file

        if not check_file_metadata_bus_exist:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: '',
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Error,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '本文件缺少业务元数据'
                }
            )
        else:
            parser.metadata.quality.append_total_quality(
                {
                    self.Name_FileName: self.metadata_bus_src_filename_with_path,
                    self.Name_ID: 'metadata_file',
                    self.Name_Title: '元数据文件',
                    self.Name_Result: self.QA_Result_Pass,
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Message: '业务元数据[{0}]存在'.format(self.metadata_bus_src_filename_with_path)
                }
            )

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        完成 负责人 王学谦 在这里将三调影像third_survey的业务元数据mdb多表, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            return CResult.merge_result(
                self.Failure,
                '数据{0}无业务元数据文件，请检查数据业务元数据文件是否存在!'.format(self.file_info.file_main_name)
            )

        transformer = CMDTransformerThirdSurvey(
            parser.object_id,
            parser.object_name,
            parser.file_info,
            parser.file_content,
            parser.metadata,
            self.metadata_bus_transformer_type,
            self.metadata_bus_src_filename_with_path
        )
        return transformer.process()

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        初始化ortho文件的质检列表,调用默认的img方法，并拼接剩余附属文件
        完成 负责人 王学谦 在这里设定默认的质检列表
        """
        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))  # 调用默认的规则列表

        return list_qa

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        完成 负责人 王学谦
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='ysjwjm']",
                self.Name_ID: 'mbii.ysjwjm',
                self.Name_Title: '元数据文件名',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='xzqdm']",
                self.Name_ID: 'mbii.xzqdm',
                self.Name_Title: '8位数字代码',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='xmc']",
                self.Name_ID: 'mbii.xmc',
                self.Name_Title: '行政区名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='mfqk']",
                self.Name_ID: 'mbii.mfqk',
                self.Name_Title: '满幅情况',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='sjgs']",
                self.Name_ID: 'mbii.sjgs',
                self.Name_Title: '数据格式',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 25
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='dtty']",
                self.Name_ID: 'mbii.dtty',
                self.Name_Title: '地图投影',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='zyjx']",
                self.Name_ID: 'mbii.zyjx',
                self.Name_Title: '中央经线',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='fdfs']",
                self.Name_ID: 'mbii.fdfs',
                self.Name_Title: '分带方式',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='gsklgtydh']",
                self.Name_ID: 'mbii.gsklgtydh',
                self.Name_Title: '投影带号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_integer,
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='zbdw']",
                self.Name_ID: 'mbii.zbdw',
                self.Name_Title: '坐标单位',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='gcjz']",
                self.Name_ID: 'mbii.gcjz',
                self.Name_Title: '高程基准',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='mj']",
                self.Name_ID: 'mbii.mj',
                self.Name_Title: '密级',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='sjscdw']",
                self.Name_ID: 'mbii.sjscdw',
                self.Name_Title: '单位名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/root/property[@tablename='mbii']/item[@name='sjscsj']",
                self.Name_ID: 'mbii.sjscsj',
                self.Name_Title: '生产时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_date,
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        """
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: "//item[@name='sx']",
                # self.Name_XPath: "//item[@name='sjscsj']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: "//item[@name='sx']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: "//item[@name='sx']",
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def add_file_to_detail_list(self, match_name):
        """
        设定国土行业数据三调的附属文件的验证规则（镶嵌影像）
        完成 负责人 王学谦 在这里检验三调的附属文件
        :return:
        """
        file_main_name = self._object_name
        file_path = self.file_info.file_path
        # 模糊匹配附属文件
        if not CUtils.equal_ignore_case(file_path, ''):
            match_str = '{0}*xq.*'.format(match_name)
            match_file_list = CFile.file_or_dir_fullname_of_path(file_path, False, match_str, CFile.MatchType_Common)
            for file_with_path in match_file_list:
                if not CUtils.equal_ignore_case(CFile.file_main_name(file_with_path), file_main_name):  # 去除自身与同名文件
                    self.add_file_to_details(file_with_path)  # 将文件加入到附属文件列表中
            try:
                db = CFactory().give_me_db(self.file_info.db_server_id)
                metadata_name_before_six_name = db.one_row("select gdstitle from ro_global_dim_space "
                                                           "where gdsid = '{0}'".format(match_name)) \
                    .value_by_name(0, 'gdstitle', None)
                metadata_file_name = '{0}{1}.mdb'.format(match_name, metadata_name_before_six_name)
                metadata_file_name_with_path = CFile.join_file(file_path, metadata_file_name)
                if CFile.file_or_path_exist(metadata_file_name_with_path):
                    self.add_file_to_details(metadata_file_name_with_path)
            except:
                pass
