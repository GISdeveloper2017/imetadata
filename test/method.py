# -*- coding: utf-8 -*-
# @Time : 2020/9/15 17:00
# @Author : 赵宇飞
# @File : method.py
from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_resource import CResource
from sortedcontainers import SortedList


class test_fei(CResource):
    def aa(self):
        dir = 'D:/data/0生态审计/少量数据测试_修改后'
        # file_ralationpath = '\\工业园区规划范围'
        file_ralationpath = '/工业园区规划范围'
        file_fullpath = CFile.join_file(dir, file_ralationpath)
        print(file_fullpath)

    def aa1(self, arr: []):
        arr.append(3)
        # pass

    def __file_or_dir_fullname_of_path_recurse(self, result_file_fullname_list:[], path: str, is_recurse_subpath: bool = False, match_str: str = '*',
                                             match_type: int = CFile.MatchType_Common):
        """
            私有方法，递归路径获取路径下的所有文件和文件夹的全文件名，仅供内部函数file_or_dir_fullname_of_path调用
        @param result_file_fullname_list:
        @param path:
        @param is_recurse_subpath:
        @param match_str:
        @param match_type:
        @return:
        """
        list_file_name = CFile.file_or_subpath_of_path(path, match_str, match_type)
        for file_name_temp in list_file_name:
            file_fullname_temp = CFile.join_file(path, file_name_temp)
            result_file_fullname_list.append(file_fullname_temp)
            if is_recurse_subpath:
                if CFile.is_dir(file_fullname_temp):
                    self.__file_or_dir_fullname_of_path_recurse(result_file_fullname_list,file_fullname_temp,is_recurse_subpath,match_str,match_type)

    def file_or_dir_fullname_of_path(self, path: str, is_recurse_subpath: bool = False, match_str: str = '*',
                                     match_type: int = CFile.MatchType_Common):
        """
            公共方法：根据路径获取文件和文件夹的全文件名，根据参数is_recurse_subpath支持是否递归子目录
        @param path:
        @param is_recurse_subpath:
        @param match_str:
        @param match_type:
        @return:
        """
        list_file_fullname = []
        if CFile.is_dir(path):
            self.__file_or_dir_fullname_of_path_recurse(list_file_fullname,path,is_recurse_subpath,match_str,match_type)
        return list_file_fullname


if __name__ == "__main__":
    # aa()
    arr_list = [1, 2]
    # arr_list = r''
    test_fei().aa1(arr_list)
    print(arr_list)

    query_object_fullname = r'D:\data\0生态审计\产品样例数据-昆明矢量\基础地理信息\县界'
    list_file_fullname = test_fei().file_or_dir_fullname_of_path(query_object_fullname, True)
    for file_name_temp in list_file_fullname:
        print(file_name_temp)
