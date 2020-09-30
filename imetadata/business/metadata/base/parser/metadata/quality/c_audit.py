# -*- coding: utf-8 -*- 
# @Time : 2020/9/27 10:15 
# @Author : 王西亚 
# @File : c_audit.py
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class CAudit(CResource):
    @classmethod
    def __a_check_file__(cls, result_template: dict, file_name_with_path: str, **qa_items) -> list:
        """
        根据规则, 验证文件的合法性
        :param result_template 检查结果的模板
        :param file_name_with_path: 文件名
        :param qa_items: 检查项目, keywords
        :return:
        """
        pass

    @classmethod
    def __a_check_value__(cls, result_template: dict, value, title_prefix, qa_items: dict) -> list:
        """
        根据规则, 验证值的合法性
        注意: 值有可能为None!
        :param result_template: 检查结果的模板
        :param value: 待检验的值, 可能为None
        :param qa_items: 检查项目, keywords
        :return:
        """
        result_list = list()
        result_dict = result_template
        value_list = CUtils.dict_value_by_name(qa_items, cls.Name_List, None)
        if value_list is not None:
            if CUtils.list_count(value_list, value) > 0:
                result_dict[cls.Name_Message] = '{0}的值在指定列表中, 符合要求!'.format(title_prefix)
                result_dict[cls.Name_Result] = cls.QA_Result_Pass
            else:
                result_dict[cls.Name_Message] = '{0}的值[{1}], 不在指定列表中, 请检查修正!'.format(title_prefix, value)
            result_list.append(result_dict)

        return result_list

    @classmethod
    def __init_audit_dict__(cls, audit_id, audit_title, audit_level, audit_result) -> dict:
        result_dict = dict()
        result_dict[cls.Name_ID] = audit_id
        result_dict[cls.Name_Title] = audit_title
        result_dict[cls.Name_Level] = audit_level
        result_dict[cls.Name_Result] = audit_result

        return result_dict

    @classmethod
    def a_file_exist(cls, audit_id, audit_title, audit_level, audit_result, file_name_with_path,
                     qa_items: dict) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_level, audit_result)

        if CFile.file_or_path_exist(file_name_with_path):
            result_dict[cls.Name_Message] = '文件[{0}]存在, 符合要求'.format(CFile.file_name(file_name_with_path))
            result_dict[cls.Name_Result] = cls.QA_Result_Pass
        else:
            result_dict[cls.Name_Message] = '文件[{0}]不存在, 请检查'.format(CFile.file_name(file_name_with_path))

        return result_dict

    @classmethod
    def a_file_size(cls, audit_id, audit_title, audit_level, audit_type, file_name_with_path: str, size_min: int = -1,
                    size_max: int = -1) -> dict:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_level, audit_type)

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

    @classmethod
    def a_xml_element(cls, audit_id, audit_title, audit_level, audit_result, xml_obj: CXml, xpath: str,
                      qa_items: dict) -> list:
        """
        判断一个xml元数据中, 指定的xpath, 对应的element, 满足 kargs参数中的检测项目
        :param audit_id:
        :param audit_title:
        :param audit_level:
        :param audit_result:
        :param xml_obj:
        :param xpath:
        :param qa_items:
        :return:
        """
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_level, audit_result)
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
    def a_xml_attribute(cls, audit_id, audit_title, audit_level, audit_result, xml_obj: CXml, xpath: str,
                        attr_name: str, qa_items: dict) -> list:
        result_dict = cls.__init_audit_dict__(audit_id, audit_title, audit_level, audit_result)
        if xml_obj is None:
            result_dict[cls.Name_Message] = 'XML对象不合法, 节点[{0}]不存在'.format(xpath)
            return [result_dict]

        element_obj = xml_obj.xpath_one(xpath)
        if element_obj is not None:
            if CXml.attr_exist(element_obj, attr_name):
                attr_text = CXml.get_attr(element_obj, attr_name, '')
                return cls.__a_check_value__(result_dict, attr_text, 'XML对象的节点[{0}]的属性[{1}]'.format(xpath, attr_name), qa_items)
            else:
                result_dict[cls.Name_Message] = 'XML对象的节点[{0}]无属性[{1}], 请检查修正!'.format(xpath, attr_name)
        else:
            result_dict[cls.Name_Message] = 'XML对象的节点[{0}]不存在, 请检查修正!'.format(xpath)

        return [result_dict]
