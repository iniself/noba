#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2023/3/10  
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

# class BBService(object):
#     pass
#
#
# class BTService(object):
#     pass


from noba.confighandler import custom_config
import backtrader as bt
bt.custom_config = custom_config
import noba.tabs as tabs
#tabs: AnalyzerTab, MetadataTab, ConfigTab, LogTabs, SourceTab
bt.tabs = tabs

bt.tabs.LogTabs = lambda cols:type("LogTab",(bt.tabs.LogTab,),{'cols':cols})
bt.getlogger = bt.tabs.log.getlogger
bt.get_order_logger = lambda name="Order Trace": bt.getlogger(col=['Day', 'Ref', 'OrdType', 'Status', 'Size', 'Remsize', 'Alive'], name=name)


from noba.app import BacktraderBokeh
from noba.analyzers import LivePlotAnalyzer as BacktraderBokehLive
from noba.optbrowser import OptBrowser as BacktraderBokehOptBrowser
from noba.analyzers import RecorderAnalyzer
from noba.analyzers import TradelistAnalyzer
from noba.feeds import FakeFeed

import noba.schemes as schemes

# initialize analyzer tables
from noba.analyzer_tables import inject_datatables
inject_datatables()

from noba.plugin import *
bt.Bokeh = BacktraderBokeh

# Customized analyzers and feeds
bt.analyzers.Live = BacktraderBokehLive
bt.analyzers.Recorder = bt.analyzers.RecorderAnalyzer = RecorderAnalyzer
bt.analyzers.Tradelist = bt.analyzers.TradelistAnalyzer = TradelistAnalyzer
bt.feeds.FakeFeed = FakeFeed

bt.Opt = BacktraderBokehOptBrowser

#schemes: Blackly, Tradimo
bt.schemes = schemes
bt.schemes.Black = schemes.Blackly
bt.schemes.White = schemes.Tradimo