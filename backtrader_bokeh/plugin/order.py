#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2022/5/22  
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
Order = bt.order.Order

def getremsize(self):
    return self.executed.remsize or self.executed.size or self.size

def __str__(self):
    tojoin = list()
    tojoin.append('Ref: {}'.format(self.ref))
    tojoin.append('OrdType: {}'.format(self.ordtype))
    tojoin.append('OrdType: {}'.format(self.ordtypename()))
    tojoin.append('Status: {}'.format(self.status))
    tojoin.append('Status: {}'.format(self.getstatusname()))
    tojoin.append('Org Size: {}'.format(self.size))
    tojoin.append('Adj Size: {}'.format(self.getremsize()))
    tojoin.append('Price: {}'.format(self.price))
    tojoin.append('Price Limit: {}'.format(self.pricelimit))
    tojoin.append('TrailAmount: {}'.format(self.trailamount))
    tojoin.append('TrailPercent: {}'.format(self.trailpercent))
    tojoin.append('ExecType: {}'.format(self.exectype))
    tojoin.append('ExecType: {}'.format(self.getordername()))
    tojoin.append('CommInfo: {}'.format(self.comminfo))
    tojoin.append('End of Session: {}'.format(self.dteos))
    tojoin.append('Info: {}'.format(self.info))
    tojoin.append('Broker: {}'.format(self.broker))
    tojoin.append('Alive: {}'.format(self.alive()))
    return '\n'.join(tojoin)

def expire(self):
    if self.valid and self.data.datetime[0] > self.valid:
        self.status = Order.Expired
        self.executed.dt = self.data.datetime[0]
        return True

    return False


bt.order.Order.expire = expire
bt.order.OrderBase.__str__ = __str__
bt.order.OrderBase.getremsize = getremsize