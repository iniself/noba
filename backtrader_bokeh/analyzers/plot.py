import asyncio
import logging
from threading import Lock
import threading

import backtrader as bt

import tornado.ioloop

from ..app import BacktraderBokeh
from ..webapp import Webapp
from ..schemes import Tradimo, Blackly
from ..live.client import LiveClient

_logger = logging.getLogger(__name__)

def combine_custom_conf(name, default):
    custom_config = dict(bt.custom_config['system'], **bt.custom_config['browser'])
    if name in custom_config:
        val = custom_config[name]
        if name == 'scheme':
            if val in ['White', 'Tradimo']:
                val = Tradimo()
            elif val in ['Black', 'Blackly']:
                val = Blackly()
            else:
                val = default

        if name == 'tabs':
            try:
                v = []
                for one in val:
                    if one == 'LogTabs':
                        col = bt.custom_config["scheme"]["logger_tab_num_cols"] if bt.custom_config["scheme"]["logger_tab_num_cols"] else 2
                        one = f'LogTabs({col})'
                    v.append(eval('bt.tabs.' + one))
                val = v
            except:
                val = default

        return val
    else:
        return default

class LivePlotAnalyzer(bt.Analyzer):

    params = (
        ('scheme', combine_custom_conf('scheme', Tradimo())),
        ('style', combine_custom_conf('style', 'bar')),
        ('lookback', 23),
        ('address', combine_custom_conf('address', 'localhost')),
        ('port', combine_custom_conf('port', 8999)),
        ('title', combine_custom_conf('title', None)),
    )

    def __init__(self, **kwargs):
        title = self.p.title
        if title is None:
            title = 'Live %s' % type(self.strategy).__name__
        if not 'autostart' in kwargs:
            kwargs['autostart'] = True
        self._webapp = Webapp(
            title,
            'basic.html.j2',
            self.p.scheme,
            self._app_cb_build_root_model,
            on_session_destroyed=self._on_session_destroyed,
            autostart=kwargs['autostart'],
            address=self.p.address,
            port=self.p.port)
        self._lock = Lock()
        self._clients = {}
        self._app_kwargs = kwargs

    def _create_app(self):
        return BacktraderBokeh(
            style=self.p.style,
            scheme=self.p.scheme,
            **self._app_kwargs)

    def _on_session_destroyed(self, session_context):
        with self._lock:
            self._clients[session_context.id].stop()
            del self._clients[session_context.id]

    def _t_server(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = tornado.ioloop.IOLoop.current()
        self._webapp.start(loop)

    def _app_cb_build_root_model(self, doc):
        client = LiveClient(doc,
                            self._create_app(),
                            self.strategy,
                            self.p.lookback)
        with self._lock:
            self._clients[doc.session_context.id] = client
        return client.model

    def start(self):
        '''
        Start from backtrader
        '''
        _logger.debug('Starting PlotListener...')
        t = threading.Thread(target=self._t_server)
        t.daemon = True
        t.start()

    def stop(self):
        '''
        Stop from backtrader
        '''
        _logger.debug('Stopping PlotListener...')
        with self._lock:
            for c in self._clients.values():
                c.stop()

    def next(self):
        '''
        Next from backtrader, new data arrives
        '''
        with self._lock:
            for c in self._clients.values():
                c.next()
