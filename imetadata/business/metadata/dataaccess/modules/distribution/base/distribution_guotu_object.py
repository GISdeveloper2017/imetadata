# -*- coding: utf-8 -*- 
# @Time : 2020/11/11 18:24
# @Author : 赵宇飞
# @File : distribution_guotu_object.py

from imetadata.business.metadata.dataaccess.modules.distribution.base.distribution_guotu import \
    distribution_guotu
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.base.c_json import CJson
from imetadata.base.c_xml import CXml
import datetime

class distribution_guotu_object(distribution_guotu):
    """
    对象的处理基类（即时服务）
    """

    def information(self) -> dict:
        info = super().information()
        return info

    def _do_access(self):
        try:
            quality_xml = self._quality_info  # 获取质检xml
            access_Wait_flag = self.DB_False  # 定义等待标志，为True则存在检查项目为等待
            access_Forbid_flag = self.DB_False  # 定义禁止标志，为True则存在检查项目为禁止
            message = ''
            # 注释代码在sync稳定后进行调整
            # for qa_node_id in self.access_check_list():  # 循环写好的检查列表
            #     qa_node = quality_xml.xpath_one("//item[@id='{0}']".format(qa_node_id))  # 查询xml中的节点
            #     if qa_node is not None:
            #         node_result = CXml.get_attr(qa_node, self.Name_Result, '')  # 获取质检结果
            #         if CUtils.equal_ignore_case(node_result, self.QA_Result_Pass):
            #             pass
            #         elif CUtils.equal_ignore_case(node_result, self.QA_Result_Warn):  # 警告则等待
            #             access_Wait_flag = self.DB_True
            #         else:  # 错误以及其他情况，比如''，或者为其他字段
            #             access_Forbid_flag = self.DB_True
            #             break  # 存在禁止就直接跳出
            #     else:
            #         access_Forbid_flag = self.DB_True
            #         break  # 存在禁止就直接跳出

            # 上面代码之后调整，先用下面代码写sync的内容
            # 检查级别为warn的项目
            qa_warn_node_list = CXml.node_xpath(quality_xml, "//business/item[@result='warn']")
            if len(qa_warn_node_list) != 0:
                access_Wait_flag = self.DB_True
                for qa_warn_node in qa_warn_node_list:
                    node_id = CXml.get_attr(qa_warn_node, 'id', '')
                    message = '{0}质检项目{1}的质检级别为warn，请检查\n'.format(message, node_id)
            # 检查级别为error的项目
            qa_error_node_list = CXml.node_xpath(quality_xml, "//business/item[@result='error']")
            if len(qa_error_node_list) != 0:
                access_Forbid_flag = self.DB_True
                for qa_error_node in qa_error_node_list:
                    node_id = CXml.get_attr(qa_error_node, 'id', '')
                    message = '{0}质检项目{1}的质检级别为error，请检查\n'.format(message, node_id)

            # 这里可以继续放其他的检查项目的代码

            # 开始进行检查的结果判断
            access_flag = self.DataAccess_Pass
            if access_Forbid_flag:
                access_flag = self.DataAccess_Forbid
            elif access_Wait_flag:
                access_flag = self.DataAccess_Wait
            if CUtils.equal_ignore_case(message, ''):
                message = '模块可以进行访问'

            result = CResult.merge_result(
                self.Success,
                '模块[{0}.{1}]对对象[{2}]的访问能力已经分析完毕!'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name
                )
            )
            result = CResult.merge_result_info(result, self.Name_Access, access_flag)
            result = CResult.merge_result_info(result, self.Name_Message, message)
        except:
            result = CResult.merge_result(
                self.Failure,
                '模块[{0}.{1}]对对象[{2}]的访问能力的分析存在异常!'.format(
                    CUtils.dict_value_by_name(self.information(), self.Name_ID, ''),
                    CUtils.dict_value_by_name(self.information(), self.Name_Title, ''),
                    self._obj_name
                )
            )
        return result

    def access_check_list(self) -> list:  # 预留的方法，sync写完后再调
        check_list = list()  # 如果有其他需要，则可以升级为json
        check_list.extend(['img', 'metadata_file'])  # 配置的文件质检id
        check_list.extend(['pixelsize.width', 'coordinate'])  # 配置的影像元数据质检的id
        check_list.extend(['ysjwjm', 'sjmc'])  # 配置的业务元数据质检的id
        return check_list

    def _before_access(self):
        pass

    def _before_sync(self):
        """
        查询数据库，设置通常的字段值到self._dict_sync中，用于子类个性化构建sql字段值用
        """
        pass

    def get_sync_predefined_dict(self) -> dict:
        """
        本方法的写法为强规则，字典key为字段名，字典value为对应的值或者sql语句，在写时需要加语句号，子查询语句加(),值加‘’
        子查询：sync_dict['字段名']=“(select 字段 from 表 where id=‘1’)”
        值：sync_dict['字段名']=“‘值’”
        同时，配置插件方法时请在information()方法中添加info['table_name'] = '表名'的字段
        本方法处理公共部分
        datacount:数据量 secrecylevel:密级 regioncode:行政区码 regionname:行政区 resolution:分辨率
        colormodel:色彩模式 iexldepth:像素位数 scale:比例尺分母 mainrssource:主要星源  交插件去处理
        """
        sync_dict = dict()
        object_table_id = self._obj_id
        object_table_data = self._dataset
        dsoobjectname = object_table_data.value_by_name(0, 'dsoobjectname', '')
        sync_dict['productname'] = "'{0}'".format(dsoobjectname)
        dsodcode = object_table_data.value_by_name(0, 'dsodcode', '')
        sync_dict['producttype'] = "'{0}'".format(dsodcode)
        dsodatatype = object_table_data.value_by_name(0, 'dsodatatype', '')
        sync_dict['dsodatatype'] = "'{0}'".format(dsodatatype)
        dso_time = object_table_data.value_by_name(0, 'dso_time', '')
        dso_time_json = CJson()
        dso_time_json.load_json_text(dso_time)
        sync_dict['begdate'] = "'{0}'".format(dso_time_json.xpath_one('//end_time', ''))
        sync_dict['enddate'] = "'{0}'".format(dso_time_json.xpath_one('//start_time', ''))
        sync_dict['imagedate'] = "'{0}'".format(dso_time_json.xpath_one('//time', ''))
        # sync_dict['datacount'] = "'{0}'".format('')  # 数据数量
        # sync_dict['secrecylevel'] = "'{0}'".format('')  # 密级
        # sync_dict['regioncode'] = "'{0}'".format('')  # 行政区码
        # sync_dict['regionname'] = "'{0}'".format('')  # 行政区  上面四个字段交插件处理
        sync_dict['centerx'] = "st_x(" \
                               "st_centroid(" \
                               "(select dso_geo_wgs84 from dm2_storage_object " \
                               "where dsoid='{0}')" \
                               ")" \
                               ")".format(object_table_id)
        sync_dict['centery'] = "st_y(" \
                               "st_centroid(" \
                               "(select dso_geo_wgs84 from dm2_storage_object " \
                               "where dsoid='{0}')" \
                               ")" \
                               ")".format(object_table_id)
        sync_dict['geomwkt'] = "st_astext(" \
                               "(select dso_geo_wgs84 from dm2_storage_object " \
                               "where dsoid='{0}')" \
                               ")".format(object_table_id)
        sync_dict['geomobj'] = "(select dso_geo_wgs84 from dm2_storage_object where dsoid='{0}')"\
            .format(object_table_id)
        sync_dict['browserimg'] = "(select dso_browser from dm2_storage_object where dsoid='{0}')"\
            .format(object_table_id)
        sync_dict['thumbimg'] = "(select dso_thumb from dm2_storage_object where dsoid='{0}')"\
            .format(object_table_id)
        sync_dict['producetime'] = "'{0}'".format(dso_time_json.xpath_one('//time', ''))  # 生产日期
        now_time = CUtils.any_2_str(datetime.datetime.now().strftime('%F %T'))
        sync_dict['addtime'] = "'{0}'".format(now_time)
        # sync_dict['resolution'] = "'{0}'".format('')  # 分辨率，交插件处理
        sync_dict['imgsize'] = "(select round((sum(dodfilesize)/1048576),2) from dm2_storage_obj_detail " \
                               "where dodobjectid='{0}')"\
            .format('')
        # sync_dict['colormodel'] = "'{0}'".format('')  # 交插件处理
        # sync_dict['piexldepth'] = "'{0}'".format('')  # 交插件处理
        sync_dict['isdel'] = "'0'"
        sync_dict['extent'] = "(select dso_geo_bb_native from dm2_storage_object where dsoid='{0}')"\
            .format(object_table_id)
        sync_dict['proj'] = "(select dso_prj_coordinate from dm2_storage_object where dsoid='{0}')"\
            .format(object_table_id)
        # sync_dict['remark'] = "'{0}'".format('')  # 暂时为空
        # sync_dict['ispublishservice'] = "'{0}'".format('')   # 暂时为空
        sync_dict['queryable'] = "'1'"
        # sync_dict['scale'] = "'{0}'".format('')  # 交插件处理
        # sync_dict['mainrssource'] = "'{0}'".format('')  # 交插件处理
        query_directory_id = object_table_data.value_by_name(0, 'query_directory_id', '')
        sync_dict['dsdid'] = "'{0}'".format(query_directory_id)
        query_file_id = object_table_data.value_by_name(0, 'query_file_id', '')
        sync_dict['dsfid'] = "'{0}'".format(query_file_id)
        sync_dict['imagedatetag'] = "'{0}'".format(
            CUtils.any_2_str(dso_time_json.xpath_one('//time', ''))
        )

        return sync_dict
