# Backtrader_Bokeh 

==**You can visit our wiki homepage for more information [EN](https://github.com/iniself/backtrader_bokeh/wiki) | [中文](https://github.com/iniself/backtrader_bokeh/wiki/wiki-zh)**==

Library to add extended plotting capabilities to `backtrader` (<https://www.backtrader.com/>) using bokeh.

Backtrader_Bokeh is based on the awesome `backtrader_plotting` (<https://github.com/verybadsoldier/backtrader_plotting>) and `btplotting`(https://github.com/happydasch/btplotting)

`Backtrader_Bokeh` is a complete rework of `backtrader_plotting` with the live client in focus. Besides this, a lot of issues are fixed and new functionality is added. See the list below for differences.

**What is different:**

Basic:

* No need for custom backtrader
* Different naming / structure
* Different data generation which allows to generate data for different data sources.
  This is useful when replaying or resampling data, for example to remove gaps.
* Different filtering of plot objects
* Support for replay data
* Every figure has its own ColumnDataSource, so the live client can patch without
  having issues with nan values, every figure is updated individually
* Display of plots looks more like backtrader plotting (order, heights, etc.)
* Allows to generate custom columns, which don't have to be hardcoded. This is being used to generate
  color for candles, varea values, etc.
* Possibility to fill gaps of higher timeframes with data

Plotting:

* Datas, Indicators, Observer and Volume have own aspect ratios, which can be configured in live client
  or scheme
* Only one axis for volume will be added when using multiple data sources on one figure
* Volume axis position is configureable in scheme, by default it is being plotted on the right side
* Linked Crosshair across all figures
* fill_gt, fill_lt, fill support
* Plot objects can be filtered by one or more datanames or by plot group
* Custom plot group, which can be configured in app or in live client by providing all
  plotids in a comma-seperated list or by selecting the parts of the plot to display

Tabs:

* Default tabs can be completely removed
* New log panel to also include logging information
* Can be extended with custom tabs (for example order execution with live client, custom analysis, etc.)

Live plotting:

* Navigation in live client (Pause, Backward, Forward)
* Live plotting is done using an analyzer, so there is no need to use custom backtrader
* Live plotting data update works in a single thread and is done by a DataHandler
* Data update is being done every n seconds, which is configureable

## Features

* Interactive plots
* Interactive `backtrader` optimization result browser (only supported for single-strategy runs)
* Highly configurable
* Different skinnable themes
* Easy to use

## Bug fixed

* Because of optbrowser address and port assignment mistake problem, if port 80 is occupied, the web page will not be opened in the optimization mode
* Very imortant, fixed the legend can't be displayed in the observer or indicators's figuer



***

Python >= 3.6 is required.


## How to use
* Add to cerebro as an analyzer:
```python
from backtrader_bokeh import BacktraderBokehLive
  ...
  ...

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata(LiveDataStream())
cerebro.addanalyzer(BacktraderBokehLive)
cerebro.run()
# cerebro.plot() # do not run this line unless your data is not real-time
```

* If you need to change the default port or share the plotting to public:

```python
cerebro.addanalyzer(BacktraderBokehLive, address="localhost", port=8889)
```

## Jupyter

In Jupyter you can plut to a single browser tab with iplot=False:

```python
plot = backtrader_bokeh.BacktraderBokeh()
cerebro.plot(plot, iplot=False)
```

You may encounters TypeError: `<class '__main__.YourStrategyClass'>` is a built-in class error.

To remove the source code tab use:

```python
plot = backtrader_bokeh.BacktraderBokeh()
plot.tabs.remove(backtrader_bokeh.tabs.SourceTab)
cerebro.plot(plot, iplot=False)
```

## Demos

<https://iniself.github.io/backtrader_bokeh/>

## Installation

`pip install git+https://github.com/iniself/backtrader_bokeh`

## Sponsoring

If you want to support the development of backtrader_bokeh, consider to support this project.

* ETH: 0x0275779f70179748C6fCe1Fe5D7638DfA7e3F986
