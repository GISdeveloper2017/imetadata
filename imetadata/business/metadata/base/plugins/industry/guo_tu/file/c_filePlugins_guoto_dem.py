# -*- coding: utf-8 -*- 
# @Time : 2020/10/17 15:24 
# @Author : 王西亚 
# @File : c_filePlugins_guoto_dem.py
from imetadata.base.c_file import CFile
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.busmetadata.c_mdTransformerDEM import CMDTransformerDEM
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.guo_tu.c_filePlugins_guotu import CFilePlugins_GUOTU


class CFilePlugins_GUOTU_DEM(CFilePlugins_GUOTU):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DEM
        information[self.Plugins_Info_Code] = '02010601'  # 只有分幅DEM继承于这个类 （非分幅DEM在21at基类中）
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Object_Business
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_object_dem'
        return information

    def init_metadata_bus(self, parser: CMetaDataParser) -> str:
        """
        提取xml格式的业务元数据, 加载到parser的metadata对象中
        完成 负责人 王学谦 在这里将dem的元数据, 转换为xml, 存储到parser.metadata.set_metadata_bus_file中
        :param parser:
        :return:
        """
        if self.metadata_bus_transformer_type is None:
            parser.metadata.set_metadata_bus(self.DB_True, '', self.MetaDataFormat_Text, '')
            return CResult.merge_result(self.Success, '本数据无业务元数据, 无须解析!')

        transformer = CMDTransformerDEM(
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
        完成 负责人 李宪
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
        list_qa.extend(self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path))
        return list_qa

    def qa_file_custom(self, parser: CMetaDataParser):
        """
        自定义的文件存在性质检, 发生在元数据解析之前
        完成 负责人 李宪
        :param parser:
        :return:
        """
        super().qa_file_custom(parser)
        file_metadata_name_with_path = CFile.join_file(self.file_info.file_path, self.file_info.file_main_name)
        check_file_metadata_name_exist = False
        ext_list = ['xls', 'xlsx', 'mat', 'mdb']
        for ext in ext_list:
            temp_metadata_bus_file = '{0}.{1}'.format(file_metadata_name_with_path, ext)
            if CFile.file_or_path_exist(temp_metadata_bus_file):
                check_file_metadata_name_exist = True
                self.metadata_bus_transformer_type = ext
                self.metadata_bus_src_filename_with_path = temp_metadata_bus_file
                break

        if not check_file_metadata_name_exist:
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
        完成 负责人 李宪
        :param parser:
        :return:
        """
        transformer_type = CUtils.text_to_lower(self.metadata_bus_transformer_type)
        if transformer_type == 'mdb':
            return self.__metadata_bus_mdb_list__()
        elif transformer_type == 'mat':
            return self.__metadata_bus_mat_list__()
        elif transformer_type == 'xls' or transformer_type == 'xlsx':
            return self.__metadata_bus_xls_list__()
        else:
            return []

        # if self.metadata_bus_transformer_type is not None:
        #     transformer_type = self.metadata_bus_transformer_type.lower()
        #     if transformer_type == 'mdb':
        #         return self.__metadata_bus_mdb_list__()
        #     elif transformer_type == 'mat':
        #         return self.__metadata_bus_mat_list__()
        #     elif transformer_type == 'xls' or transformer_type == 'xlsx':
        #         return self.__metadata_bus_xls_list__()
        #     else:
        #         return []
        # else:
        #     return []

    def __metadata_bus_mdb_list__(self) -> list:
        """
        mdb的质检字段列表
        @return:
        """
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_date,
                self.Name_XPath: "//item[@name='qswxyxhqsj']",
                self.Name_ID: 'qswxyxhqsj',
                self.Name_Title: '全色卫星影像获取时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
            },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: False,
                self.Name_DataType: self.value_type_date,
                self.Name_XPath: "//item[@name='dgpwxyxhqsj']",
                self.Name_ID: 'dgpwxyxhqsj',
                self.Name_Title: '多光谱卫星影像获取时间',
                self.Name_Group: self.QA_Group_Data_Integrity,
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def __metadata_bus_mat_list__(self) -> list:
        """
        mat的质检字段列表
        @return:
        """
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def __metadata_bus_xls_list__(self) -> list:
        """
        xls/xlsx的质检字段列表
        @return:
        """
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
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
                self.Name_Result: self.QA_Result_Error
            }
        ]

    def parser_metadata_time_list(self, parser: CMetaDataParser) -> list:
        """
        标准模式的提取时间信息的列表
        完成 负责人 李宪
        :param parser:
        :return:
        """
        transformer_type = CUtils.text_to_lower(self.metadata_bus_transformer_type)
        if transformer_type == 'mdb':
            return self.__metadata_time_mdb_list()
        elif transformer_type == 'mat':
            return self.__metadata_time_mat_list()
        elif transformer_type == 'xls' or transformer_type == 'xlsx':
            return self.__metadata_time_xls_list()
        else:
            return []

        # if self.metadata_bus_transformer_type is not None:
        #     transformer_type = self.metadata_bus_transformer_type.lower()
        #     if transformer_type == 'mdb':
        #         return self.__metadata_time_mdb_list()
        #     elif transformer_type == 'mat':
        #         return self.__metadata_time_mat_list()
        #     elif transformer_type == 'xls' or transformer_type == 'xlsx':
        #         return self.__metadata_time_xls_list()
        #     else:
        #         return []
        # else:
        #     return []

    def __metadata_time_mdb_list(self) -> list:
        """
        标准模式的提取时间信息的列表
        self.Name_Source
        1. self.Name_Business: 表示从数据的业务xml元数据中取(默认, 可以不设置)
        1. self.Name_Data: 表示从数据的xml元数据中取
        :param parser:
        :return:
        """
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: "//item[@name='sjscsj']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: "//item[@name='sjscsj']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: "//item[@name='sjscsj']",
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def __metadata_time_mat_list(self) -> list:
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: "//item[@name='航摄时间']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: "//item[@name='航摄时间']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: "//item[@name='航摄时间']",
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]

    def __metadata_time_xls_list(self) -> list:
        return [
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Time,
                self.Name_XPath: "//item[@name='航摄日期']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_Start_Time,
                self.Name_XPath: "//item[@name='航摄日期']",
                self.Name_Format: self.MetaDataFormat_XML
            },
            {
                self.Name_Source: self.Name_Business,
                self.Name_ID: self.Name_End_Time,
                self.Name_XPath: "//item[@name='航摄日期']",
                self.Name_Format: self.MetaDataFormat_XML
            }
        ]
