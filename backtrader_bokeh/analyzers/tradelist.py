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

import backtrader as bt
class TradelistAnalyzer(bt.Analyzer):
    def get_analysis(self):
        return self.trades
    def __init__(self):
        self.trades = []
        self.cumprofit = 0.0
    def notify_trade(self, trade):
        if trade.isclosed:
            brokervalue = self.strategy.broker.getvalue()
            dir = 'short'
            if trade.history[0].event.size > 0: dir = 'long'
            pricein = trade.history[len(trade.history)-1].status.price
            priceout = trade.history[len(trade.history)-1].event.price
            datein = bt.num2date(trade.history[0].status.dt)
            dateout = bt.num2date(trade.history[len(trade.history)-1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                datein = datein.date()
                dateout = dateout.date()

            pcntchange = 100 * priceout / pricein - 100
            pnl = trade.history[len(trade.history)-1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue
            barlen = trade.history[len(trade.history)-1].status.barlen
            pbar = pnl / barlen
            self.cumprofit += pnl

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=barlen+1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen+1))
            hp = 100 * (highest_in_trade - pricein) / pricein
            lp = 100 * (lowest_in_trade - pricein) / pricein
            if dir == 'long':
                mfe = hp
                mae = lp
            if dir == 'short':
                mfe = -lp
                mae = -hp

            self.trades.append({'ref': trade.ref, 'ticker': trade.data._name, 'dir': dir,
                 'datein': datein, 'pricein': pricein, 'dateout': dateout, 'priceout': priceout,
                 'chng%': round(pcntchange, 2), 'pnl': pnl, 'pnl%': round(pnlpcnt, 2),
                 'size': size, 'value': value, 'cumpnl': self.cumprofit,
                 'nbars': barlen, 'pnl/bar': round(pbar, 2),
                 'mfe%': round(mfe, 2), 'mae%': round(mae, 2)})
