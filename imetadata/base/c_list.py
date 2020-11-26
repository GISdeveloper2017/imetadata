# -*- coding: utf-8 -*- 
# @Time : 2020/11/23 21:12 
# @Author : 王西亚 
# @File : c_list.py


class CList:
    @property
    def list(self):
        return self.__inner_list

    def __init__(self):
        self.__inner_list = list()

    def add(self, obj) -> bool:
        if obj is not None:
            self.list.append(obj)
            return True
        else:
            return False

    def delete(self, index: int):
        if 0 <= index <= len(self.__inner_list):
            del self.__inner_list[index]

    def clear(self):
        self.__inner_list.clear()

    def size(self):
        return len(self.__inner_list)

    def item_by_index(self, index: int):
        if 0 <= index <= len(self.__inner_list):
            return self.__inner_list[index]
        else:
            return None
