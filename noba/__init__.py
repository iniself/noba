from .confighandler import custom_config
import backtrader as bt
bt.custom_config = custom_config
import noba.tabs as tabs
#tabs: AnalyzerTab, MetadataTab, ConfigTab, LogTabs, SourceTab
bt.tabs = tabs

bt.tabs.LogTabs = lambda cols:type("LogTab",(bt.tabs.LogTab,),{'cols':cols})
bt.getlogger = bt.tabs.log.getlogger
bt.get_order_logger = lambda name="Order Trace": bt.getlogger(col=['Day', 'Ref', 'OrdType', 'Status', 'Size', 'Remsize', 'Alive'], name=name)


from .app import BacktraderBokeh
from .analyzers import LivePlotAnalyzer as BacktraderBokehLive
from .optbrowser import OptBrowser as BacktraderBokehOptBrowser
from .analyzers import RecorderAnalyzer
from .analyzers import TradelistAnalyzer
from .feeds import FakeFeed

import noba.schemes as schemes

# initialize analyzer tables
from .analyzer_tables import inject_datatables
inject_datatables()

from .plugin import *
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