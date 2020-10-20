# -*- coding: utf-8 -*- 
# @Time : 2020/10/6 10:46 
# @Author : 王西亚 
# @File : c_time.py
import datetime


class CTime:
    @classmethod
    def now(cls):
        return datetime.datetime.now()

    @classmethod
    def today(cls):
        return datetime.datetime.today()

    @classmethod
    def from_datetime_str(cls, date_time_str: str, datetime_format: str = '%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.strptime(date_time_str, datetime_format)

    @classmethod
    def format_str(cls, date_time_value: datetime, datetime_format: str):
        return date_time_value.strftime(datetime_format)


if __name__ == '__main__':
    date_str = '2020-10-20 13:09:05'
    date_value = CTime.from_datetime_str(date_str, '%Y-%m-%d %H:%M:%S')
    print(CTime.format_str(date_value, '%Y-%m %H:%M'))
