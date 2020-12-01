# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:25 
# @Author : 王西亚 
# @File : plugins_6001_shp.py.py
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.industry.common.c_vectorFilePlugins import CVectorFilePlugins
from imetadata.database.c_factory import CFactory
from imetadata.database.tools.c_table import CTable


class plugins_6002_mdb(CVectorFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'mdb'
        # information[self.Plugins_Info_Name] = 'mdb'
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_Same_File_Main_Name
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Vector
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        # information[self.Plugins_Info_Group_Name] = self.DataGroup_Vector
        # information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group_Name])
        information[self.Plugins_Info_Child_Layer_Data_Type] = 'layer'
        information[self.Plugins_Info_Child_Layer_Plugins_Name] = 'plugins_6050_layer_vector'
        return information

    def get_classified_character(self):
        """
        设置识别的特征
        :return:
        [0]: 特征串
        [1]: 特征串的类型
            TextMatchType_Common: 常规通配符, 如 *.txt
            TextMatchType_Regex: 正则表达式
        """
        return '*.mdb', self.TextMatchType_Common

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
        return self.init_qa_file_integrity_default_list(
            self.file_info.file_name_with_full_path)  # 调用默认的规则列表,对对象及其附属文件进行质检

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        :param parser:
        :return:
        """
        return []

    def init_qa_metadata_json_list(self, parser: CMetaDataParser) -> list:
        """
        设置解析json格式元数据的检验规则列表, 为空表示无检查规则
        完成 负责人 李宪
        :param parser:
        :return:
        """
        return [
            # {
            #     self.Name_Type: self.QA_Type_XML_Node_Exist,
            #     self.Name_NotNull: True,
            #     self.Name_DataType: self.value_type_decimal_or_integer_positive,
            #     self.Name_XPath: 'pixelsize.width',
            #     self.Name_ID: 'width',
            #     self.Name_Title: '影像宽度',
            #     self.Name_Group: self.QA_Group_Data_Integrity,
            #     self.Name_Result: self.QA_Result_Error
            # },
            {
                self.Name_Type: self.QA_Type_XML_Node_Exist,
                self.Name_NotNull: True,
                self.Name_DataType: self.value_type_string,
                self.Name_Width: 1000,
                self.Name_XPath: 'layers[0].wgs84.coordinate',
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
                self.Name_XPath: 'layers[0].wgs84.extent.maxy',
                self.Name_ID: 'maxy',
                self.Name_Title: 'maxy',
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
                self.Name_XPath: 'layers[0].wgs84.extent.maxx',
                self.Name_ID: 'maxx',
                self.Name_Title: 'maxx',
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
                self.Name_XPath: 'layers[0].wgs84.extent.minx',
                self.Name_ID: 'minx',
                self.Name_Title: 'minx',
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
                self.Name_XPath: 'layers[0].wgs84.extent.miny',
                self.Name_ID: 'miny',
                self.Name_Title: 'miny',
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
        meta_data_json = parser.metadata.metadata_json()
        if meta_data_json is None:
            return CResult.merge_result(
                self.Success,
                '数据[{0}]的质检和空间等元数据解析完毕, 但子图层解析有误, 无法获取JSON格式的元数据! '.format(
                    self.file_info.file_name_with_full_path,
                )
            )

        json_data_source = meta_data_json.xpath_one('datasource', None)

        layer_list = meta_data_json.xpath_one(self.Name_Layers, None)
        if layer_list is None:
            return CResult.merge_result(
                self.Success,
                '数据[{0}]的质检和空间等元数据解析完毕, 但子图层解析有误, 元数据中无法找到layers节点! '.format(
                    self.file_info.file_name_with_full_path,
                )
            )

        error_message_list = []
        table = CTable()
        table.load_info(self.file_info.db_server_id, self.TableName_DM_Object)

        for layer in layer_list:
            layer_name = CUtils.dict_value_by_name(layer, self.Name_Name, '')
            if CUtils.equal_ignore_case(layer_name, ''):
                continue

            layer_metadata_json = CJson()
            layer_metadata_json.set_value_of_name('datasource', json_data_source)
            layer_metadata_json.set_value_of_name('layer_count', 1)
            layer_metadata_json.set_value_of_name('layers', [layer])
            layer_metadata_text = layer_metadata_json.to_json()

            try:
                sql_find_layer_existed = '''
                select dsoid as layer_id_existed
                from dm2_storage_object
                where upper(dsoobjectname) = upper(:layer_name)
                    and dsoparentobjid = :object_id
                '''
                layer_id_existed = CFactory().give_me_db(self.file_info.db_server_id).one_value(
                    sql_find_layer_existed,
                    {
                        'layer_name': layer_name,
                        'object_id': parser.object_id
                    }
                )
                if layer_id_existed is None:
                    layer_id_existed = CUtils.one_id()

                table.column_list.reset()
                table.column_list.column_by_name('dsoid').set_value(layer_id_existed)
                table.column_list.column_by_name('dsoobjectname').set_value(layer_name)
                table.column_list.column_by_name('dsoobjecttype').set_value(
                    CUtils.dict_value_by_name(
                        self.get_information(),
                        self.Plugins_Info_Child_Layer_Plugins_Name,
                        ''
                    )
                )
                table.column_list.column_by_name('dsodatatype').set_value(
                    CUtils.dict_value_by_name(
                        self.get_information(),
                        self.Plugins_Info_Child_Layer_Data_Type,
                        ''
                    )
                )
                table.column_list.column_by_name('dsoalphacode').set_value(CUtils.alpha_text(layer_name))
                table.column_list.column_by_name('dsoaliasname').set_value(layer_name)
                table.column_list.column_by_name('dsoparentobjid').set_value(parser.object_id)

                table.column_list.column_by_name('dsometadatatext').set_value(layer_metadata_text)
                table.column_list.column_by_name('dsometadatajson').set_value(layer_metadata_text)
                table.column_list.column_by_name('dsometadataparsestatus').set_value(self.ProcStatus_InQueue)
                table.column_list.column_by_name('dsotagsparsestatus').set_value(self.ProcStatus_InQueue)
                table.column_list.column_by_name('dsodetailparsestatus').set_value(self.ProcStatus_InQueue)
                result = table.save_data()
                if not CResult.result_success(result):
                    error_message_list.append(
                        '图层[{0}]的创建过程出现错误, 详细信息为: {1}'.format(
                            layer_name,
                            CResult.result_message(result)
                        )
                    )
            except Exception as error:
                error_message_list.append('图层[{0}]的创建过程出现错误, 详细信息为: {1}'.format(layer_name, error.__str__()))

        if len(error_message_list) > 0:
            return CResult.merge_result(
                self.Failure,
                '数据[{0}]的质检和空间等元数据解析完毕, 但子图层解析有误, 详细情况如下: \n{1}'.format(
                    self.file_info.file_name_with_full_path,
                    CUtils.list_2_str(error_message_list, '', '\n', '', True)
                )
            )
        else:
            return CResult.merge_result(
                self.Success,
                '数据[{0}]的自定义元数据解析完毕! '.format(
                    self.file_info.file_name_with_full_path,
                )
            )
