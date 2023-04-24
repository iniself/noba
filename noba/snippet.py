#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/2/12  
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function, unicode_literals)

import inspect, importlib, threading, os, json, pprint, re

DIRECTORY_SEPARATOR =  os.sep

def has_key(obj, k):
    o = obj
    arr = k.split('.')
    for one in arr:
        if (hasattr(o, '__iter__')  and (not one in o)) or not hasattr(o, '__iter__'):
            return False
        else:
            o = o[one]
    return True

def get_value(obj, k, default= None):
    o = obj
    arr = k.split('.')
    for one in arr:
        if (hasattr(o, '__iter__')  and (not one in o)) or not hasattr(o, '__iter__'):
            return default
        else:
            o = o[one]
    return o

def set_value(obj, k, value):
    o = obj
    arr = k.split('.')

    for one in arr:
        if (hasattr(o, '__iter__')  and (not one in o)) or not hasattr(o, '__iter__'):
            return None
        else:
            if one == arr[-1]:
                o[one] = value
            o = o[one]
    return {k:o}


def get_class_by_name(cls):
    try:
        return globals()[cls]
    except KeyError:
        return cls

def is_list(arg):
    return isinstance(arg, list)

def is_dict(arg):
    return isinstance(arg, dict)

def is_class(some):
    return inspect.isclass(some)


def is_str(some):
    return isinstance(some, str)

def is_number(some):
    if re.match(r'^[-+]?\d+(\.\d+)?$', some):
        return True
    return False


def is_function(some):
    return inspect.isfunction(some)

def is_all_empty(lst):
    if not isinstance(lst, list):
        return False
    elif len(lst) == 0:
        return True
    else:
        return all(is_all_empty(elem) for elem in lst)

def get_key_by_value(my_dict, value):
    return [k for k, v in my_dict.items() if v == value]

def singletonDecorator(cls, *args, **kwargs):
    instance = {}

    def wrapperSingleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return wrapperSingleton

class DefaultMethodDecorator(object):
    def __init__(self, fun):
        fun.__getattr__ = lambda self,key: self.default(key)
        self.__fun = fun

    def __call__(self):
        obj = self.__fun()
        return obj

def import_module(mod):
    return importlib.import_module(mod)

def dyn_from_import(mod: str, cls: str):
    import_modual = import_module(mod)
    return getattr(import_modual, cls)

def dyn_from_path_import(path: str):
    import_modual = import_module('.'.join(path.split(".")[:-1]))
    return getattr(import_modual, path.split(".")[-1])

def delay(cbname,delay,*argments):
    threading.Timer(delay,cbname,argments).start()


def load_json_file_if_not_exist_return_empty_dict(file, *args, **kwargs):
    try:
        with open(file, "r", encoding='utf-8') as f:
            json_text = f.read()
        jsontodict = json.loads(json_text, *args, **kwargs)
        return jsontodict
    except FileNotFoundError as e:
        return dict()

try:
    from shutil import copyfile
except ImportError:
    def copyfile(src, dst):
        with open(src,'r', encoding='utf-8') as fr:
            content = fr.read()
        with open(dst,'w', encoding='utf-8') as fw:
            fw.write(content)

def write_config_to_json_file(file, config_dict):
    config_json = json.dumps(config_dict, indent=4)
    with open(file, "w", encoding='utf-8') as f:
        f.write(config_json)

def here(something, do_print=True):
    '''Get the current file and line number in Python script.'''
    frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
    if do_print:
        print(f"{frameinfo.filename.split(DIRECTORY_SEPARATOR)[-1]}, {frameinfo.lineno}: ")
        pprint.pprint(something)
        print("\r\n")