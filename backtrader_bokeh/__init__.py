from .app import BacktraderBokeh
from .analyzers import LivePlotAnalyzer as BacktraderBokehLive
from .optbrowser import OptBrowser as BacktraderBokehOptBrowser
from .analyzers import RecorderAnalyzer
from .analyzers import TradelistAnalyzer
from .feeds import FakeFeed

import backtrader_bokeh.schemes as schemes
import backtrader_bokeh.tabs as tabs

# initialize analyzer tables
from .analyzer_tables import inject_datatables
inject_datatables()

import backtrader as bt
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

#tabs: AnalyzerTab, MetadataTab, ConfigTab, LogTab, SourceTab
bt.tabs = tabs
