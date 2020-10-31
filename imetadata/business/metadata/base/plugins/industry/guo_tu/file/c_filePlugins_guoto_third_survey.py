# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 11:21
# @Author : 赵宇飞
# @File : c_filePlugins_guoto_third_survey.py
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerThirdSurvey import \
    CMDTransformerThirdSurvey
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.database.c_factory import CFactory


class CFilePlugins_GUOTU_Third_Survey(CFilePlugins_GUOTU):

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
                                                   "where gdsid = '{0}'".format(file_name_before_six))\
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
        todo 负责人 王学谦 在这里将三调影像third_survey的业务元数据mdb多表, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

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
        todo 负责人 王学谦 在这里设定默认的质检列表
        """
        list_qa = list()
        list_qa.extend(
            self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))  # 调用默认的规则列表

        return list_qa

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
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
            }, {
                self.Name_XPath: "coordinate",
                self.Name_ID: 'coordinate',
                self.Name_Title: '坐标系参考存在',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000
            }, {
                self.Name_XPath: "boundingbox.top",
                self.Name_ID: 'boundingbox.top',
                self.Name_Title: '经纬度坐标（top）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    }
            }, {
                self.Name_XPath: "boundingbox.left",
                self.Name_ID: 'boundingbox.left',
                self.Name_Title: '经纬度坐标（left）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    }
            }, {
                self.Name_XPath: "boundingbox.right",
                self.Name_ID: 'boundingbox.right',
                self.Name_Title: '经纬度坐标（right）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    }
            }, {
                self.Name_XPath: "boundingbox.bottom",
                self.Name_ID: 'boundingbox.bottom',
                self.Name_Title: '经纬度坐标（bottom）',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    }
            }
        ]

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        todo 负责人 王学谦
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