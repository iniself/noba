#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2022/5/31  
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


from ..helper.datatable import ColummDataType


def datatable(self):
    cols1 = [['ticker', ColummDataType.STRING], ['chng%', ColummDataType.PERCENTAGE], ['cumpnl', ColummDataType.FLOAT], ['datein', ColummDataType.STRING], ['dateout', ColummDataType.STRING], ['dir', ColummDataType.STRING], ['mae%', ColummDataType.PERCENTAGE], ['mfe%', ColummDataType.PERCENTAGE], ['nbars', ColummDataType.INT], ['pnl%', ColummDataType.PERCENTAGE], ['pnl', ColummDataType.FLOAT], ['pnl/bar', ColummDataType.FLOAT], ['pricein', ColummDataType.FLOAT], ['priceout', ColummDataType.FLOAT], ['ref', ColummDataType.INT], ['size', ColummDataType.INT],  ['value', ColummDataType.FLOAT]]
    cols = []
    a = self.get_analysis()
    for one in a:
        cols1[0].append(one['ticker'])
        cols1[1].append(one['chng%']/100)
        cols1[2].append(one['cumpnl'])
        cols1[3].append(one['datein'])
        cols1[4].append(one['dateout'])
        cols1[5].append(one['dir'])
        cols1[6].append(one['mae%']/100)
        cols1[7].append(one['mfe%']/100)
        cols1[8].append(one['nbars'])
        cols1[9].append(one['pnl%']/100)
        cols1[10].append(one['pnl'])
        cols1[11].append(one['pnl/bar'])
        cols1[12].append(one['pricein'])
        cols1[13].append(one['priceout'])
        cols1[14].append(one['ref'])
        cols1[15].append(one['size'])
        cols1[16].append(one['value'])
        cols.append(cols1)
    return 'Trade List', cols
