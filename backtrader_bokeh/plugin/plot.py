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

import backtrader.plot.plot as plot
sys = plot.sys
matplotlib = plot.matplotlib
datetime = plot.datetime
bisect = plot.bisect


PInfo = plot.PInfo
MultiCursor = plot.MultiCursor
date2num = plot.date2num


def p(self, strategy, figid=0, numfigs=1, iplot=True,
         start=None, end=None, **kwargs):
    if not strategy.datas:
        return

    if not len(strategy):
        return

    if iplot:
        if 'ipykernel' in sys.modules:
            matplotlib.use('nbagg')

    # this import must not happen before matplotlib.use
    import matplotlib.pyplot as mpyplot
    self.mpyplot = mpyplot

    self.pinf = PInfo(self.p.scheme)
    self.sortdataindicators(strategy)
    self.calcrows(strategy)

    st_dtime = strategy.lines.datetime.plot()
    if start is None:
        start = 0
    if end is None:
        end = len(st_dtime)

    if isinstance(start, datetime.date):
        start = bisect.bisect_left(st_dtime, date2num(start))

    if isinstance(end, datetime.date):
        end = bisect.bisect_right(st_dtime, date2num(end))

    if end < 0:
        end = len(st_dtime) + 1 + end  # -1 =  len() -2 = len() - 1

    slen = len(st_dtime[start:end])
    d, m = divmod(slen, numfigs)
    pranges = list()
    for i in range(numfigs):
        a = d * i + start
        if i == (numfigs - 1):
            d += m  # add remainder to last stint
        b = a + d

        pranges.append([a, b, d])

    figs = []

    for numfig in range(numfigs):
        # prepare a figure
        fig = self.pinf.newfig(figid, numfig, self.mpyplot)
        figs.append(fig)

        self.pinf.pstart, self.pinf.pend, self.pinf.psize = pranges[numfig]
        self.pinf.xstart = self.pinf.pstart
        self.pinf.xend = self.pinf.pend

        self.pinf.clock = strategy
        self.pinf.xreal = self.pinf.clock.datetime.plot(
            self.pinf.pstart, self.pinf.psize)
        self.pinf.xlen = len(self.pinf.xreal)
        self.pinf.x = list(range(self.pinf.xlen))
        # self.pinf.pfillers = {None: []}
        # for key, val in pfillers.items():
        #     pfstart = bisect.bisect_left(val, self.pinf.pstart)
        #     pfend = bisect.bisect_right(val, self.pinf.pend)
        #     self.pinf.pfillers[key] = val[pfstart:pfend]

        # Do the plotting
        # Things that go always at the top (observers)
        self.pinf.xdata = self.pinf.x
        for ptop in self.dplotstop:
            self.plotind(None, ptop, subinds=self.dplotsover[ptop])

        # Create the rest on a per data basis
        dt0, dt1 = self.pinf.xreal[0], self.pinf.xreal[-1]
        for data in strategy.datas:
            if not data.plotinfo.plot:
                continue

            self.pinf.xdata = self.pinf.x
            xd = data.datetime.plotrange(self.pinf.xstart, self.pinf.xend)
            if len(xd) < self.pinf.xlen:
                self.pinf.xdata = xdata = []
                xreal = self.pinf.xreal
                dts = data.datetime.plot()
                xtemp = list()
                for dt in (x for x in dts if dt0 <= x <= dt1):
                    dtidx = bisect.bisect_left(xreal, dt)
                    xdata.append(dtidx)
                    xtemp.append(dt)

                self.pinf.xstart = bisect.bisect_left(dts, xtemp[0])
                self.pinf.xend = bisect.bisect_right(dts, xtemp[-1])

            for ind in self.dplotsup[data]:
                self.plotind(
                    data,
                    ind,
                    subinds=self.dplotsover[ind],
                    upinds=self.dplotsup[ind],
                    downinds=self.dplotsdown[ind])

            self.plotdata(data, self.dplotsover[data])

            for ind in self.dplotsdown[data]:
                self.plotind(
                    data,
                    ind,
                    subinds=self.dplotsover[ind],
                    upinds=self.dplotsup[ind],
                    downinds=self.dplotsdown[ind])

        cursor = MultiCursor(
            fig.canvas, list(self.pinf.daxis.values()),
            useblit=True,
            horizOn=True, vertOn=True,
            horizMulti=False, vertMulti=True,
            horizShared=True, vertShared=False,
            color='black', lw=1, ls=':')

        self.pinf.cursors.append(cursor)

        # Put the subplots as indicated by hspace
        fig.subplots_adjust(hspace=self.pinf.sch.plotdist,
                            top=0.98, left=0.05, bottom=0.05, right=0.95)

        laxis = list(self.pinf.daxis.values())

        # Find last axis which is not a twinx (date locator fails there)
        i = -1
        while True:
            lastax = laxis[i]
            if lastax not in self.pinf.vaxis:
                break

            i -= 1

        self.setlocators(lastax)  # place the locators/fmts

        # Applying fig.autofmt_xdate if the data axis is the last one
        # breaks the presentation of the date labels. why?
        # Applying the manual rotation with setp cures the problem
        # but the labels from all axis but the last have to be hidden
        for ax in laxis:
            self.mpyplot.setp(ax.get_xticklabels(), visible=True)

        self.mpyplot.setp(lastax.get_xticklabels(), visible=True,
                          rotation=self.pinf.sch.tickrotation)

        # Things must be tight along the x axis (to fill both ends)
        axtight = 'x' if not self.pinf.sch.ytight else 'both'
        self.mpyplot.autoscale(enable=True, axis=axtight, tight=True)

    return figs

plot.Plot_OldSync.plot = p
plot.Plot = plot.Plot_OldSync.plot



