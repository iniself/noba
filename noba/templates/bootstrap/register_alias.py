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

from functools import reduce

class RegisterAlias():
    def bootstrap(self, core):
        user_alias = core.make("config").get("aliases")
        if not user_alias:
            return

        package_aliase = core.aliases
        core.aliases = reduce(self.__merge, [package_aliase, user_alias])

    def __merge(self, package_aliase, user_alias):
        if not package_aliase:
            return user_alias

        for k in user_alias:
            if k in package_aliase and isinstance(package_aliase[k], dict) and isinstance(user_alias[k], dict):
                package_aliase[k] = self.__merge(package_aliase[k], user_alias[k])
            elif(user_alias[k] or (not user_alias[k] and user_alias[k] is None)):
                package_aliase[k] = user_alias[k]
        return package_aliase