# -*- coding: utf-8 -*- 
# @Time : 2020/10/13 16:22
# @Author : 赵宇飞
# @File : plugins_1001_dom_10_dom.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerDOM import CMDTransformerDOM
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_dom import CFilePlugins_GUOTU_DOM
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser


class plugins_1001_dom_10_dom(CFilePlugins_GUOTU_DOM):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据'
        information[self.Plugins_Info_Name] = 'dom_10_dom'

        return information

    def classified(self):
        """
        设计国土行业数据的dom_10_dom验证规则
        todo 负责人 李宪 在这里检验dom_10_dom的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.__file_main_name__
        file_ext = self.file_info.__file_ext__

        check_file_main_name_length = len(file_main_name) == 13
        if not check_file_main_name_length:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        file_metadata_name_with_path = CFile.join_file(self.file_info.__file_path__, self.file_info.__file_main_name__)
        check_file_main_name_exist = CFile.file_or_path_exist('{0}.{1}'.format(file_metadata_name_with_path, 'tif'))

        if not check_file_main_name_exist:
            return self.Object_Confirm_IUnKnown, self.__object_name__

        """
        下面判别第1位是字母
        下面判别第4位是字母
        下面判别第23位是数字
        下面判别第567位是数字
        下面判别第8910位是数字
        下面判别第111213位是DOM
        """
        char_1 = file_main_name[0:1]
        char_2_3 = file_main_name[1:3]
        char_4 = file_main_name[3:4]
        char_5_to_7 = file_main_name[4:7]
        char_8_to_10 = file_main_name[7:10]
        char_11_to_13 = file_main_name[10:13]
        if CUtils.text_is_alpha(char_1) is False \
                or CUtils.text_is_numeric(char_2_3) is False \
                or CUtils.text_is_alpha(char_4) is False \
                or CUtils.text_is_numeric(char_5_to_7) is False \
                or CUtils.text_is_numeric(char_8_to_10) is False \
                or CUtils.equal_ignore_case(char_11_to_13,"DOM") is False:
            return self.Object_Confirm_IUnKnown, self.__object_name__
        if CUtils.equal_ignore_case(file_ext, 'tif'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = file_main_name
        else:
            self.__object_confirm__ = self.Object_Confirm_IKnown_Not
            self.__object_name__ = None

        return self.__object_confirm__, self.__object_name__

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        todo 负责人 王学谦 在这里将dom-10的元数据, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

        transformer = CMDTransformerDOM(
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
        return [
             {self.Name_FileName: '{0}.tfw'.format(self.classified_object_name()),
              self.Name_ID: 'tfw',
                self.Name_Title: '投影信息文件',
              self.Name_Result: self.QA_Result_Warn}
        ]

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
                self.Name_DataType: self.value_type_string,
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
                self.Name_Width: 8,
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
                self.Name_Width: 8,
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
                self.Name_Width: 8,
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
                self.Name_Width: 8,
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
        return [
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_date,
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
                self.Name_DataType: self.value_type_date,
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
                self.Name_DataType: self.value_type_string,
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
                self.Name_XPath: "//item[@name='QSYXCGQLX']",
                self.Name_ID: 'QSYXCGQLX',
                self.Name_Title: '全色影像传感器',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8,
                self.Name_XPath: "//item[@name='QSWXYXFBL']",
                self.Name_ID: 'QSWXYXFBL',
                self.Name_Title: '全色卫星影像分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38,
                self.Name_XPath: "//item[@name='QSWXYXGDH']",
                self.Name_ID: 'QSWXYXGDH',
                self.Name_Title: '全色卫星影像轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_string,
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
                self.Name_XPath: "//item[@name='DGPYXCGQLX']",
                self.Name_ID: 'DGPYXCGQLX',
                self.Name_Title: '多光谱影像传感器',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8,
                self.Name_XPath: "//item[@name='DGPWXYXFBL']",
                self.Name_ID: 'DGPWXYXFBL',
                self.Name_Title: '多光谱卫星影像分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100,
                self.Name_XPath: "//item[@name='DGPWXYXGDH']",
                self.Name_ID: 'DGPWXYXGDH',
                self.Name_Title: '多光谱卫星影像轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_date,
                self.Name_Width: 20,
                self.Name_XPath: "//item[@name='DGPWXYXHQSJ']",
                self.Name_ID: 'DGPWXYXHQSJ',
                self.Name_Title: '多光谱卫星影像获取时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Warn
            }
        ]
if __name__ == '__main__':
    # file_info = CFileInfoEx(plugins_1000_dom_10.FileType_File,
    #                        '/Users/wangxiya/Documents/交换/1.给我的/即时服务产品/业务数据集/DOM/湖北单个成果数据/H49G001026/H49G001026.tif',
    #                        '/Users/wangxiya/Documents/交换', '<root><type>dom</type></root>')
    file_info = CFileInfoEx(plugins_1001_dom_10_dom.FileType_File,
                            r'D:\迅雷下载\数据入库3\DOM\造的数据\dom-10\G49G001030\G49G001030DOM.tif',
                            r'D:\迅雷下载\数据入库3\DOM\造的数据\dom-10\G49G001030\tif', '<root><type>dom</type></root>')
    plugins = plugins_1001_dom_10_dom(file_info)
    object_confirm, object_name = plugins.classified()
    plugins.init_qa_file_list(file_info)
    if object_confirm == plugins_1001_dom_10_dom.Object_Confirm_IUnKnown:
        print('对不起, 您给你的文件, 我不认识')
    elif object_confirm == plugins_1001_dom_10_dom.Object_Confirm_IKnown_Not:
        print('您给你的文件, 我确认它不是对象')
    elif object_confirm == plugins_1001_dom_10_dom.Object_Confirm_IKnown:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
    elif object_confirm == plugins_1001_dom_10_dom.Object_Confirm_Maybe:
        print('您给你的文件, 我确认它的类型是[{0}], 对象名称为[{1}]'.format(plugins.get_id(), object_name))
