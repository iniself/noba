#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2022/5/5  
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

import backtrader as bt
with_metaclass = bt.writer.with_metaclass
string_types = bt.writer.string_types
integer_types = bt.writer.integer_types
collections = bt.writer.collections

def writedict(self, dct, level=0, recurse=False):
    if not recurse:
        self.writelineseparator(level)

    indent0 = level * self.p.indent
    for key, val in dct.items():
        kline = ' ' * indent0
        if recurse:
            kline += '- '

        kline += str(key) + ':'

        try:
            sclass = issubclass(val, bt.LineSeries)
        except TypeError:
            sclass = False

        if sclass:
            kline += ' ' + val.__name__
            self.writeline(kline)
        elif isinstance(val, string_types):
            kline += ' ' + val
            self.writeline(kline)
        elif isinstance(val, integer_types):
            kline += ' ' + str(val)
            self.writeline(kline)
        elif isinstance(val, float):
            if self.p.rounding is not None:
                val = round(val, self.p.rounding)
            kline += ' ' + str(val)
            self.writeline(kline)
        elif isinstance(val, dict):
            if recurse:
                self.writelineseparator(level=level)
            self.writeline(kline)
            self.writedict(val, level=level + 1, recurse=True)
        elif isinstance(val, (list, tuple, collections.abc.Iterable)):
            line = ', '.join(map(str, val))
            self.writeline(kline + ' ' + line)
        else:
            kline += ' ' + str(val)
            self.writeline(kline)


bt.writer.WriterFile.writedict = writedict