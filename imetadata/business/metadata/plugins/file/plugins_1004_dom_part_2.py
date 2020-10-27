# -*- coding: utf-8 -*- 
# @Time : 2020/10/20 10:11
# @Author : 赵宇飞
# @File : plugins_1004_dom_part_2.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dom import CFilePlugins_GUOTU_DOM


class plugins_1004_dom_part_2(CFilePlugins_GUOTU_DOM):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_part_2'

    def classified(self):
        """
        设计国土行业数据的dom_part_2验证规则
        todo 负责人 李宪 在这里检验dom_part_2的识别规则
        :return:
        """
        super().classified()
        char_1 = self.file_info.__file_main_name__.split('-')[0]
        char_2 = self.file_info.__file_main_name__.split('-')[1]
        if CUtils.text_is_decimal(char_1) is False \
                or CUtils.text_is_decimal(char_2) is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__
        if CUtils.equal_ignore_case(self.file_info.__file_ext__, 'tif'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = self.file_info.__file_main_name__
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None
        return self.__object_confirm__, self.__object_name__

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
        list_qa = list()
        list_qa.extend(self.init_qa_file_integrity_tif_list(self.file_info.__file_main_name_with_full_path__))
        return list_qa

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
                设置解析json格式元数据的检验规则列表, 为空表示无检查规则
                :param parser:
                :return:
                """
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer_positive,
                self.Name_XPath: 'pixelsize.width',
                self.Name_ID: 'width',
                self.Name_Title: '影像宽度',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000,
                self.Name_XPath: 'coordinate',
                self.Name_ID: 'coordinate',
                self.Name_Title: '坐标参考系',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_XPath: 'boundingbox.top',
                self.Name_ID: 'top',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error

            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_XPath: 'boundingbox.left',
                self.Name_ID: 'left',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -180,
                        self.Name_Max: 180
                    },
                self.Name_XPath: 'boundingbox.right',
                self.Name_ID: 'right',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Range:
                    {
                        self.Name_Min: -90,
                        self.Name_Max: 90
                    },
                self.Name_XPath: 'boundingbox.bottom',
                self.Name_ID: 'bottom',
                self.Name_Title: '经纬度坐标',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def init_qa_metadata_bus_xml_list(self, parser: CMetaDataParser) -> list:
        """
        初始化默认的, 业务元数据xml文件的检验列表
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type == 'mdb':

            return [
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='ysjwjm']",
                    self.Name_ID: 'ysjwjm',
                    self.Name_Title: '带扩展元数据文件名',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='sjmc']",
                    self.Name_ID: 'sjmc',
                    self.Name_Title: '对象名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='sjbqdwm']",
                    self.Name_ID: 'sjbqdwm',
                    self.Name_Title: '单位名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='sjscdwm']",
                    self.Name_ID: 'sjscdwm',
                    self.Name_Title: '单位名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='sjcbdwm']",
                    self.Name_ID: 'sjcbdwm',
                    self.Name_Title: '单位名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='sjscsj']",
                    self.Name_ID: 'sjscsj',
                    self.Name_Title: '数据上传时间',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='mj']",
                    self.Name_ID: 'mj',
                    self.Name_Title: '密级',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20,
                    self.Name_XPath: "//item[@name='th']",
                    self.Name_ID: 'th',
                    self.Name_Title: '图号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20,
                    self.Name_XPath: "//item[@name='dmfbl']",
                    self.Name_ID: 'dmfbl',
                    self.Name_Title: '地面分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20,
                    self.Name_XPath: "//item[@name='yxscms']",
                    self.Name_ID: 'yxscms',
                    self.Name_Title: '影像色彩模式',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='xsws']",
                    self.Name_ID: 'xsws',
                    self.Name_Title: '影像位深',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 25,
                    self.Name_XPath: "//item[@name='sjgs']",
                    self.Name_ID: 'sjgs',
                    self.Name_Title: '时间格式',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='dtty']",
                    self.Name_ID: 'dtty',
                    self.Name_Title: '地图投影',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 38,
                    self.Name_XPath: "//item[@name='wxmc']",
                    self.Name_ID: 'wxmc',
                    self.Name_Title: '卫星名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20,
                    self.Name_XPath: "//item[@name='qsyxcgqlx']",
                    self.Name_ID: 'qsyxcgqlx',
                    self.Name_Title: '全色影像传感器',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_decimal_or_integer,
                    self.Name_Width: 8,
                    self.Name_XPath: "//item[@name='qswxyxfbl']",
                    self.Name_ID: 'qswxyxfbl',
                    self.Name_Title: '全色卫星影像分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 38,
                    self.Name_XPath: "//item[@name='qswxyxgdh']",
                    self.Name_ID: 'qswxyxgdh',
                    self.Name_Title: '全色卫星影像轨道号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='qswxyxhqsj']",
                    self.Name_ID: 'qswxyxhqsj',
                    self.Name_Title: '全色卫星影像获取时间',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='dgpyxcgqlx']",
                    self.Name_ID: 'dgpyxcgqlx',
                    self.Name_Title: '多光谱影像传感器',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_decimal_or_integer,
                    self.Name_Width: 8,
                    self.Name_XPath: "//item[@name='dgpwxyxfbl']",
                    self.Name_ID: 'dgpwxyxfbl',
                    self.Name_Title: '多光谱卫星影像分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='dgpwxyxgdh']",
                    self.Name_ID: 'dgpwxyxgdh',
                    self.Name_Title: '多光谱卫星影像轨道号',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='dgpwxyxhqsj']",
                    self.Name_ID: 'dgpwxyxhqsj',
                    self.Name_Title: '多光谱卫星影像获取时间',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                }
            ]

        elif self.metadata_bus_transformer_type == 'mat':  # mat业务元数据

            return [
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='数据名称']",
                    self.Name_ID: '数据名称',
                    self.Name_Title: '元数据文件名',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='数据生产时间']",
                    self.Name_ID: '数据生产时间',
                    self.Name_Title: '数据生产时间',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='航摄时间']",
                    self.Name_ID: '航摄时间',
                    self.Name_Title: '航摄时间',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20,
                    self.Name_XPath: "//item[@name='密级']",
                    self.Name_ID: '密级',
                    self.Name_Title: '密级',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 10,
                    self.Name_XPath: "//item[@name='地面分辨率']",
                    self.Name_ID: '地面分辨率',
                    self.Name_Title: '地面分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='像素位数']",
                    self.Name_ID: '像素位数',
                    self.Name_Title: '像素位数',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='地图投影']",
                    self.Name_ID: '地图投影',
                    self.Name_Title: '地图投影',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 38,
                    self.Name_XPath: "//item[@name='卫星名称']",
                    self.Name_ID: '卫星名称',
                    self.Name_Title: '卫星名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 25,
                    self.Name_XPath: "//item[@name='数据格式']",
                    self.Name_ID: '数据格式',
                    self.Name_Title: '数据格式',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='数据生产单位名']",
                    self.Name_ID: '数据生产单位名',
                    self.Name_Title: '数据生产单位名',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='数据版权单位名']",
                    self.Name_ID: '数据版权单位名',
                    self.Name_Title: '数据版权单位名',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='数据出版单位名']",
                    self.Name_ID: '数据出版单位名',
                    self.Name_Title: '数据出版单位名',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                }
            ]

        else:  # xls、xlsx业务元数据

            return [
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='产品名称']",
                    self.Name_ID: '产品名称',
                    self.Name_Title: '产品名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='产品生产日期']",
                    self.Name_ID: '产品生产日期',
                    self.Name_Title: '产品生产日期',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_date,
                    self.Name_XPath: "//item[@name='航摄日期']",
                    self.Name_ID: '航摄日期',
                    self.Name_Title: '航摄日期',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 20,
                    self.Name_XPath: "//item[@name='密级']",
                    self.Name_ID: '密级',
                    self.Name_Title: '密级',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 10,
                    self.Name_XPath: "//item[@name='影像地面分辨率']",
                    self.Name_ID: '影像地面分辨率',
                    self.Name_Title: '影像地面分辨率',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Error
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 50,
                    self.Name_XPath: "//item[@name='像素位数']",
                    self.Name_ID: '像素位数',
                    self.Name_Title: '像素位数',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='地图投影名称']",
                    self.Name_ID: '地图投影名称',
                    self.Name_Title: '地图投影名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 38,
                    self.Name_XPath: "//item[@name='卫星名称']",
                    self.Name_ID: '卫星名称',
                    self.Name_Title: '卫星名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 25,
                    self.Name_XPath: "//item[@name='数据格式']",
                    self.Name_ID: '数据格式',
                    self.Name_Title: '数据格式',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='产品生产单位名称']",
                    self.Name_ID: '产品生产单位名称',
                    self.Name_Title: '产品生产单位名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: False,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='产品所有权单位名称']",
                    self.Name_ID: '产品所有权单位名称',
                    self.Name_Title: '产品所有权单位名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                },
                {
                    self.Name_Type: self.QA_Type_XML_Node_Exist,
                    self.Name_NotNull: True,
                    self.Name_DataType: self.value_type_string,
                    self.Name_Width: 100,
                    self.Name_XPath: "//item[@name='产品出版单位名称']",
                    self.Name_ID: '产品出版单位名称',
                    self.Name_Title: '产品出版单位名称',
                    self.Name_Group: self.QA_Group_Data_Integrity,
                    self.Name_Result: self.QA_Result_Warn
                }
            ]

if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_1004_dom_part_2.FileType_File,
                            r'D:\迅雷下载\数据入库1\DOM\广西影像数据\2772.0-509.0\2772.0-509.0.tif',
                            r'D:\迅雷下载\数据入库1\DOM\广西影像数据\2772.0-509.0\tif', '<root><type>dom</type></root>')
    plugins = plugins_1004_dom_part_2(file_info)
    object_confirm, object_name = plugins.classified()
    plugins.init_qa_file_list(file_info)
    if object_confirm == plugins_1004_dom_part_2.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_1004_dom_part_2.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_1004_dom_part_2.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_1004_dom_part_2.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
