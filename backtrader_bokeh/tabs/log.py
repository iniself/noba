#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2022/6/12
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

import logging
import pandas as pd
from threading import Lock
from functools import partial
from tornado import gen

from bokeh.io import curdoc
from bokeh.models import DataTable, TableColumn, ColumnDataSource, Paragraph
from bokeh.layouts import column, row, gridplot, layout

from ..tab import BacktraderBokehTab


handlers = []

def getlogger(col=[], name='Log Detail', stdout=False, level=logging.DEBUG):
    global handlers
    if isinstance(name,list) and len(name) > 0:
        logger = []
        for n in name:
            handler = get_hander()(level=level, col=col, title=n)
            one = logging.Logger(n)
            one.addHandler(handler)
            stdout and one.addHandler(logging.StreamHandler())
            logger.append(one)
            handlers.append(handler)
        # return logger
    else:
        handler = get_hander()(level=level, col=col, title=name)
        logger = logging.Logger(str(id(handler))[0:10])
        logger.addHandler(handler)
        stdout and logger.addHandler(logging.StreamHandler())
        handlers.append(handler)
        # return logger
    return logger


def is_log_tab_initialized():
    global handlers
    return len(handlers) > 0

def get_hander():
    class CDSHandler(logging.Handler):
        def __init__(self, title, level=logging.DEBUG, col=[]):
            super(CDSHandler, self).__init__(level=level)
            self._lock = Lock()
            self.messages = []
            self.idx = {}
            self.cds = {}
            self.cb = {}
            self.col = col
            self.title = title


        def emit(self, record):
            message = record.msg
            self.messages.append(message)
            with self._lock:
                for doc in self.cds:
                    try:
                        doc.remove_next_tick_callback(self.cb[doc])
                    except ValueError:
                        pass
                    self.cb[doc] = doc.add_next_tick_callback(
                        partial(self._stream_to_cds, doc))


        def  _split_cols(self, msg):
            if len(msg)==0:
                msg.append([])
            if not isinstance(msg[0],list):
                msg[0] = [msg[0]]
            diff = len(self.col) - len(msg[0])
            if diff > 0:
                # msg = list(map(lambda m:m + ['None']*diff,msg))
                msg = list(map(lambda m:(m if isinstance(m,list) else [m]) + ['None']*diff,msg))
            elif diff < 0:
                for x in range(0,abs(diff)):
                    self.col = self.col + [str(x)]

            df = pd.DataFrame(msg,columns=self.col)
            return df

        def get_cds(self, doc):
            if doc not in self.cds:
                with self._lock:
                    self.cds[doc] = ColumnDataSource(
                        data=self._split_cols(self.messages.copy())
                    )
                    self.cb[doc] = None
                    self.idx[doc] = len(self.messages) - 1
                    self.cds[doc].selected.indices = [self.idx[doc]]
            return self.cds[doc]

        @gen.coroutine
        def _stream_to_cds(self, doc):
            last = len(self.messages) - 1
            messages = self.messages[self.idx[doc] + 1:last + 1]
            if not len(messages):
                return
            with self._lock:
                self.idx[doc] = last
                self.cds[doc].stream({'message': messages})
                # move only to last if there is a selected row
                # when no row is selected, then don't move to new
                # row
                if len(self.cds[doc].selected.indices) > 0:
                    self.cds[doc].selected.indices = [self.idx[doc]]
    return CDSHandler



class LogTab(BacktraderBokehTab):

    def _is_useable(self):
        return is_log_tab_initialized()

    def _get_panel(self):
        global handlers
        if len(handlers) == 0:
            getlogger([])
        if self._client is not None:
            doc = self._client.doc
        else:
            doc = curdoc()

        child = []

        for h in handlers:
            message = []
            source = h.get_cds(doc)
            title = Paragraph(
                text = h.title,
                css_classes=['table-title'])
            for n in h.col:
                message.append(TableColumn(
                    field=n,
                    title="No title" if n.isnumeric() else n,
                    sortable=True
                ))
            table = DataTable(
                source=source,
                columns=message,
                height=250,
                scroll_to_selection=True,
                sortable=True,
                reorderable=False,
                fit_columns=True)

            c = column(
                children=[title, table],
                sizing_mode='scale_width')
            child.append(c)
        info = gridplot(
            child,
            ncols=self.cols,
            sizing_mode='stretch_width',
            toolbar_options={'logo': None})


        title_area = []
        title = Paragraph(
            text='Log Overview',
            css_classes=['panel-title'])
        title_area.append(row([title], width_policy='min'))

        l =  layout(
            [
                title_area,
                [info]
            ],
            sizing_mode='stretch_width'
        )

        return l, 'Log'
