# -*- coding: utf-8 -*- 
# @Time : 2020/8/15 18:33 
# @Author : 王西亚 
# @File : test_dict.py

import multiprocessing

if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    demo1 = mgr.dict()
    demo1['a'] = 'bb'
    print("第一种情况：", end='')
    print(demo1)

    demo2 = mgr.dict()
    demo2['a'] = {}
    demo2['a']['b'] = 'cc'
    print("第二种情况：", end='')
    print(demo2)

    demo3 = mgr.dict()
    demo3.update({'a': 'b'})
    print("第三种情况：", end='')
    print(demo3)

    demo5 = mgr.dict()
    demo5['a'] = {}
    demo5['a'].update({'a': {'a': 'b'}})
    print("第五种情况：", end='')
    print(demo5)

    demo4 = mgr.dict()
    demo4.update({'a': {'a': {'a': 'b'}}})
    print("第四种情况：", end='')
    print(demo4)

    demo6 = mgr.dict()
    demo6.update({'a': {'a': {'a': 'b'}}, 'b': {}})
    demo6.update({'b': {'a': 'b'}, 'c': {'a1': 'b1'}})
    demo6.pop('b')
    print("第六种情况：", end='')
    print(demo6)
