import datetime

from backtrader_bokeh import bt


cerebro = bt.Cerebro()

data = bt.feeds.YahooFinanceCSVData(
    dataname="datas/orcl-1995-2014.txt",
    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2001, 2, 28),
    reverse=False,
    swapcloses=True,
)
cerebro.adddata(data)
data1 = cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks, compression=1)
data1.plotinfo.plotmaster = data
cerebro.addanalyzer(bt.analyzers.SharpeRatio)

cerebro.run()

p = bt.Bokeh(style='bar', force_plot_legend=True)
cerebro.plot(p)
