# -*- coding: utf-8 -*- 
# @Time : 2020/10/25 15:21
# @Author : 赵宇飞
# @File : plugins_8050_guoqing_scene_noblock.py
from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.plugins.industry.guo_tu.file.c_filePlugins_guoto_guoqing import \
    CFilePlugins_GUOTU_GuoQing
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
import re


class plugins_8050_guoqing_scene_noblock(CFilePlugins_GUOTU_GuoQing):
    """
    数据内容	文件格式	是否有坐标系	内容样例	                说明
    影像文件
    （至少有一个img）	img/IMG	有	GF2398924020190510F.img	融合影像文件，xxxF-n、xxxM-n、xxxP-n为一组
                                GF2398924020190510M.img	多光谱影像文件
                                GF2398924020190510P.img	全色波段影像文件
    元数据文件	    xml/XML	无	GF2398924020190510M.XML	多光谱元数据文件
                                GF2398924020190510P.XML	全色元数据文件
                                GF2398924020190510Y.XML	整体元数据文件
    关于正则表达式     https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '国情影像-整景纠正'
        information[self.Plugins_Info_Name] = 'guoqing_scene_noblock'

        return information

    def classified(self):
        """
        设计国土行业数据guoqing_scene_noblock的验证规则（国情影像—非分块）,不带数字
        todo 负责人 王学谦 在这里检验guoqing_scene_noblock的识别规则
        :return:
        """
        super().classified()
        file_main_name = self.file_info.file_main_name
        file_ext = self.file_info.file_ext  # 初始化需要的参数
        file_path = self.file_info.file_path
        file_object_name = file_main_name[:]  # 这里需要取得规则匹配用的‘对象名’，即去除尾部字母等字符的名

        # 正则表达式，(?i)代表大小写不敏感，^代表字符串开头，$代表字符串结尾
        # [a-z]指匹配所有小写字母，配合(?i)匹配所有字母，{2}代表前面的匹配模式匹配2次，即[a-z]{2}匹配两个字母
        # \d匹配数字，即[0-9]，即\d+匹配一个或多个非空字符，\d{4}匹配四个任意数字
        # [0123]一般指匹配一个括号中任意字符，即匹配0到3
        # \S用于匹配所有非空字符，+代表匹配前面字符的数量为至少一个，即\S+匹配一个或多个非空字符
        if len(file_main_name) < 13:
            return self.Object_Confirm_IUnKnown, self._object_name
        # 下面正则：开头两个字母，字母后任意数量字符,而后匹配8位时间，4位任意数字（年份），[01]\d为月份，[0123]\d日
        if CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                r'\d{4}[01]\d[0123]\d[a-z]$'):  # 结尾为单个字母的情况
            file_object_name = file_main_name[:-1]  # 这里需要取得规则匹配用的‘对象名’，即去除尾部字母
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'  # 尾部没字母取原本主名
                                                  r'\d{4}[01]\d[0123]\d$'):
            pass
        elif CUtils.text_match_re(file_main_name, r'(?i)^[a-z]{2}\S+'
                                                  r'\d{4}[01]\d[0123]\d\S+$'):  # 结尾为多个的字符情况
            file_object_name_list = re.findall(r'(?i)^([a-z]{2}\S+\d{4}[01]\d[0123]\d)\S+$',
                                               file_main_name)
            file_object_name = file_object_name_list[0]  # 剔除结尾多个字符

        match_str = '(?i)^' + file_object_name + r'[FMP].img$'  # 匹配主文件的规则，即对象名+F/M/P
        check_file_main_name_exist = CFile.find_file_or_subpath_of_path(file_path, match_str, CFile.MatchType_Regex)
        if not check_file_main_name_exist:  # 检查主文件存在性
            return self.Object_Confirm_IUnKnown, self._object_name

        """文件名第1-2位为字母，最后1位是字母在F/P/M中，倒数2-9位是数字"""
        name_sub_1_to_2 = file_object_name[0:2]
        name_sub_backwards_9_to_2 = file_object_name[-8:]
        if CUtils.text_is_alpha(name_sub_1_to_2) is False \
                or CUtils.text_is_numeric(name_sub_backwards_9_to_2) is False:
            return self.Object_Confirm_IUnKnown, self._object_name

        # 作为对象的主文件存在优先级，F-M-P,比如需要F的文件不存在，M才能是主文件
        # 能跑到这里的文件已经可以认为不是主文件，就是附属文件
        match_str_f = '(?i)^' + file_object_name + r'[F].img$'
        match_str_fm = '(?i)^' + file_object_name + r'[FM].img$'
        name_sub_backwards_1 = file_main_name[-1:]
        if CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'f') \
                and CUtils.equal_ignore_case(file_ext, 'img'):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        elif CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'm') \
                and CUtils.equal_ignore_case(file_ext, 'img') \
                and not CFile.find_file_or_subpath_of_path(file_path, match_str_f, CFile.MatchType_Regex):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        elif CUtils.equal_ignore_case(name_sub_backwards_1.lower(), 'p') \
                and CUtils.equal_ignore_case(file_ext, 'img') \
                and not CFile.find_file_or_subpath_of_path(file_path, match_str_fm, CFile.MatchType_Regex):
            self._object_confirm = self.Object_Confirm_IKnown
            self._object_name = file_main_name
        else:
            self._object_confirm = self.Object_Confirm_IKnown_Not
            self._object_name = None

        return self._object_confirm, self._object_name

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        todo 负责人 王学谦
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        metadata_main_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        metadata_main_name_with_path = metadata_main_name_with_path[:-1]  # 去除尾部的F/M/P
        check_file_metadata_bus_exist = False
        ext = self.Transformer_XML
        temp_metadata_bus_file_Y = '{0}Y.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_P = '{0}P.xml'.format(metadata_main_name_with_path)
        temp_metadata_bus_file_M = '{0}M.xml'.format(metadata_main_name_with_path)
        if CFile.file_or_path_exist(temp_metadata_bus_file_Y):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_Y
        elif CFile.file_or_path_exist(temp_metadata_bus_file_P):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_P
        elif CFile.file_or_path_exist(temp_metadata_bus_file_M):
            check_file_metadata_bus_exist = True
            self.metadata_bus_transformer_type = ext
            self.metadata_bus_src_filename_with_path = temp_metadata_bus_file_M

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
                self.Name_XPath: "/Metadatafile/BasicDataContent/MetaDataFileName",
                self.Name_ID: 'MetaDataFileName',
                self.Name_Title: '带扩展名元数据文件名',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 60
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ProductName",
                self.Name_ID: 'ProductName',
                self.Name_Title: '对象名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Owner",
                self.Name_ID: 'Owner',
                self.Name_Title: '所有者',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Producer",
                self.Name_ID: 'Producer',
                self.Name_Title: '生产商',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/Publisher",
                self.Name_ID: 'Publisher',
                self.Name_Title: '出版商',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ProduceDate",
                self.Name_ID: 'ProduceDate',
                self.Name_Title: '生产日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_date,
                self.Name_NotNull: True
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ConfidentialLevel",
                self.Name_ID: 'ConfidentialLevel',
                self.Name_Title: '密级',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/GroundResolution",
                self.Name_ID: 'GroundResolution',
                self.Name_Title: '地面分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 10
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/ImgColorModel",
                self.Name_ID: 'ImgColorModel',
                self.Name_Title: '影像类型',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/PixelBits",
                self.Name_ID: 'PixelBits',
                self.Name_Title: '位深',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/DataFormat",
                self.Name_ID: 'DataFormat',
                self.Name_Title: '格式',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 25
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/BasicDataContent/MathFoundation/MapProjection",
                self.Name_ID: 'MapProjection',
                self.Name_Title: '地图投影',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 50
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/SateName",
                self.Name_ID: 'SateName',
                self.Name_Title: '星源',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/PBandSensorType",
                self.Name_ID: 'PBandSensorType',
                self.Name_Title: '全色传感器',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/SateResolution",
                self.Name_ID: 'SateResolution',
                self.Name_Title: '全色分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/PBandOribitCode",
                self.Name_ID: 'PBandOribitCode',
                self.Name_Title: '全色轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 38
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/PanBand/PBandDate",
                self.Name_ID: 'PBandDate',
                self.Name_Title: '拍摄日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_date
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/MultiBand/MultiBandSensorType",
                self.Name_ID: 'MultiBandSensorType',
                self.Name_Title: '多光谱传感器',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/MultiBand/MultiBandResolution",
                self.Name_ID: 'MultiBandResolution',
                self.Name_Title: '多光谱分辨率',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer,
                self.Name_Width: 8
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/MultiBand/MultiBandOrbitCode",
                self.Name_ID: 'MultiBandOrbitCode',
                self.Name_Title: '多光谱轨道号',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 100
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/MultiBand/MultiBandDate",
                self.Name_ID: 'MultiBandDate',
                self.Name_Title: '多光谱拍摄日期',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_decimal_or_integer
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/MultiBand/MultiBandNum",
                self.Name_ID: 'MultiBandNum',
                self.Name_Title: '波段数量',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_integer
            }, {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_XPath: "/Metadatafile/ImgSource/MultiBand/MultiBandName",
                self.Name_ID: 'MultiBandName',
                self.Name_Title: '波段名称',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 20
            }
        ]

