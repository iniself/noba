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

@staticmethod
def iterize(iterable):
    '''Handy function which turns things into things that can be iterated upon
    including iterables
    '''
    try:
        collectionsAbc = bt.collections.abc
    except AttributeError:
        collectionsAbc = bt.collections

    niterable = list()
    for elem in iterable:
        if isinstance(elem, bt.string_types):
            elem = (elem,)
        elif not isinstance(elem, collectionsAbc.Iterable):
            elem = (elem,)

        niterable.append(elem)

    return niterable


def p(self, plotter=None, numfigs=1, iplot=True, start=None, end=None,
         width=16, height=9, dpi=300, tight=True, use=None,
         **kwargs):
    if self._exactbars > 0:
        return

    if not plotter:
        plot = bt.plot
        if self.p.oldsync:
            plotter = plot.Plot_OldSync(**kwargs)
        else:
            plotter = plot.Plot(**kwargs)

    figs = []
    for stratlist in self.runstrats:
        for si, strat in enumerate(stratlist):
            rfig = plotter.plot(strat, figid=si * 100,
                                numfigs=numfigs, iplot=iplot,
                                start=start, end=end, use=use)
            # pfillers=pfillers2)

            figs.append(rfig)

        plotter.show()

    return figs

bt.cerebro.Cerebro.iterize = iterize
bt.cerebro.Cerebro.plot = p