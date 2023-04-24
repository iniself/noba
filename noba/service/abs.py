#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/2/10  
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

from abc import ABCMeta, abstractmethod
from functools import reduce

class ServiceProvider(object, metaclass=ABCMeta):
    @abstractmethod
    def register(self, core):
        pass

    def boot(self):
        pass

class DBService(object, metaclass=ABCMeta):
    @abstractmethod
    def go(self):
        pass

class ConfigAbs(object, metaclass=ABCMeta):
    def __init__(self, file_type):
        self._files: list = []
        self._content: list = []
        self._filter_type = file_type
        self.final = self.load()

    def _list_all_file_in_folder_with_file_type(self, folder, file_type):
        self._files = sorted(folder.glob(file_type))
        return self

    def _filter_file_type(self, file_type):
        pass

    def _merge(self, contents: list):
        return reduce(self.__merge, contents)

    def __merge(self, one ,two):
        if not one:
            return two

        for k in two:
            if k in one and isinstance(one[k], dict) and isinstance(two[k], dict):
                one[k] = self.__merge(one[k], two[k])
            elif(two[k] or (not two[k] and two[k] is None)):
                one[k] = two[k]
            # else:
            #     one[k] = two[k]
        return one

    @abstractmethod
    def load(self):
        pass



class ConfigManagerAbs(object, metaclass=ABCMeta):
    def __init__(self):
        self.item = dict()

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def get(self, key, default=None):
        pass


    def has(self, key):
        pass

    def get(self, key):
        pass

    @abstractmethod
    def all(self):
        pass


class DBManagerAbs(object, metaclass=ABCMeta):
    @abstractmethod
    def table(self):
        pass
