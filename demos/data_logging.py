from backtrader_bokeh import bt
import datetime

class MyStrategy(bt.Strategy):
    def next(self):
        open([self.data.open[0]])
        close.info([self.data.open[0]])


if __name__ == '__main__':
    # get logger with default log level INFO
    open = bt.getlogger(['open'], name='Open Price')
    close = bt.getlogger(['close'], name='Close Price')

    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)

    data = bt.feeds.YahooFinanceCSVData(
        dataname="datas/orcl-1995-2014.txt",
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2001, 2, 28),
        reverse=False,
        swapcloses=True,
    )
    cerebro.adddata(data)

    cerebro.run()

    p = bt.Bokeh(style='bar', use_default_tabs=False,  tabs=[bt.tabs.LogTabs(2)])
    cerebro.plot(p)
