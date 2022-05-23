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
import numbers
Order = bt.brokers.bbroker.Order

def set_rule(self, p):
    self.p.rule = p

def _is_daily_limit(isbuy, issell, phigh, plow, pre_close, limit):
    if (pre_close == None) and ((phigh - plow) < 0.02):
        return True
    elif isbuy and ((plow > pre_close * (1 + limit) - 0.01) or ((phigh - plow) < 0.02)):
        return True
    elif issell and phigh < pre_close * (1 - limit) + 0.01:
        return True
    return False

def _is_number(num):
    return isinstance(num, numbers.Number) and type(num)!=bool

def _check_sell_size(size,sized):
    return max(size,-sized)

def _check_rule_attr(self,attr):
    return  hasattr(self.p, 'rule') and type(self.p.rule) == dict and attr in self.p.rule

def check_submitted(self):
    cash = self.cash
    positions = dict()
    while self.submitted:
        order = self.submitted.popleft()
        if self._take_children(order) is None:  # children not taken
            continue
        comminfo = self.getcommissioninfo(order.data)
        position = positions.setdefault(
            order.data, self.positions[order.data].clone())
        # can sell
        if order.issell() and not (self.p.rule['short'] if _check_rule_attr(self,'short') else True):
            order.executed.remsize = _check_sell_size(order.executed.remsize,self.getposition(order.data).size)
            if order.executed.remsize == 0:
                order.reject()
                self.notify(order)
                return
        # least
        if (True if (_check_rule_attr(self, 'least') and order.isbuy() and _is_number(self.p.rule['least'])) else False):
            order.executed.remsize = order.executed.remsize // self.p.rule['least'] * self.p.rule['least']
            if order.executed.remsize == 0:
                order.reject()
                self.notify(order)
                return

        # pseudo-execute the order to get the remaining cash after exec
        cash = self._execute(order, cash=cash, position=position)
        if cash >= 0.0:
            self.submit_accept(order)
            continue
        order.margin()
        self.notify(order)
        self._ococheck(order)
        self._bracketize(order, cancel=True)    


def _try_exec(self, order):
    data = order.data
    popen = getattr(data, 'tick_open', None)
    if popen is None:
        popen = data.open[0]
    phigh = getattr(data, 'tick_high', None)
    if phigh is None:
        phigh = data.high[0]
    plow = getattr(data, 'tick_low', None)
    if plow is None:
        plow = data.low[0]
    pclose = getattr(data, 'tick_close', None)
    if pclose is None:
        pclose = data.close[0]

    pcreated = order.created.price

    if order.data == 1:
        pre_close = None
    else:
        pre_close = order.data.close[-1]

    plimit = order.created.pricelimit

    if (self.p.rule['limit'] if _check_rule_attr(self,'limit') else False) and _is_number(self.p.rule['limit']) and _is_daily_limit(isbuy=order.isbuy(), issell=order.issell(), phigh=phigh, plow=plow, pre_close=pre_close, limit=self.p.rule['limit']):
        return

    if order.exectype == Order.Market:
        self._try_exec_market(order, popen, phigh, plow)

    elif order.exectype == Order.Close:
        self._try_exec_close(order, pclose)

    elif order.exectype == Order.Limit:
        self._try_exec_limit(order, popen, phigh, plow, pcreated)

    elif (order.triggered and
          order.exectype in [Order.StopLimit, Order.StopTrailLimit]):
        self._try_exec_limit(order, popen, phigh, plow, plimit)

    elif order.exectype in [Order.Stop, Order.StopTrail]:
        self._try_exec_stop(order, popen, phigh, plow, pcreated, pclose)

    elif order.exectype in [Order.StopLimit, Order.StopTrailLimit]:
        self._try_exec_stoplimit(order,
                                 popen, phigh, plow, pclose,
                                 pcreated, plimit)

    elif order.exectype == Order.Historical:
        self._try_exec_historical(order)


bt.brokers.bbroker.BackBroker._try_exec = _try_exec
bt.brokers.bbroker.BackBroker.check_submitted = check_submitted
bt.brokers.bbroker.BackBroker.set_rule = set_rule