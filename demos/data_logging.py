from backtrader_bokeh.tabs.log import init_log_tab
from backtrader_bokeh import bt
import logging
import datetime


class MyStrategy(bt.Strategy):
    def next(self):
        print(f"close: {self.data.close[0]}")
        logger.debug(f"open: {self.data.open[0]}")
        logger.info(f"close: {self.data.close[0]}")


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # add stream handler to log everything to console
    logger.addHandler(logging.StreamHandler())
    cerebro = bt.Cerebro()

    # init log tab with log level INFO
    init_log_tab([__name__], logging.INFO)

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

    p = bt.Bokeh(style='bar', force_plot_legend=True)
    cerebro.plot(p)
