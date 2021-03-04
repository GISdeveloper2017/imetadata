#!/usr/bin/python3
# -*- coding:utf-8 -*-


from __future__ import absolute_import

import logging

from imetadata.base.c_singleton import singleton


@singleton
class CLogger:
    def __init__(self):
        pass

    @staticmethod
    def debug(msg, *args, **kwargs):
        if len(logging.root.handlers) != 0:
            logging.debug(msg, args, kwargs)
        else:
            print('debug: ' + str(msg))

    @staticmethod
    def info(msg, *args, **kwargs):
        if len(logging.root.handlers) != 0:
            logging.info(msg, args, kwargs)
        else:
            print('info: ' + str(msg))

    @staticmethod
    def warning(msg, *args, **kwargs):
        if len(logging.root.handlers) != 0:
            logging.warning(msg, args, kwargs)
        else:
            print('warning: ' + str(msg))

    @staticmethod
    def critical(msg, *args, **kwargs):
        if len(logging.root.handlers) != 0:
            logging.critical(msg, args, kwargs)
        else:
            print('critical: ' + str(msg))

    @staticmethod
    def error(msg, *args, **kwargs):
        if len(logging.root.handlers) != 0:
            logging.error(msg, args, kwargs)
        else:
            print('error: ' + str(msg))
