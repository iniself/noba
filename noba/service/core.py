#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/3/1  
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
import noba.snippet as snippet
from noba.ioc import Container

# p = snippet.here

@snippet.singletonDecorator
class Core(Container):
    def __init__(self, package_absolute_path=None, project_absolute_path=None, aliases=dict):
        super().__init__()
        self._project_absolute_path = project_absolute_path
        self._package_absolute_path = package_absolute_path

        if package_absolute_path and project_absolute_path:
            self._set_base_path(package_absolute_path, project_absolute_path)

        self._register_core_aliases(aliases)
        self._register_core_service_providers()

    def _set_base_path(self, package_absolute_path, project_absolute_path):
        self._package_absolute_path = (package_absolute_path).is_absolute() and self._check_absolute_path_else_return_relative_path(package_absolute_path)
        self._project_absolute_path = (project_absolute_path).is_absolute() and self._check_absolute_path_else_return_relative_path(project_absolute_path)
        self._bind_paths_in_core()
        return self

    def _check_absolute_path_else_return_relative_path(self, path):
        if not path.exists():
            raise FileExistsError("Check Your Config Path! ")
        return path

    def _bind_paths_in_core(self, path=''):
        self.instance('package.base.absolute.path', self._package_absolute_path)
        self.instance('package.config.absolute.path', self._package_absolute_path.joinpath("config"))
        self.instance('package.bootstrap.absolute.path', self._package_absolute_path.joinpath("bootstrap"))
        self.instance('package.provider.absolute.path', self._package_absolute_path.joinpath("provider"))

        self.instance('project.base.absolute.path', self._project_absolute_path)
        self.instance('project.config.absolute.path', self._project_absolute_path.joinpath("config"))
        self.instance('project.bootstrap.absolute.path', self._project_absolute_path.joinpath("bootstrap"))
        self.instance('project.provider.absolute.path', self._project_absolute_path.joinpath("provider"))
        self.instance('project.migrate.absolute.path', self._project_absolute_path.joinpath("migrate"))

        self.instance('package.config.module.path', "config")
        self.instance('project.config.module.path', "config")

    def _register_core_bindings(self):
        pass

    def _register_core_aliases(self, aliases):
        self.aliases = aliases

    def _register_core_service_providers(self):
        self.singleton('bb', lambda core: snippet.dyn_from_path_import("noba.service.backtest.bt"))
        self.singleton('bt', lambda core: snippet.import_module("backtrader"))

        self.instance('event', snippet.dyn_from_path_import("noba.service.event.EventHub"))

        self.instance('tools', snippet)

        self.instance('pd', snippet.import_module("pandas"))

    def bootstrap(self, bootstrappers):
        self._load_configuration()

        config = self.make('config')
        connector = config.get('db.connector')

        if connector and connector.lower() == 'csv':
            self.singleton('noba.service.abs.DBManagerAbs', 'noba.service.dber.CSV')
        elif connector and connector.lower() == 'xls':
            self.singleton('noba.service.abs.DBManagerAbs', 'noba.service.dber.XLS')
        else:
            self.singleton('noba.service.abs.DBManagerAbs', 'noba.service.dber.DBManager')

        if not bootstrappers:
            return

        for bootstrapper in bootstrappers:
            (self.make(bootstrapper)).bootstrap(self)

    def _load_configuration(self):
        self.make('config').load()