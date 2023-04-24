#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/2/15  
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

from .abs import ConfigAbs, ConfigManagerAbs
from noba.snippet import is_list, get_value, set_value ,dyn_from_path_import, load_json_file_if_not_exist_return_empty_dict, DIRECTORY_SEPARATOR, singletonDecorator
from noba.Core import core

class PackageMainConfig(ConfigAbs):
    def __init__(self):
        super(PackageMainConfig, self).__init__("*.json")

    def load(self):
        path = core('package.config.absolute.path')
        self._list_all_file_in_folder_with_file_type(path, self._filter_type)
        self._content = [load_json_file_if_not_exist_return_empty_dict(file)  for file in self._files]
        return self._content and self._merge(self._content)

class ProjectMainConfig(ConfigAbs):
    def __init__(self):
        super(ProjectMainConfig, self).__init__("*.json")

    def load(self):
        path = core('project.config.absolute.path')
        self._list_all_file_in_folder_with_file_type(path, self._filter_type)
        self._content = [load_json_file_if_not_exist_return_empty_dict(file)  for file in self._files]
        return self._content and self._merge(self._content)

class ConfigManager(ConfigAbs):
    def __init__(self, package: PackageMainConfig, project: ProjectMainConfig):
        self._package = package
        self._project = project
        self.final = self.load()

    def __getattr__(self, item):
        return self.get(item, None)

    def load(self):
        return self._merge([self._package.final, self._project.final])

    def all(self):
        return self.final

    def get(self, key, default=None):
        return get_value(self.final, key, default)

    def get_many(self, key, default=None):
        config = dict()
        if not is_list(key):
            return self.get(key, default)
        for one in key:
            config[one] = self.get(one, default)
        return config


    def set(self, key, value):
        return set_value(self.final, key, value)
