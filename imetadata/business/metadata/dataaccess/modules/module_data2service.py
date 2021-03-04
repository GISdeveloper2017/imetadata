# -*- coding: utf-8 -*- 
# @Time : 2020/11/13 18:56 
# @Author : 王西亚 
# @File : module_data2service.py
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.dataaccess.base.c_daModule import CDAModule
from imetadata.database.c_factory import CFactory


class module_data2service(CDAModule):
    """
    数据服务发布模块
    """

    def information(self) -> dict:
        info = super().information()
        info[self.Name_Title] = '数据服务发布'

        return info

    def access(self, obj_id, obj_name, obj_type, quality) -> str:
        """
        解析数管中识别出的对象, 与第三方模块的访问能力, 在本方法中进行处理
        返回的json格式字符串中, 是默认的CResult格式, 但是在其中还增加了Access属性, 通过它反馈当前对象是否满足第三方模块的应用要求
        注意: 一定要反馈Access属性
        :return:
        """
        result = self.__test_module_obj(obj_id)
        if not CResult.result_success(result):
            return result
        result = super().access(obj_id, obj_name, obj_type, quality)
        return CResult.merge_result_info(result, self.Name_Access, self.DataAccess_Wait)

    def __test_module_obj(self, obj_id):
        sql_query = '''
                    SELECT
                        dso_quality_summary
                    FROM
                        dm2_storage_object
                    WHERE
                        dm2_storage_object.dsoid = '{0}'
                '''.format(obj_id)
        db_id = self._db_id
        dataset = CFactory().give_me_db(db_id).one_row(sql_query)
        dso_quality_summary = dataset.value_by_name('dso_quality_summary', None)
        dso_quality_summary_json = CJson()
        dso_quality_summary_json.load_json_text(dso_quality_summary)
        data = dso_quality_summary_json.xpath_one('data.items', '')     #影像文件
        total = dso_quality_summary_json.xpath_one('data.items', '')
        metadata_data = dso_quality_summary_json.xpath_one('data.items', '')    #实体元数据
        metadata_business = dso_quality_summary_json.xpath_one('data.items', '')    #业务元数据
        if CUtils.equal_ignore_case(data, 'pass') \
           and CUtils.equal_ignore_case(metadata_data, 'pass') \
            and CUtils.equal_ignore_case(metadata_business, 'pass'):
            result = CResult.merge_result(self.Success, '数据的信息检查完成，可以发布服务')
            return result
        else:
            if not CUtils.equal_ignore_case(data, 'pass'):
                message = '影像文件异常，结果为{0}'.format(data)
            if not CUtils.equal_ignore_case(metadata_data, 'pass'):
                message = message + ',' + '影像元数据异常，结果为{0}'.format(metadata_data)
            if not CUtils.equal_ignore_case(metadata_business, 'pass'):
                message = message + ',' + '影像业务元数据异常，结果为{0}'.format(metadata_business)
            result = CResult.merge_result(self.Exception, '数据的信息检查完成，不可以发布服务，具体异常信息为{0}'.format(message))
            return result