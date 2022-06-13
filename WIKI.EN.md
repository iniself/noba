Welcome to the backtrader_bokeh wiki!

Everyone who has used backtrader knows that it's plot backend is Matplotlib. The advantage is that Matplotlib is the default backend of backtrader, but the disadvantage is that Matplotlib is relatively weak in interaction and other aspects. How can the strategy data and analysis results be display in the browser? The answer is **[Backtrader_Bokeh](https://github.com/iniself/backtrader_bokeh)** which combined Backtrader and Bokeh。 Check the [example](https://iniself.github.io/backtrader_bokeh/) , you can see the plot effect via Backtrader_Bokeh.   *\* just present part of demos, all demos pls run `*.py` in [demos](https://github.com/iniself/backtrader_bokeh/tree/main/demos/)*

Backtrader_Bokeh inherited from [backtrader_plotting](https://github.com/verybadsoldier/backtrader_plotting) and [btplotting](https://github.com/happydasch/btplotting). In the meantime, corrected their problems and plan to launch a series of new features more suitable for the quantitative framework backtrader. Welcome to GitHub for issue and discussion, and ***star is also important***. If you want to support the development of Backtrader_Bokeh, consider to support this project via ETH: **0x0275779f70179748C6fCe1Fe5D7638DfA7e3F986**

Telegram Channel: [Aui_Say](https://t.me/aui_say)
Discord Server: [Aui and Friends](https://discord.gg/dhp8uzKSfR)

# Installation
```
pip install git+https://github.com/iniself/backtrader_bokeh
```

*\* If there is an error prompt during the installation and use of dependent packages，It is recommended to create a new Python environment and install backtrader_ Bokeh。Do not install like:*  
```
pip install --force-reinstall git+https://github.com/iniself/backtrader_bokeh
```

# Quickstart
Backtrader_Bokeh is very easy. You only need to import Backtrader_Bokeh in your Python file as follows. That's all , then you can to get Backtrader_Bokeh brings many benefits, include:
1. Get a powerful backend via Bokeh
2. Enhance Backtrader and fix many bugs of Backtrader through Backtrader_Bokeh's patch, instead of modifying the source code of backtrader
3. A set of easier and clearer Api 

```python
from backtrader_bokeh import bt
# import backtraer as bt  # no need anymore, don't do this
```

There are many ways to use Backtrader_Bokeh. This wiki only introduces three kinds, and you can refer to [Demo](https://github.com/iniself/backtrader_bokeh/tree/main/demos) for more information:

## Use Backtrader_Bokeh as analyzers（only Live Mode）

* Default 80 port:

  ```python
  from backtrader_bokeh import bt
    ...
    ...
  
  cerebro = bt.Cerebro()
  cerebro.addstrategy(MyStrategy)
  cerebro.adddata(LiveDataStream()) # Note! Data is must Live Data
  cerebro.addanalyzer(bt.analyzers.Live, force_plot_legend=True, autostart=True)
  cerebro.run()

  ```

* If 80 port is not available, you can use other port:

  ```python
  cerebro.addanalyzer(bt.analyzers.Live, address="localhost", port=8889, force_plot_legend=True, autostart=True)
  ```

## Use Backtrader_Bokeh as plot object

* **Normal Mode** is the backtest which has only a set of strategy's argument:

  ```python
  from backtrader_bokeh import bt
    ...
    ...
    
  plot = bt.Bokeh(style = 'bar', scheme=bt.schemes.Blackly(), force_plot_legend=True) # bt.schemes.Blackly is style of scheme
  cerebro.plot(plot, iplot=False) # if run in Jupter, need to pass 'iplot' argument in there
  ```

* **Optstrategy Mode** is the backtest which has multi sets of strategy's argument:
  ```python
  from backtrader_bokeh import bt
    ...
    ...
  	

  cerebro.optstrategy(MyStrategy, buydate=range(40, 180, 30))	
  result = cerebro.run(optreturn=False)
  
  b = bt.Bokeh(style='bar', scheme=bt.schemes.Tradimo(), force_plot_legend=True)
  browser = bt.Opt(b, result, address='localhost', port=8889, autostart= True)
  browser.start()
  ```

# New Feature

**We will put some content into there that are not easy to put into other chapter**
* **How can additional DataFeeds be plotted:**  
    By inheriting the method of datafeeds class and modifying the lines parameter, you can add datafeeds lines. But backtrader will not plot these lines, you just can use it in strategy. Since backtrader_ Bokeh `v0.0.9` , you can do it without additional work
  ```python
  from backtrader_bokeh import bt
  class MyYahooData(bt.feeds.YahooFinanceCSVData):
    lines = ('extradata',) #Add additional datafeed lines, which is backtrader's job
    extradataline = {  #Note! 'extradataline' is 'extradata' + 'line'. If wrong or is not set, line still be plotted according to the default method
        # All options in 'plotinfo' can be set in the following
        'plotname':"linename",
        'subplot':True
        ...
    }    
    ...
  ```
  As above, plotting additional data lines does not require you to do any additional work, unless you want to customize the plot of line via the option of 'extradataline'. In generally, default is ok

* **Set special transaction rules:**
  Different securities markets have different rules. For example, stock market in Chinese Mainland have a daily limit. After `v0.1.0` , these transaction rules can be set. At present, what can be set is the "daily limit", "short", and "the minimum number of purchases". If the following settings are not made, the default rule is  **no daily limit**, **can short** and **no minimum purchase limit**
  ```python
  cerebro.broker.set_rule({
    'limit':0.2, #20% for daily limit
    'short':False, #can't short
    'least':100, #minimum purchase limit is 100
  })
  ```
  * If `'limit': 0.2`, when you encounter the limit-up, you can't buy stocks, and if you encounter limit-down, you can't sell stocks. *\* Although stocks cannot be traded on the day, the order will remain valid. If you want to limit the validity period of the order, pass in the **` valid `** option, for example: ` self buy(size=1000, valid=timedelta(3))`*

  * If `'short':false`, securities can only be sold within the position size. For example: if your position is 10000, but your sales order is 15000, the transaction will be carried out automatically to 10000, and the extra 5000 **will be automatically canceled**. If carried amount is zero, the whole sales order will be canceled. *\* when printing order, the **'adj size'** should display the adjusted order amount*

  * If `'least':100`, the purchase amount can only be an integer multiple of this parameter. For example: if the amount of orders is 680, the final amount of transactions will be 600, and the extra 80 will be **automatically canceled**. *\* when printing order, the **'adj size'** should display the adjusted order amount*

* **LogTab:**  
In addition to plot, we often need to some additional informations. At this time, the usual method is to use `print` to print the information in the terminal. However, this kind of method is very unfriendly, so we put these informations to the **Logtab** web page instead of treminal:
  * Different print contents will be displayed in different tables on the **Logtab** page
  * Support to display other relevant information, such as the log title
  * Support different levels of log control. *\*CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET*
  * Can sort the log table etc.
  * Others

# List of Options 

 First, introduce some functions that need to pass in arguments:

* Live Mode
  ```python
  cerebro.addanalyzer(...)
  ```
* Normal Mode
  ```python
  bt.Bokeh(...)
  ```
* Optstrategy Mode
  ```python
  bt.Bokeh(...)
  bt.Opt(...)
  ```

This wiki will introduce Backtrader_Bokeh parameters from the following aspects:

* Type of parameters
* Definition of Parameter
* Example. *\* In addition to special statements, the parameters suitable for `bt. Bokeh()` are also suitable for `cerebro addanalyzer()`*

## Pre knowledge

Back to **Backtrader's** plot options:
* Options affecting the plotting behavior of the entire object
* Options affecting the plotting behavior of individual lines
* Options affecting the SYSTEM wide plotting options

Backtrader_Bokeh also configures plot's options like above. Backtrader_Bokeh's option inherit most of the Backtrader's option. Besides this, Backtrader_Bokeh has also added a large of options according to Bokeh's needs. In short，`Backtrader_Bokeh Options = Backtrader Options + Bokeh Options`

##  **System** and **Scheme** Options

1. **style**
   * `str`
   * Controls the type of display of the main plot: ` Single ` only shows the line chart of closing price, ` bar` or ` candle` shows the bar chart including opening price, closing price, highest price and lowest price. *\* since `v0.0.7`, you can customize the style of each data like following:*
        ```python
        data = bt.feeds.YahooFinanceCSVData(...)
        data.plotinfo.plotstyle = 'bar'      
        ```
   * `bt.Bokeh(style='bar')`
2. **resources**
   * `str`
   * Unless this option is passed in as follows, backtrader_Bokeh loads the local bokeh resource file by default instead of through the CDN network
   * `bt.Bokeh(resources='cdn')`
3. **scheme**
   * `object`
   * Plot Scheme. There are currently two schemes: blackly (dark theme) and tradimo (light theme). **Default is tradimo**
   * `bt.Bokeh(scheme=bt.schemes.Blackly())`
4. **filename**
   * `str`
   * In Normal Mode, the specified file name is used instead of the Backtrader_Bokeh default temporary file name. *\* This option is only applicable to static web pages, so it is invalid in "Live Mode" and "Optstrategy Mode"*
   * `bt.Bokeh(filename='yourfile.html')`
5. **output_mode**
   * `str`
   * only Normal Mode:  
     `save`: save the file without opening the browser  
     `show`: save the file and opening the browser  
     `memory`: do not save the file, but return to the model
6. **use_default_tabs**
   * `bool`
   * If  `true`, the default web tabs will be added
   * `bt.Bokeh(use_default_tabs=False)`
7. **tabs**
   * `list`
   * Tabs you want to add in the web page. only be effectual when `use_default_tabs=False` 
   * ```python
     bt.Bokeh(tabs=[bt.tabs.AnalyzerTab])
     ```
8. **show_headline**
   * `bool`
   * Headline show or not show
   * `bt.Bokeh(show_headline=False)`
9. **headline**
   * `str`
   * Change headline content. Default is "Backtrader Backtesting Results"
   * `bt.Bokeh(headline='Your backtrader')`
10. **force_plot_legend**
     * `bool`
    * If True **(default is True)**, all legends will be forced to plot. *\* Set to ` true` when legends dont be ploted*
    * `bt.Bokeh(force_plot_legend=True)`
11.  **hover_tooltip_config**
     * `str`
     * Decide what is included in the tooltip. When this parameter is not passed in, tooltip is default (data, indicators, observer) . For example, data feed will display time, opening price, closing price, highest price, lowest price and trading volume. But if you want to display additional info, you need this option
     * `IND-DATA`: Add the indicators info to the tooltip in the figure of main Data Feed 
     * `DATA-OBS`: Add the Data feed info to the Observer
     * `IND-OBS`:   Add the Indicators info to the Observer
     * ……
12. **plotconfig**
    * `dict`
    * **Object-Wide plotting options** (detail on **Object-Wide plotting** options）。Backtrader_Bokeh's plotconfig is equivalent to [Plotting - Backtrader](https://backtrader.com/docu/plotting/plotting/)
    * ```python
      plotconfig = {
          'id: sm5': dict(
              subplot=False,
              plotname='sm5 indicator'
          )
      }
      
      bt.Bokeh(plotconfig=plotconfig)
      ```
13. **usercolumns**
    * `dict`
    * Custom columns can be added to the results list to display special attributes of the results. To use it, you need to pass a dictionary, where the key is the label of the column, and the value is an callable value, which needs an optimization result to calculate the attribute. This option is only applicable to **Optstrategy Mode**
    * ```python
      def get_pnl_gross(strats):
          a = strats[0].analyzers.tradeanalyzer.get_analysis()
          return a.pnl.gross.total if 'pnl' in a else 0
      
      b = bt.Bokeh(style='bar', scheme=bt.schemes.Tradimo())
      browser = bt.Opt(b, result, usercolumns=dict(pnl=get_pnl_gross), sortcolumn='pnl', sortasc=False)
      browser.start()
      ```
14. Other **Scheme** Options
    * ```python
          def _set_params(self):
              self.multiple_tabs = False
              self.show_headline = True
              self.headline = ''
              self.hover_tooltip_config = ''
      
              self.barup_wick = self.barup
              self.bardown_wick = self.bardown
      
              self.barup_outline = self.barup
              self.bardown_outline = self.bardown
      
              self.crosshair_line_color = '#999999'
      
              self.legend_background_color = '#3C3F41'
              self.legend_text_color = 'lightgrey'
              self.legend_location = 'top_left'
              self.legend_orientation = 'vertical'
      
              self.loc = 'lightgray'
              self.background_fill = '#222222'
              self.body_background_color = 'white'
              self.border_fill = '#3C3F41'
              self.legend_click = 'hide'  # or 'mute'
              self.axis_line_color = 'darkgrey'
              self.tick_line_color = self.axis_line_color
              self.grid_line_color = '#444444'
              self.axis_text_color = 'lightgrey'
              self.plot_title_text_color = 'darkgrey'
              self.axis_label_text_color = 'darkgrey'
              self.tag_pre_background_color = 'lightgrey'
              self.tag_pre_text_color = 'black'
      
              self.xaxis_pos = 'all'  # 'all' or 'bottom'
      
              self.table_color_even = '#404040'
              self.table_color_odd = '#333333'
              self.table_header_color = '#7a7a7a'
      
              # Plot a title above the plot figure
              self.plot_title = True
              # Number of columns on the analyzer tab
              self.analyzer_tab_num_cols = 1
              # Number of columns on the metadata tab
              self.metadata_tab_num_cols = 3
              # Sizing mode for plot figures
              self.plot_sizing_mode = 'scale_width'
              # Aspect ratios for different figure types
              self.data_aspectratio = 2.5
              self.vol_aspectratio = 5.0
              self.obs_aspectratio = 5.0
              self.ind_aspectratio = 5.0
              # output backend mode ("canvas", "svg", "webgl")
              self.output_backend = 'canvas'
      
              self.toolbar_location = 'right'
      
              self.tooltip_background_color = '#4C4F51'
              self.tooltip_text_label_color = '#848EFF'
              self.tooltip_text_value_color = '#aaaaaa'
      
              self.tab_active_background_color = '#333333'
              self.tab_active_color = '#4C4F51'
      
              self.text_color = 'lightgrey'
      
              # https://docs.bokeh.org/en/latest/docs/reference/models/formatters.html#bokeh.models.formatters.DatetimeTickFormatter
              self.hovertool_timeformat = '%F %R'
      
              self.number_format = '0,0[.]00[000000]'
              self.number_format_volume = '0.00 a'
      
              # https://docs.bokeh.org/en/latest/docs/reference/models/formatters.html
              self.axis_tickformat_days = '%d %b %R'
              self.axis_tickformat_hourmin = '%H:%M:%S'
              self.axis_tickformat_hours = '%d %b %R'
              self.axis_tickformat_minsec = '%H:%M:%S'
              self.axis_tickformat_minutes = '%H:%M'
              self.axis_tickformat_months = '%d/%m/%y'
              self.axis_tickformat_seconds = '%H:%M:%S'
              self.axis_tickformat_years = '%Y %b'
      
              # used to add padding on the y-axis for all data except volume
              self.y_range_padding = 0.5
              # position of y axis for volume
              self.vol_axis_location = 'right'
      ```
    * **Scheme** Options can be directly pass into ` cerebro Addanalyzer() ` or `bt. bokeh()` as arguments. Or you can pass into the construct function of the scheme class
      * ```python
        bt.Bokeh(overtool_timeformat='%F %R:%S')
        ```
      * ```python
        bt.Bokeh(scheme=bt.schemes.Blackly(overtool_timeformat='%F %R:%S'))
        ```
        
## **Object-Wide plotting** options

It has been said in **pre knowledge**, **Object-Wide plotting** options are the settings of **plotinfo** and **plotlines** for each object (such as an indicator). There are three ways to configure this option in backtrader:

1. **Inheriting:**
   ```python
   class MY_SMA(bt.indicators.SMA):
      params = (('barplot', True), ('bardist', 0.02))
      plotinfo = dict(
        plotname = "MySMA"
      )
      plotlines = dict(
   		...
     )
   class MyStrategy(bt.Strategy):
     def __init__(self):
       self.sma5 = MY_SMA(period=15)
     ....
     
   cerebro.addstrategy(MyStrategy)
   ```
2. **Pass in argument:**
   ```python
   class MyStrategy(bt.Strategy):
     def __init__(self):
   		self.sma5 = bt.indicators.SMA(period=15, plotname = "MySMA")
     ....
     
   cerebro.addstrategy(MyStrategy)
   ```
   ```python
   class MyStrategy(bt.Strategy):
     def __init__(self):
   		self.sma5 = bt.indicators.SMA(period=15)
   		self.sma5.plotinfo.plotname = "MySMA"
     ....
     
   cerebro.addstrategy(MyStrategy)
   ```
3. **Backtrader_Bokeh adds a way to handle all Object-Wide plotting options in one place:**
   ```python
   class MyStrategy(bt.Strategy):
     def __init__(self):
        self.sma5 = bt.indicators.SMA(period=15)
        self.sma5.plotinfo.plotid='sm5'
     ....
   plotconfig = {
       'id:sm5': dict(
           plotname='MySMA'
       )
   }  
   cerebro.addstrategy(MyStrategy)
   b = bt.Bokeh(plotconfig=plotconfig)
   cerebro.plot(b)
   ```
Example of **Object-Wide plotting** options *\*  just part of plotinfo，more plotinfo and plotlines pls refer Backtrader* :
1. **plot**
    * `bool`
    * Whether the object has to be plotted
    * `plot=True`
2. **subplot**
   * `bool`
   * Whether to plot along the data or in an independent subchart. Moving Averages are an example of plotting over the data. Stochastic and RSI are examples of things plotted in a subchart on a different scale
   * `subplot=True`
3. **plotmaster**
   * `object`
   * An Indicator/Observer has a master which is the data on which is working. In some cases plotting it with a different master may be wished needed
   * ```python
     class MyStrategy(bt.Strategy):
         def __init__(self):
             self.sma5 = bt.indicators.SMA(period=5, subplot=True)
             self.sma10 = bt.indicators.SMA(period=10, plotmaster=sma5)
     ```
4. **plotname**
   * `str`
   * Name to use on the chart instead of the class name. As in the example above mysma instead of SimpleMovingAverage
   * `plotname='somename'`
5. **plotorder**
   * `int`
   * The smaller of number, the plot is more upper on the page. Default all ` 0`  
     *\* The following code will let the Observer be ploted above Data Feed (stock price, trading volume and other main charts)*
   * ```python
     class MyBroker(bt.observers.Broker):
         def __init__(self):
             self.plotinfo.plotorder = 5
             
     cerebro.addobserver(MyBroker)
     ```
6. The other **Object-Wide plotting** options
   * ```python
     plotinfo = dict(plot=True, 
                     subplot=True,
                     plotname='',
                     plotorder=0, 
                     plotlinelabels=False, # whether to plot the names of the individudal lines along the data in the legend on the chart when subplot=False
                     plotlinevalues=True, # controls whether the legend for the lines in indicators and observers has the last plotted value. Can be controlled on a per-line basis with _plotvalue for each line
                     plotvaluetags=True, # controls whether a value tag with the last value is plotted on the right hand side of the line. Can be controlled on a per-line basis with _plotvaluetag for each line
                     plotymargin=0.0, # margin to add to the top and bottom of individual subcharts on the graph. It is a percentage but 1 based. For example: 0.05 -> 5%
                     plothlines=[a,b,...], # an iterable containing values (within the scale) at which horizontal lines have to be plotted
                     plotyticks=[], #  an iterable containing values (within the scale) at which value ticks have to specifically be placed on the scale
                     plotyhlines=[a,b,...], # an iterable containing values (within the scale) at which horizontal lines have to be plotted
                     plotforce=False, # sometimes and thus the complex process of matching data feeds to indicators and bla, bla, bla … a custom indicator may fail to plot. This is a last resort mechanism to try to enforce plotting
                     plotmaster=None, # an Indicator/Observer has a master which is the data on which is working. In some cases plotting it with a different master may be wished needed
                     plotylimited=True, # currently only applies to data feeds. If True (default), other lines on the data plot don’t change the scale. Example: Bollinger Bands (top and bottom) may be far away from the actual absolute minimum/maximum of the data feed. With \plotlimited=True, those bands remain out of the chart, because the data controls the scaling. If set toFalse`, the bands affects the y-scale and become visible on the chart
     )
     ```
   * Please try different options by yourself

## **Browser** option

1. **autostart**
   * `bool`
   * If `true` **(default is True)**, open browser automatically. **\* Suitable for Optstrategy Mode and Live Mode, because browser can't be open automatically under the two Modes**
   * `bt.Opt(autostrart=True)` (**Optstrategy Mode**),  `cerebro.addanalyzer(autostrart=True)` (**Live Mode**)
2. **address**
   * `str`
   * Hosts address. If run Backtrader_Bokeh locally, the configuration is "localhost" :
   * `bt.Opt(address='localhost', port=8889` (**Optstrategy Mode**),  `cerebro.addanalyzer(address='localhost', port=9889)` (**Live Mode**)
3. **port**
   * `int`
   * Web port. The default is `80` port，If `80` port is not available or want to share the plotting to public, you can change the default port:
   * `bt.Opt(address='localhost', port=8889` (**Optstrategy Mode**),  `cerebro.addanalyzer(address='localhost', port=9889)` (**Live Mode**)

# Datadomains
Datadomains are basically used to group entities that belong together to plot them together on one page. A datadomain is a single string. All entities having an identical string belong to the same datadomain.

Per default each data feed creates one datadomain which is derived from its `_name` attribute. All entities that are based on this data (like e.g. indiators) will inherit the datadomain of that data. So by default each data and its corresponding indicators and others entities do form a separate datadomain.

Datadomain values can be manually overridden though to change the automtically created grouping. This is done by passing the parameter `datadomain` to the initializer of an entity.