#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import uuid


class MetaDataUtils:
    Success = -1
    Failure = 0
    Exception = 1

    @classmethod
    def merge_result(cls, result, message=None, base=None) -> str:
        new_result = json.loads('{}')
        if base is not None:
            new_result = json.loads(base)
        new_result['result'] = result
        if message is not None:
            new_result['message'] = message
        return json.dumps(new_result)

    @classmethod
    def result_success(cls, text) -> bool:
        result = json.loads(text)
        return result['result'] == MetaDataUtils.Success

    @classmethod
    def one_id(cls) -> str:
        name = 'metadata.org'
        uuid_text = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid4())))
        uuid_text = uuid_text.replace('-', '')
        return uuid_text

    @classmethod
    def equal_ignore_case(cls, str1: str, str2: str) -> bool:
        return str1.strip().lower() == str2.strip().lower()
