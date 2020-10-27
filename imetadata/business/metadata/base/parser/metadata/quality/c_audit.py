# -*- coding: utf-8 -*- 
# @Time : 2020/9/27 10:15 
# @Author : 王西亚 
# @File : c_audit.py
from imetadata.base.c_file import CFile
from imetadata.base.c_gdalUtils import CGdalUtils
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml
from imetadata.database.c_factory import CFactory
import copy


class CAudit(CResource):

    @classmethod
    def __a_check_file__(cls, result_template: dict, file_name_with_path: str, qa_items: dict) -> list:
        """
        根据规则, 验证文件的合法性
        todo 负责人 赵宇飞 在这里对文件的其他内容进行质检, 目前实现了检查文件大小, 请参考__a_check_file_size__完善其他内容, 包括并不限于
            验证文件可读性, 验证元数据文件可读性, 验证元数据文件的格式(xml\json), 以便于后面在处理元数据时, 不会出现异常
        :param result_template 检查结果的模板
        :param file_name_with_path: 文件名
        :param qa_items: 检查项目, keywords
        :return:
        """
        result_list = list()

        result_list.append(
            cls.__a_check_file_size__(
                result_template,
                file_name_with_path,
                CJson.dict_attr_by_path(qa_items, '{0}.{1}'.format(cls.Name_Size, cls.Name_Min), -1),
                CJson.dict_attr_by_path(qa_items, '{0}.{1}'.format(cls.Name_Size, cls.Name_Max), -1)
            )
        )

        result_list.append(
            cls.__a_check_file_format__(
                result_template,
                file_name_with_path,
                CJson.dict_attr_by_path(qa_items, cls.Name_Format, None)
            )
        )

        return result_list

    @classmethod
    def __a_check_value__(cls, result_template: dict, value, title_prefix, qa_items: dict) -> list:
        """
        根据规则, 验证值的合法性
        注意: 值有可能为None!
        todo 负责人 赵宇飞 这里仅仅对值进行了字典检验, 请添加其他检验, 比如大小判断, 数值类型判断, 长度检验等内容
        :param result_template: 检查结果的模板
        :param value: 待检验的值, 可能为None
        :param qa_items: 检查项目, keywords
        :return:
        """
        result_list = list()

        value_not_null = CUtils.dict_value_by_name(qa_items, cls.Name_NotNull, None)
        if value_not_null is not None:
            result_list.append(cls.__a_check_value_not_null__(result_template, value, title_prefix, value_not_null))

        if not CUtils.equal_ignore_case(value, ''):
            value_type = CUtils.dict_value_by_name(qa_items, cls.Name_DataType, None)
            if value_type is not None:
                result_list.append(cls.__a_check_value_datatype__(result_template, value, title_prefix, value_type))

            value_range = CUtils.dict_value_by_name(qa_items, cls.Name_Range, None)
            if value_range is not None:
                result_list.append(cls.__a_check_value_range__(result_template, value, title_prefix, qa_items))

            value_width = CUtils.dict_value_by_name(qa_items, cls.Name_Width, None)
            if value_width is not None:
                result_list.append(cls.__a_check_value_width__(result_template, value, title_prefix, value_width))

            value_list = CUtils.dict_value_by_name(qa_items, cls.Name_List, None)
            if value_list is not None:
                result_list.append(cls.__a_check_value_in_list__(result_template, value, title_prefix, value_list))

            value_sql = CUtils.dict_value_by_name(qa_items, cls.Name_SQL, None)
            if value_sql is not None:
                value_sql_db_server_id = CUtils.dict_value_by_name(qa_items, cls.Name_DataBase,
                                                                   cls.DB_Server_ID_Default)
                result_list.append(
                    cls.__a_check_value_in_sql__(result_template, value, title_prefix, value_sql_db_server_id,
                                                 value_sql))

        return result_list

    @classmethod
    def __init_audit_dict__(cls, audit_id, audit_title, audit_group, audit_result) -> dict:
        result_dict = dict()
        result_dict[cls.Name_ID] = audit_id
        result_dict[cls.Name_Title] = audit_title
        result_dict[cls.Name_Group] = audit_group
        result_dict[cls.Name_Result] = audit_result

        return result_dict

    @classmethod
    def a_file(cls, audit_id, audit_title, audit_group, audit_result, file_name_with_path,
               qa_items: dict) -> list:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_group, audit_result)

        if CFile.file_or_path_exist(file_name_with_path):
            return cls.__a_check_file__(result_dict, file_name_with_path, qa_items)
        else:
            result_dict[cls.Name_Message] = '文件[{0}]不存在, 请检查'.format(CFile.file_name(file_name_with_path))

        return [result_dict]

    @classmethod
    def a_xml_element(cls, audit_id, audit_title, audit_group, audit_result, xml_obj: CXml, xpath: str,
                      qa_items: dict) -> list:
        """
        判断一个xml元数据中, 指定的xpath, 对应的element, 满足 kargs参数中的检测项目
        :param audit_id:
        :param audit_title:
        :param audit_group:
        :param audit_result:
        :param xml_obj:
        :param xpath:
        :param qa_items:
        :return:
        """
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_group, audit_result)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return [result_dict]

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            element_text = CXml.get_element_text(element_obj)
            return cls.__a_check_value__(result_dict, element_text, 'XML对象的节点[{0}]'.format(xpath), qa_items)
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)
            return [result_dict]

    @classmethod
    def a_xml_attribute(cls, audit_id, audit_title, audit_group, audit_result, xml_obj: CXml, xpath: str,
                        attr_name: str, qa_items: dict) -> list:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_group, audit_result)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return [result_dict]

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            if CXml.attr_exist(element_obj, attr_name):
                attr_text = CXml.get_attr(element_obj, attr_name, '')
                return cls.__a_check_value__(result_dict, attr_text, 'XML对象的节点[{0}]的属性[{1}]'.format(xpath, attr_name),
                                             qa_items)
            else:
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]无属性[{1}], 请检查修正!'.format(xpath, attr_name)
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)

        return [result_dict]

    @classmethod
    def a_json_element(cls, audit_id, audit_title, audit_group, audit_result, json_obj: CJson, xpath: str,
                       qa_items: dict) -> list:
        """
        判断一个json元数据中, 指定的jsonpath, 对应的element, 满足qa_items参数中的检测项目
        :param audit_id:
        :param audit_title:
        :param audit_group:
        :param audit_result:
        :param json_obj:
        :param xpath:
        :param qa_items:
        :return:
        """
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_group, audit_result)
        if json_obj is None:
            result_dict[cls.Name_Message] = 'Json对象不合法, 节点[{0}]不存在'.format(xpath)
            return [result_dict]

        json_value = json_obj.xpath_one(xpath, None)
        if json_value is not None:
            return cls.__a_check_value__(result_dict, json_value, 'Json对象的节点[{0}]'.format(xpath), qa_items)
        else:
            result_dict[cls.Name_Message] = 'Json对象的节点[{0}]不存在, 请检查修正!'.format(xpath)
            return [result_dict]

    @classmethod
    def __a_check_value_width__(cls, result_template: dict, value, title_prefix, value_width):
        """
        根据规则, 验证值的合法性
        注意: 值有可能为None!
        todo 负责人 赵宇飞 这里对值进行了长度检验
        :param result_template: 检查结果的模板
        :param value: 待检验的值, 可能为None
        :param title_prefix: 提示文本的前缀
        :param value_width: 检查value的宽度
        :return:
        """
        result_dict = copy.deepcopy(result_template)
        value_lenth = CUtils.len_of_text(value)
        if value_lenth <= value_width:
            result_dict[cls.Name_Message] = '{0}的值的宽度不超过{1}, 符合要求!'.format(title_prefix, value_width)
            result_dict[cls.Name_Result] = cls.QA_Result_Pass
        else:
            result_dict[cls.Name_Message] = '{0}的值[{1}],宽度为[{2}]，不符合要求的宽度不超过[{3}], 请检查修正!'.format(title_prefix,
                                                                                               value, value_lenth,
                                                                                               value_width)

        return result_dict

    @classmethod
    def __a_check_value_in_list__(cls, result_template: dict, value, title_prefix, value_list: list):
        """
        根据规则, 验证值的合法性
        注意: 值有可能为None!
        todo 负责人 赵宇飞 这里对值在列表中存在性检验
        :param result_template: 检查结果的模板
        :param value: 待检验的值, 可能为None
        :param title_prefix: 提示文本的前缀
        :param value_list: 检查value的必须存在于指定的列表
        :return:
        """
        result_dict = copy.deepcopy(result_template)
        if CUtils.list_count(value_list, value) > 0:
            result_dict[cls.Name_Message] = '{0}的值在指定列表中, 符合要求!'.format(title_prefix)
            result_dict[cls.Name_Result] = cls.QA_Result_Pass
        else:
            result_dict[cls.Name_Message] = '{0}的值[{1}], 不在指定列表中, 请检查修正!'.format(title_prefix, value)

        return result_dict

    @classmethod
    def __a_check_value_in_sql__(cls, result_template: dict, value, title_prefix, db_server_id: str, sql: str):
        """
        根据规则, 验证值的合法性
        注意: 值有可能为None!
        todo 负责人 赵宇飞 这里判断值在指定的sql查询必须有结果
        :param result_template: 检查结果的模板
        :param value: 待检验的值, 可能为None
        :param title_prefix: 提示文本的前缀
        :param db_server_id: 检查value的必须存在于指定的数据库中
        :param sql: 检查value的必须存在于指定的sql中, sql中只有一个参数, 注意
        :return:
        """
        result_dict = copy.deepcopy(result_template)
        is_exist_in_sql = False
        ds = CFactory().give_me_db(db_server_id).one_row(sql)
        if not ds.is_empty():
            # field_count = ds.field_count()
            for row_index in range(ds.size()):
                row_value = ds.value_by_index(row_index, 0, "")  # 取出第1列的行值
                if CUtils.equal_ignore_case(row_value, value):
                    is_exist_in_sql = True
                    break

        if is_exist_in_sql:
            result_dict[cls.Name_Message] = '{0}的值在指定的sql查询结果中, 符合要求!'.format(title_prefix)
            result_dict[cls.Name_Result] = cls.QA_Result_Pass
        else:
            result_dict[cls.Name_Message] = '{0}的值[{1}], 不在指定的sql查询结果中, 请检查修正，sql为【{2}】!'.format(title_prefix, value,
                                                                                                 sql)

        return result_dict

    @classmethod
    def __a_check_value_datatype__(cls, result_template: dict, value, title_prefix, value_type):
        """
        TODO 赵宇飞 对字段值根据字段类型进行检验（正整数或正小数类型、数字类型（科学计数法/正负整数/正负小数）、文本类型、日期类型...）
        :param result_template: 检查结果的模板
        :param value: 待检验的值, 可能为None
        :param title_prefix:
        :param value_type: 类型（正整数类型、数字类型（科学计数法/正负整数/正负小数）、文本类型、日期类型...）
        :return:
        """
        result_dict = copy.deepcopy(result_template)
        if CUtils.equal_ignore_case(value_type, cls.value_type_string):
            if CUtils.text_is_string(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_date):
            if CUtils.text_is_date(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_datetime):
            if CUtils.text_is_datetime(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_date_or_datetime):
            if CUtils.text_is_date_or_datetime(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_decimal):
            if CUtils.text_is_decimal(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_integer):
            if CUtils.text_is_integer(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_decimal_or_integer):
            if CUtils.text_is_decimal_or_integer(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        elif CUtils.equal_ignore_case(value_type, cls.value_type_decimal_or_integer_positive):
            if CUtils.text_is_decimal_or_integer_positive(value):
                result_dict[cls.Name_Message] = '{0}的值类型符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值【{1}】的类型不符合【{2}】类型, 请检查修正!'.format(title_prefix, value,
                                                                                         value_type)
        return result_dict

    @classmethod
    def __a_check_value_range__(cls, result_template, value, title_prefix, qa_items):
        """
         判断数字的范围，如经纬度坐标值：（-180 ~ 180） （-90~90）
        @param result_template:
        @param value:
        @param title_prefix:
        @param qa_items:
        @return:
        """
        default_value = -1.000001
        range_max = CUtils.to_decimal(
            CJson.dict_attr_by_path(qa_items, '{0}.{1}'.format(cls.Name_Range, cls.Name_Max), default_value))
        range_min = CUtils.to_decimal(
            CJson.dict_attr_by_path(qa_items, '{0}.{1}'.format(cls.Name_Range, cls.Name_Min), default_value))

        result_dict = copy.deepcopy(result_template)

        value_real = CUtils.to_decimal(value, -1)

        if range_max != default_value and range_min != default_value:
            if range_min <= value_real <= range_max:
                result_dict[cls.Name_Message] = '[{0}]的值[{1}]在指定的[{2}-{3}]范围内, 符合要求!'.format(
                    title_prefix,
                    value, range_min,
                    range_max)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '[{0}]的值[{1}]在指定的[{2}-{3}]范围外, 请检查!'.format(
                    title_prefix,
                    value, range_min,
                    range_max)
        elif range_min != default_value:
            if range_min <= value_real:
                result_dict[cls.Name_Message] = '[{0}]的值[{1}]大于最小值[{2}], 符合要求!'.format(
                    title_prefix,
                    value, range_min)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '[{0}]的值[{1}]低于最小值[{2}], 请检查!'.format(
                    title_prefix,
                    value, range_min)
        elif range_max != default_value:
            if range_max >= value_real:
                result_dict[cls.Name_Message] = '[{0}]的值[{1}]低于最大值[{2}], 符合要求!'.format(
                    title_prefix,
                    value, range_max)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '[{0}]的值[{1}]超过最大值[{2}], 请检查!'.format(
                    title_prefix,
                    value, range_max)
        else:
            result_dict[cls.Name_Message] = '[{0}]的值[{1}]未给定限定范围, 默认符合要求!'.format(
                title_prefix, value)
            result_dict[cls.Name_Result] = cls.QA_Result_Pass

        return result_dict


    @classmethod
    def __a_check_value_not_null__(cls, result_template: dict, value, title_prefix, value_not_null):
        """
            对结果值不为空进行校验
        @param result_template:
        @param value:
        @param title_prefix:
        @return:
        """
        result_dict = copy.deepcopy(result_template)
        if value_not_null is None or value_not_null is False:
            result_dict[cls.Name_Message] = '{0}的值可以为空, 符合要求!'.format(title_prefix)
            result_dict[cls.Name_Result] = cls.QA_Result_Pass
            return result_dict

        if value_not_null is True:
            if value is not None and (not CUtils.equal_ignore_case(value, '')):
                result_dict[cls.Name_Message] = '{0}的值不为空, 符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值为空, 请检查修正!'.format(title_prefix, value)
        return result_dict

    @classmethod
    def __a_check_file_format__(cls, result_template: dict, file_name_with_path: str, file_format: str):
        result_dict = copy.deepcopy(result_template)

        if CUtils.equal_ignore_case(file_format, cls.MetaDataFormat_XML):
            try:
                CXml().load_file(file_name_with_path)
                result_dict[cls.Name_Message] = '文件[{0}]为合法的XML, 符合要求!'.format(
                    CFile.file_name(file_name_with_path))
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            except:
                result_dict[cls.Name_Message] = '文件[{0}]不是合法的XML, 请检查!'.format(
                    CFile.file_name(file_name_with_path))
        elif CUtils.equal_ignore_case(file_format, cls.MetaDataFormat_Json):
            try:
                CJson().load_file(file_name_with_path)
                result_dict[cls.Name_Message] = '文件[{0}]为合法的JSON, 符合要求!'.format(
                    CFile.file_name(file_name_with_path))
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            except:
                result_dict[cls.Name_Message] = '文件[{0}]不是合法的JSON, 请检查!'.format(
                    CFile.file_name(file_name_with_path))
        elif CUtils.equal_ignore_case(file_format, cls.DataFormat_Vector_File):
            # 判断是否能正常打开矢量数据文件 file_name_with_path
            is_file_can_read = CGdalUtils.is_vector_file_can_read(file_name_with_path)
            if is_file_can_read:
                result_dict[cls.Name_Message] = '文件[{0}]为合法的矢量数据, 符合要求!'.format(
                    CFile.file_name(file_name_with_path))
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]不是合法的矢量数据, 请检查!'.format(
                    CFile.file_name(file_name_with_path))
        elif CUtils.equal_ignore_case(file_format, cls.DataFormat_Vector_Dataset):
            """
            todo 判断是否能正常打开矢量数据集 file_name_with_path
            """
            is_can_read = CGdalUtils.is_vector_dataset_can_read(file_name_with_path)
            if is_can_read:
                result_dict[cls.Name_Message] = '文件[{0}]为合法的矢量数据集, 符合要求!'.format(
                    CFile.file_name(file_name_with_path))
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]不是合法的矢量数据集, 请检查!'.format(
                    CFile.file_name(file_name_with_path))
        elif CUtils.equal_ignore_case(file_format, cls.DataFormat_Raster_File):
            # 判断是否能正常打开影像数据文件 file_name_with_path
            is_file_can_read = CGdalUtils.is_raster_file_can_read(file_name_with_path)
            if is_file_can_read:
                result_dict[cls.Name_Message] = '文件[{0}]为合法的影像数据, 符合要求!'.format(
                    CFile.file_name(file_name_with_path))
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]不是合法的影像数据, 请检查!'.format(
                    CFile.file_name(file_name_with_path))
        else:
            result_dict[cls.Name_Message] = '文件[{0}]未给定格式要求, 默认符合要求!'.format(
                CFile.file_name(file_name_with_path))
            result_dict[cls.Name_Result] = cls.QA_Result_Pass

        return result_dict

    @classmethod
    def __a_check_file_size__(cls, result_template: dict, file_name_with_path: str, size_min: int,
                              size_max: int) -> list:
        """
        根据规则, 验证文件大小的合法性
        :param result_template 检查结果的模板
        :param file_name_with_path: 文件名
        :param size_min: 最小要求, -1表示忽略比较
        :param size_max: 最大要求, -1表示忽略比较
        :return:
        """
        result_dict = copy.deepcopy(result_template)

        file_size = CFile.file_size(file_name_with_path)

        if size_min != -1 and size_min != -1:
            if size_min <= file_size <= size_max:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]在指定的[{2}-{3}]范围内, 符合要求!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_min,
                    size_max)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]在指定的[{2}-{3}]范围外, 请检查!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_min,
                    size_max)
        elif size_min != -1:
            if size_min <= file_size:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]大于最小值[{2}], 符合要求!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_min)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]低于最小值[{2}], 请检查!'.format(
                    CFile.file_name(file_name_with_path), file_size,
                    size_min)
        elif size_max != -1:
            if size_max >= file_size:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]低于最大值[{2}], 符合要求!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_max)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]超过最大值[{2}], 请检查!'.format(
                    CFile.file_name(file_name_with_path),
                    file_size, size_max)
        else:
            result_dict[cls.Name_Message] = '文件[{0}]的大小[{1}]未给定限定范围, 默认符合要求!'.format(
                CFile.file_name(file_name_with_path), file_size)
            result_dict[cls.Name_Result] = cls.QA_Result_Pass

        return result_dict


