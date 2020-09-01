#!/usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import absolute_import
import os


class CFile:
    def __init__(self):
        pass

    @classmethod
    def file_name(cls, file_name) -> str:
        return os.path.basename(file_name)

    @classmethod
    def file_main_name(cls, file_name, file_ext_whitelist=None):
        filename = cls.file_name(file_name)

        if file_ext_whitelist is None:
            file_info = os.path.splitext(filename)
            return file_info[0]
        else:
            return ''


