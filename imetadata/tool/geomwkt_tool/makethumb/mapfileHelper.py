# coding:utf-8
'''
@Author: zhangxx
@Date: 2020-02-19 14:14:42
@LastEditors: zhangxx
@LastEditTime: 2020-03-04 14:44:32
@Description: a python class to handle MapServer mapfile
'''

import re
import sys
from collections import OrderedDict

PY3 = sys.version_info[0] >= 3
if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

LINESEP = '\n'
LINETAB = '  '
SIMPLE_TYPES = (str if PY3 else basestring, int, float, type(None))
COMPLEX_TYPES = (list, dict)
DICT_KEYWORDS = ("MAP", "MAP.LAYER", "MAP.SYMBOL", "MAP.LAYER.CLASS", 
    "MAP.LAYER.CLUSTER", "MAP.LAYER.CLASS.STYLE", "MAP.LAYER.CLASS.LABEL", 
    "MAP.LAYER.CLASS.LABEL.STYLE", "MAP.LAYER.CLASS.LEADER", 
    "MAP.LAYER.CLASS.METADATA", "MAP.LAYER.CLASS.LEADER.STYLE", "MAP.PROJECTION", 
    "MAP.LAYER.PROJECTION", "MAP.LAYER.FEATURE", "MAP.LAYER.GRID", 
    "MAP.LAYER.JOIN", "MAP.OUTPUTFORMAT", "MAP.WEB.METADATA", "MAP.LAYER.METADATA",
    "MAP.LEGEND", "MAP.LEGEND.LABEL", "MAP.QUERYMAP", "MAP.SCALEBAR", 
    "MAP.SCALEBAR.LABEL", "MAP.WEB", "MAP.REFERENCE")
LAYER_KEYWORDS = ["LAYER", "CLASS"]
PROCESSING_KEYWORDS = ("PROCESSING")
PROJ_KEYWORDS = ("MAP.PROJECTION","MAP.LAYER.PROJECTION")

class MapfileHelper(object):

    def __init__(self):
        self._mapfile = OrderedDict()
            
    def loads(self, file_path):
        path = ''
        key = ''
        fobj = open(file_path)
        mapline = fobj.readline()
        while(mapline):
            if '#' in mapline and (mapline[mapline.index('#')-1] != '"' and mapline.index('#') > 0):
                mapline = mapline[:mapline.index('#')]
            mapline = mapline.strip()
            values = mapline.split()
            
            if len(values) > 0:
                key = values[0]
            else:
                mapline = fobj.readline()
                continue
            
            key = key.upper()
            if(key if len(path)==0 else dellistsign(path)+'.'+key in DICT_KEYWORDS):
                path = key if len(path)==0 else path+'.'+key
                model_path = dellistsign(path)
                if model_path in PROJ_KEYWORDS:
                    self.setvalue(path, [])
                elif key in LAYER_KEYWORDS:
                    try:
                        lyr_count = len(self.getvalue(path))
                    except Exception:
                        self.setvalue(path, [])
                        lyr_count = 0

                    path = path + '.' +str(lyr_count)
                    self.setvalue(path, OrderedDict())
                else:
                    self.setvalue(path, OrderedDict())
            elif(key == 'END'):
                if(path == 'MAP'):
                    break
                path = path[:path.rindex('.')]
                if '.' in path and path[path.rindex('.') + 1:] in LAYER_KEYWORDS:
                    path = path[:path.rindex('.')]
            elif (key in PROCESSING_KEYWORDS):
                try:
                    pcs_count = len(self.getvalue(path+'.'+key))
                except Exception:
                    self.setvalue(path+'.'+key, [])
                    pcs_count = 0
                    
                self.setvalue(path+'.'+key+'.'+str(pcs_count), mapline[len(key):])

            elif dellistsign(path) in PROJ_KEYWORDS:
                self.setvalue(path + '.99', key)
            else:
                self.setvalue(path + '.' + key, mapline[len(key):])

            mapline = fobj.readline()
            

    def dumps(self, file_path):
        path = 'MAP'
        key = 'MAP'
        fobj = open(file_path, 'w')

        fobj.writelines(key + LINESEP)
        self.dump(path, fobj)
        fobj.writelines('END')
        fobj.flush()
        fobj.close()

    def getvalue(self, nodename):
        return mget(self._mapfile, nodename)    

    def setvalue(self, nodename, val):
        mset(self._mapfile, nodename, val)

    def delnode(self, nodename):
        pass 

    def dump(self, map_path, map_fobj):
        # print(map_path)
        for map_key in self.getvalue(map_path):

            if map_key in PROCESSING_KEYWORDS:
                for word in self.getvalue(map_path+'.'+map_key):
                    map_fobj.writelines(u'{0}{1} {2}{3}'.format(self.getlinetab(map_path), map_key, \
                        word, LINESEP))
            
            elif dellistsign(map_path+'.'+map_key) in PROJ_KEYWORDS:
                map_fobj.writelines(self.getlinetab(map_path) + map_key + LINESEP)
                
                for prj in self.getvalue(map_path + '.' + map_key).split():
                    map_fobj.writelines(self.getlinetab(map_path + '.') + prj + LINESEP)
                
                map_fobj.writelines(self.getlinetab(map_path) + 'END' + LINESEP)
            
            elif map_key in LAYER_KEYWORDS:
                lyr_index = 0
                for lyr_def in self.getvalue(map_path + '.' + map_key):
                    map_fobj.writelines(self.getlinetab(map_path) + map_key + LINESEP)
                    self.dump(map_path+'.'+map_key+'.'+str(lyr_index), map_fobj)
                    lyr_index += 1
                    map_fobj.writelines(self.getlinetab(map_path) + 'END' + LINESEP)

            elif isinstance(self.getvalue(map_path + '.' + map_key), SIMPLE_TYPES):
                map_fobj.writelines('{0}{1} {2}{3}'.format(self.getlinetab(map_path), map_key, \
                                    self.getvalue(map_path + '.' + map_key), LINESEP))

            else:
                map_fobj.writelines(self.getlinetab(map_path) + map_key + LINESEP)
                self.dump(map_path+'.'+map_key, map_fobj)
                map_fobj.writelines(self.getlinetab(map_path) + 'END' + LINESEP)

    def getlinetab(self, path):
        return (path.count('.')+1) * LINETAB
        
    
def dellistsign(nodename):
    '''return the nodename that delete list index parts
        >>> dellistsign('map.layer.0.projection')
        map.layer.projection
    '''
    return ''.join(re.split('\.\d+', nodename))

def tokenize(s):
    r"""Returns an iterable through all subparts of string splitted by '.'

    So:

        >>> list(tokenize('foo.bar.wiz'))
        ['foo', 'bar', 'wiz']
    """
    if s is None:
        return
    return s.split('.')
    '''
    tokens = (re.sub(r'\\(\\|\.)', r'\1', m.group(0))
            for m in re.finditer(r'((\\.|[^.\\])*)', s))
    ## an empty string superfluous token is added after all non-empty token
    for token in tokens:
        if len(token) != 0:
            next(tokens)
        yield token
    '''

def mget(dct, key):
        return aget(dct, tokenize(key))

def mset(dct, key, val):
    aset(dct, tokenize(key), val)

def aget(dct, key):
    r"""Allow to get values deep in a dict with iterable keys

    Accessing leaf values is quite straightforward:

        >>> dct = {'a': {'x': 1, 'b': {'c': 2}}}
        >>> aget(dct, ('a', 'x'))
        1
        >>> aget(dct, ('a', 'b', 'c'))
        2

    If key is empty, it returns unchanged the ``dct`` value.

        >>> aget({'x': 1}, ())
        {'x': 1}

    """
    key = iter(key)
    try:
        head = next(key)
    except StopIteration:
        return dct

    if isinstance(dct, list):
        try:
            idx = int(head)
        except ValueError:
            raise Exception(
                "non-integer index %r provided on a list."
                % head)
        try:
            value = dct[idx]
        except IndexError:
            raise Exception(
                "index %d is out of range (%d elements in list)."
                % (idx, len(dct)))
    else:
        try:
            value = dct[head]

        except KeyError:
            ## Replace with a more informative KeyError
            raise KeyError(
                "missing key %r in dict."
                % (head, ))
        except Exception:
            raise Exception(
                "can't query subvalue %r of a leaf%s."
                % (head, dct))
    return aget(value, key)

def aset(dct, key, val):
    idx = -1

    if len(key) == 1:
        head = key.pop()
        if isinstance(dct, list):
            try:
                idx = int(head)
            except ValueError:
                raise TypeError(
                    "non-integer index %r provided on a list1." % head)
            if abs(idx) < len(dct):
                dct[idx] = val
            else:
                dct.append(val)
        else:
            dct[head] = val
    else:
        head = key.pop(0)
        if isinstance(dct, list):
            try:
                idx = int(head)
            except ValueError:
                raise Exception(
            "non-integer index %r provided on a list2." % head
            )
            aset(dct[idx], key, val)
        else:
            aset(dct[head], key, val)