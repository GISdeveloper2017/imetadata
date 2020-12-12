# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:35 
# @Author : 王西亚 
# @File : c_mdExtractorVector.py
from tikapp import TikaApp as TikaApplication
from tika import parser as TikaServer
from imetadata import settings
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_result import CResult
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.parser.metadata.metadata.c_mdExtractorDocument import CMDExtractorDocument


class CMDExtractorDocument_Tika(CMDExtractorDocument):
    def process(self) -> str:
        """
        在这里提取文档数据的元数据, 将元数据文件存储在self.file_content.work_root_dir下, 固定名称为self.FileName_MetaData, 注意返回的串中有元数据的格式
        注意: 如果出现内存泄漏现象, 则使用新建进程提取元数据, 放置到文件中, 在本进程中解析元数据!!!
        :return:
        """
        default_result = super().process()
        out_metadata_file_fullname = CFile.join_file(self.file_content.work_root_dir, self.FileName_MetaData)
        in_file_fullname = self.file_info.file_name_with_full_path

        if not settings.application.xpath_one(self.Path_Setting_Dependence_Tika_Enable, True):
            return default_result

        tika_dependence_mode = settings.application.xpath_one(self.Path_Setting_Dependence_Tika_Mode, self.Name_Server)
        if CUtils.equal_ignore_case(tika_dependence_mode, self.Name_Server):
            tika_server_url = settings.application.xpath_one(self.Path_Setting_Dependence_Tika_Server_Url, None)
            tika_server_connect_timeout = settings.application.xpath_one(
                self.Path_Setting_Dependence_Tika_Server_Timeout, 30)
            if CUtils.equal_ignore_case(tika_server_url, ''):
                return default_result

            try:
                parsed = TikaServer.from_file(in_file_fullname, tika_server_url,
                                              requestOptions={'timeout': tika_server_connect_timeout})
                meta_data_dict = parsed["metadata"]
                json_obj = CJson()
                json_obj.load_obj(meta_data_dict)
                json_obj.to_file(out_metadata_file_fullname)
                return CResult.merge_result_info(
                    CResult.merge_result(
                        self.Success,
                        '文档[{0}]的元数据提取成功'.format(in_file_fullname)
                    ),
                    self.Name_Format,
                    self.MetaDataFormat_Json
                )
            except Exception as error:
                return CResult.merge_result(
                    self.Failure,
                    '文档[{0}]的元数据提取过程出现错误, 详细信息为: [{1}]'.format(
                        in_file_fullname, error.__str__()
                    )
                )
        else:
            tika_application = settings.application.xpath_one(self.Path_Setting_Dependence_Tika_Client_App, None)
            if CUtils.equal_ignore_case(tika_application, ''):
                return default_result

            if not CFile.file_or_path_exist(tika_application):
                return CResult.merge_result(
                    self.Failure,
                    '文档[{0}]的元数据无法提取, 详细原因为: [依赖中间件{1}文件不存在, 请修正后重试!]'.format(
                        in_file_fullname, tika_application
                    )
                )

            try:
                tika_client = TikaApplication(file_jar=tika_application)
                meta_data_dict = tika_client.extract_only_metadata(in_file_fullname)
                json_obj = CJson()
                json_obj.load_obj(meta_data_dict)
                json_obj.to_file(out_metadata_file_fullname)
                return CResult.merge_result_info(
                    CResult.merge_result(
                        self.Success,
                        '文档[{0}]的元数据提取成功'.format(in_file_fullname)
                    ),
                    self.Name_Format,
                    self.MetaDataFormat_Json
                )
            except Exception as error:
                return CResult.merge_result(
                    self.Failure,
                    '文档[{0}]的元数据提取过程出现错误, 详细信息为: [{1}]'.format(
                        in_file_fullname, error.__str__()
                    )
                )

        # result = raster_mdreader.get_metadata_2_file(out_metadata_file_fullname)
        # result = CProcessUtils.processing_method(raster_mdreader.get_metadata_2_file, out_metadata_file_fullname)
        # 进程调用模式
        # p_one = Process(target=raster_mdreader.get_metadata_2_file, args=(out_metadata_file_fullname,))
        # p_one.start()
        # p_one.join()
        return CResult.merge_result_info(result, self.Name_Format, self.MetaDataFormat_Json)
        # return CResult.merge_result_info(CResult.merge_result(self.Success, '处理完毕!'), self.Name_Format,
        #                                  self.MetaDataFormat_Text)
