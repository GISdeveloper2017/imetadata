#!/usr/bin/python3
# -*- coding:utf-8 -*-


class ConfigNotExistException(Exception):
    def __init__(self, file_name):
        self.__file_name__ = file_name

    def __str__(self):
        print("配置文件[{}]不存在, 系统无法运行! ".format(self.__file_name__))


class BusinessNotExistException(Exception):
    def __init__(self, type, message):
        self.__message__ = message
        self.__type__ = type

    def __str__(self):
        print("无法找到您需要的类型为[{0}]的类[{1}]! ".format(self.__type__, self.__message__))


class DBException(Exception):
    def __init__(self, db_id):
        self.__db_id__ = db_id

    def __str__(self):
        print("标示为[%s]的数据库不存在, 系统无法运行! ".format(self.__db_id__))


class DBLinkException(DBException):
    def __str__(self):
        print("标示为[%s]的数据库连接失败, 请检查数据库连接参数是否正确! " % self.__db_id__)


class DBSQLExecuteException(DBException):
    def __init__(self, db_id, sql):
        super().__init__(db_id)
        self.__sql__ = sql

    def __str__(self):
        print("标示为[%s]的数据库运行[%s]连接失败, 请检查数据库连接参数是否正确! " % self.__db_id__, self.__sql__)


class FileContentWapperNotExistException(Exception):
    pass


class FileException(Exception):
    __file_name__: None

    def __init__(self, file_name):
        super().__init__()
        self.__file_name__ = file_name


class ZipFileCanNotOpenException(FileException):
    def __str__(self):
        print("压缩文件[%s]无法打开!" % self.__file_name__)


class PathNotCreateException(FileException):
    def __str__(self):
        print("目录[%s]无法创建!" % self.__file_name__)


class FileCanNotOpenException(FileException):
    def __str__(self):
        print("数据文件[%s]无法打开!" % self.__file_name__)
