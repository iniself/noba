# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/2/2
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


from noba.snippet import *

__all__ = ['Container', 'container']


class Container(object):
    """
    ioc ioccontainer
    """
    def __init__(self):
        self._binds = dict()
        self._instances = dict()
        self._with = list()
        self.aliases = dict()

    def __getitem__(self, item):
        return self.make(item)

    def __call__(self, abstract=None, parameters=[]):
        return self.make(abstract, parameters)

    def instance(self, abstract, instance):
        self._instances[abstract] = instance
        return instance

    def singleton(self, abstract, concrete=None):
        self.bind(abstract, concrete, True)

    def bind(self, abstract, concrete=None, shared=False):
        if not is_function(concrete):
            concrete = self.get_function(abstract, concrete)

        self._binds[abstract] = {
            'concrete': concrete,
            'shared': shared,
        }

    def bound(self, abstract):
        return (abstract in self._binds) or (abstract in self._instances)

    def get_function(self, abstract, concrete):
        def doit(container, parameters=[]):
            if abstract == concrete:
                return container.build(concrete);
            else:
                return container.make(concrete, parameters)
        return doit

    def make_with(self, abstract, parameters = []):
        return self.make(abstract, parameters);

    def make(self, abstract, parameters = []):
        is_alias = not is_list(abstract) and abstract in self.aliases
        abstract = self.get_alias(abstract)
        is_share_in_alias = False

        if is_alias:
            is_share_in_alias = True
        if is_list(abstract):
            abstract, is_share_in_alias = abstract

        needsContextualBuild = not (not parameters);
        isclass = False
        if is_class(abstract):
            abstract_cls = abstract
            package_name = abstract.__module__
            abstract = package_name + "." + abstract.__name__
            isclass = True

        # if singleton, return obj directly
        if (abstract in self._instances) and (not needsContextualBuild):
            return self._instances[abstract]

        parameters and (self._with).append(parameters)

        concrete = self.get_concrete(abstract, abstract_cls if isclass else None)

        if self.is_buildable(concrete, abstract):
            obj = self.build(concrete)
        else:
            obj = self.make(concrete)

        if self.is_shared(abstract, is_share_in_alias):
            self._instances[abstract] = obj

        return obj

    def is_buildable(self, concrete, abstract):
        return  (concrete == abstract) or is_function(concrete)

    def get_concrete(self, abstract, abstract_cls):
        if abstract in self._binds:
            return self._binds[abstract]['concrete']

        if abstract_cls:
            for b in self._binds:
                if "." in b:
                    m = dyn_from_path_import(b)
                    if m == abstract_cls:
                        return self._binds[b]['concrete']

        return abstract

    def build(self, concrete):
        if is_function(concrete):
            if concrete.__name__ == "__init__":
                Last_parameter = self.get_Last_parameter_override()
                return concrete(self, Last_parameter)
            else:
                return concrete(self)

        if is_class(concrete):
            reflector = concrete
        elif is_str(concrete):
            reflector = self.get_class_by_name(concrete)
        else:
            raise TypeError(f"build need str or class, but {type(concrete)} were given")

        init_fun = reflector.__init__

        if not is_function(init_fun):
            return reflector()

        init_param = inspect.signature(reflector.__init__).parameters.values()
        dependencies: list = self.get_dependencies(init_param)
        if reflector.__name__ == 'ABCMeta':
            raise TypeError("")

        # if dependencies is empty，ignore it
        if is_all_empty(dependencies):
            return reflector()
        else:
            return reflector(*dependencies)

    def get_Last_parameter_override(self):
        last_with = (self._with.pop()) if (self._with) else  []
        return last_with


    def get_class_by_name(self, cls):
        try:
            return dyn_from_path_import(cls)
        except KeyError:
            return cls

    def get_alias(self, abstract):
        return self.get_alias(self.aliases[abstract]) if (not is_list(abstract) and abstract in self.aliases) else abstract

    def is_shared(self, abstract, is_share_in_alias):
        return (abstract in self._instances) or (is_share_in_alias) or (abstract in self._binds and self._binds[abstract]['shared'])

    def get_dependencies(self, parameters):
        dependencies = []
        for param in  list(parameters)[1:]:
            if not param.annotation is inspect._empty:
                if None:
                    dependencies.append(None)
                else:
                    dependencies.append(self.resolve_class(param.annotation))
            else:
                dependencies.append(self.get_Last_parameter_override())
        return dependencies

    def resolve_class(self, parameter):
        return self.make(parameter)

    def get_bindings(self):
        return self._binds

container = Container()