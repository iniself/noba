用过 Backtrader 都知道它的可视化是用的 `matplotlib` , 好处是开箱即用，因为 `matplotlib` 是 Backtrader的默认可视化后端，但缺点就是 `matplotlib`的绘图还是不够日常需要。要说到图片文字的展示能力，我们熟悉的 HTML + JS + CSS 才是王道。那么有没有一个可以在浏览器展示策略数据和分析结果的呢？答案就是 Backtrader和 Bokeh 的结合产品：[Welcome to backtrader_bokeh | backtrader_bokeh (iniself.github.io)](https://iniself.github.io/backtrader_bokeh/)

`Backtrader_Bokeh`继承自[backtrader_plotting](https://github.com/verybadsoldier/backtrader_plotting) and [btplotting](https://github.com/happydasch/btplotting) ，对两者的问题做了修正并且计划推出更加适合量化框架 Backtrader 的一系列新特性。欢迎来 github 上关注及讨论

# 快速上手

使用 Backtrader_Bokeh 非常容易，它对原 Backtrader 是无侵入的。有多种方式使用 Backtrader_Bokeh 。本文只介绍 3 种，其他更多你可以参考 [Demo](https://github.com/iniself/backtrader_bokeh/tree/main/demos):

## 把  Backtrader_Bokeh 当作策略使用（适用于实时数据模式）

* 使用默认 80 端口：

  ```python
  from backtrader_bokeh import BacktraderBokehLive
    ...
    ...
  
  cerebro = bt.Cerebro()
  cerebro.addstrategy(MyStrategy)
  cerebro.adddata(LiveDataStream())
  cerebro.addanalyzer(BacktraderBokehLive, force_plot_legend=True, autostart=True)
  cerebro.run() # 注意如果上面添加的数据不是实数数据，则打开浏览器失败
  ```

* 如果你的 80 端口被占用，比如你同时运行了 `nginx`，此时需要指定其他端口启动 Backtrader_Bokeh：

  ```python
  cerebro.addanalyzer(BacktraderBokehLive, address="localhost", port=8889, force_plot_legend=True, autostart=True)
  ```

## 把  Backtrader_Bokeh 当作回测工具使用

* 普通模式（常用）：对一套策略参数的回测

  ```python
  from backtrader_bokeh import BacktraderBokeh
  from backtrader_bokeh.schemes import Blackly  # Blackly 是主题
  	...
    ...
    
  plot = backtrader_bokeh.BacktraderBokeh(style = 'bar', scheme=Blackly(), force_plot_legend=True)
  cerebro.plot(plot, iplot=False) # 如果你在 Jupyter 中运行，需要传入 iplot 参数
  ```

  

* 参数优化模式：对对套策略参数的回测。可以选择在不同参数下展示策略的效果

  ```python
  from backtrader_bokeh import BacktraderBokeh
  from backtrader_bokeh import BacktraderBokehOptBrowser
  from backtrader_bokeh.schemes import Tradimo
  	...
  	...
  	
  	
  result = cerebro.run(optreturn=False)
  
  b = BacktraderBokeh(style='bar', scheme=Tradimo(), force_plot_legend=True)
  browser = BacktraderBokehOptBrowser(b, result, address='localhost', port=8889, autostart= True)
  browser.start()
  ```

  

# 参数列表

Backtrader_Bokeh 涉及到需要传入参数几个函数：

* Live mode 时
  ```python
  cerebro.addanalyzer(...)
  ```
* 常规回测模式时
  ```python
  BacktraderBokeh(...)
  ```
* 参数优化模式时
  ```python
  BacktraderBokeh(...)
  BacktraderBokehOptBrowser(...)
  ```

本文从如下几个方面介绍 Backtrader_Bokeh 配置参数：

* 该参数的类型
* 该参数的用途
* 该参数适合哪些函数。本文除了特殊说明外，**适合 `BacktraderBokeh()` 的参数同样适合 `cerebro.addanalyzer()`**

## 前置知识

回忆一下 **Backtrader** 自带的绘图选项：
* Options affecting the plotting behavior of the entire object：对象的绘图选项。比如一个指标就是一个对象，它会自带默认的**plotinfo**(控制这个指标整体的绘图) 和 **plotlines**(控制每条 lines 的绘图)。该配置对应 **plotinfo**
* Options affecting the plotting behavior of individual lines：该配置对应绘图对象的 **plotlines** 配置
* Options affecting the SYSTEM wide plotting options：Backtrader 最上层的配置和某个主题的配置

Backtrader_Bokeh 也是以这样的分类来配置绘图选项的。在继承了大部分 Backtrader 配置的前提下[^1]，Backtrader_Bokeh 根据 Bokeh 的需要还增加了大量配置。简言之，`Backtrader_Bokeh'Options = Backtrader'Options + Bokeh'Options`

##  “系统”和“主题”的绘图选项

1. `style`
   * `str`
   * 控制主图显示的类型。`single`显示收盘价的线条图，`bar` 或则 `candle`显示包含了开盘价、收盘价、最高价、最低价的 K 线柱状图
   * `BacktraderBokeh(style='bar')`
2. `scheme`
   * `object`
   * 告诉 Backorder_Bokeh 绘图时选择哪个主题：目前有两个主题 Blackly（深色主题）和 Tradimo（浅色主题）
   * `BacktraderBokeh(scheme=Blackly())`
3. `filename`
   * `str`
   * 在常规回测时，用指定的文件名代替 Backtrader_Bokeh 默认的临时文件名。 **仅适应于生成的静态网页，所以在 “live mode” 和“参数优化” 时此选项无效**
   * `BacktraderBokeh(filename='yourfile.html')`
4. `output_mode`
   * `str`
   * 在常规回测时:
     `save`：只保存文件，不打开浏览器
     `show`：保存文件同时打开浏览器
     `memory`：不保存文件，但返回模型
5. `use_default_tabs`
   * `bool`
   * 如果设置成 `true` ，则默认的网页 tab 将会添加进去
   * `BacktraderBokeh(use_default_tabs=False)`
6. `tabs`
   * `list`
   * 在网页中希望添加的 tab。在 `use_default_tabs=False` 生效
   * ```python
     from backtrader_bokeh.tabs.analyzer import AnalyzerTab
     BacktraderBokeh(tabs=[AnalyzerTab])
     ```
7. `show_headline`
   * `bool`
   * 是否显示设置页面标题
   * `BacktraderBokeh(show_headline=False)`
8. `headline`
   * `str`
   * 改变页面标题。默认是 `Backtrader Backtesting Results`
   * `BacktraderBokeh(headline='Your backtrader')`
9. `force_plot_legend`
   * `bool`
   * 是否强制显示所有图例(legend)。当遇到有图列不显示时设置成 `True`
   * `BacktraderBokeh(force_plot_legend=True)`
10. `hover_tooltip_config`
    * `str`
     * 控制数据指向图形时的提示内容。在没有传入该参数时，Backtrader_Bokeh 会默认用该数据类型（Datas、Indicators、Observer）默认的方式提示。比如 Datas 会显示时间、开盘价、收盘价、最高价、最低价、交易量，但如果想显示额外数据，就需要用到这个选项
     * `IND-DATA`: 把 Indicators 的数据添加到主图(Datas)的 tooltip 
     * `DATA-OBS`: 把主图数据添加到Observer 
     * `IND-OBS`:   把 Indicators 的数据添加到 Observer
     * ……
1.  `plotconfig`
    * `dict`
    * 用于控制 **局部绘图** 时的参数配置（具体见**局部绘图选项**）。Backtrader_Bokeh 的 `plotconfig` 相当于 [Plotting - Backtrader](https://backtrader.com/docu/plotting/plotting/)  中的 **Object-wide plotting options**
    * ```python
      plotconfig = {
          'id: sm5': dict(
              subplot=False,
              plotname='sm5 indicator'
          )
      }
      
      BacktraderBokeh(plotconfig=plotconfig)
      ```
2.  `usercolumns`
    * `dict`
    * 自定义列可以添加到结果列表中，用于显示结果中感兴趣的特殊属性。要使用它，需要传递一个字典，其中键是列的标签，值是一个可调用的值，该值需要一个优化结果来计算属性。该参数只适用于**参数优化模式**
    * ```python
      def get_pnl_gross(strats):
          a = strats[0].analyzers.tradeanalyzer.get_analysis()
          return a.pnl.gross.total if 'pnl' in a else 0
      
      b = BacktraderBokeh(style='bar', scheme=Tradimo())
      browser = BacktraderBokehOptBrowser(b, result, usercolumns=dict(pnl=get_pnl_gross), sortcolumn='pnl', sortasc=False)
      browser.start()
      ```
3.  `其他主题参数`
    * ```
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
    * 主题参数可以直接在 `cerebro.addanalyzer()` 中传入这些参数。或则可以在主题构建函数中传入：
      * ```
        BacktraderBokeh(overtool_timeformat='%F %R:%S')
        ```
      * ```python
        BacktraderBokeh(scheme=Blackly(overtool_timeformat='%F %R:%S'))
        ```
        
## “局部绘图”选项

在 **前置知识** 中已经说过 局部选项 就是针对每个对象（比如某个指标）的 **plotinfo** 和 **plotlines**  的设置。在 Backtrader 配置此选项有 三种方式：
1. 通过继承类：
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
2. 传参修改：
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
3. Backtrader_Bokeh 多了一种可以在一个地方处理所有对象绘图参数的方法：
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
   b = BacktraderBokeh(plotconfig=plotconfig)
   cerebro.plot(b)
   ```
   **局部绘图**选项[^2]：
1.  `plot`
   * `bool`
   * 是否绘制此图
   * `plot=True`
2. `subplot`
   * `bool`
   * 是否绘制成子图，否则将在主图中统一显示
   * `subplot=True`
3. `plotmaster`
   * `object`
   * 用哪个绘图对象作为自己的主图。比如默认情况下，indicators 是和 主图（股价、交易量）绘制在一起。通过如下代码可以把 indicators 单独绘制
   * ```python
     class MyStrategy(bt.Strategy):
         def __init__(self):
             self.sma5 = bt.indicators.SMA(period=5, subplot=True)
             self.sma10 = bt.indicators.SMA(period=10, plotmaster=sma5)
     ```
4. `plotname`
   * `str`
   * 图例名字
   * `plotname='somename'`
5. `plotorder`
   * `int`
   * 各绘图对象在页面上的绘图顺序。数字越小则越在上面。默认所有为`0`。 下面代码会让 Observer 绘制在 Datas (股价、交易量等主图)
   * ```python
     class MyBroker(bt.observers.Broker):
         def __init__(self):
             self.plotinfo.plotorder = 5
             
     cerebro.addobserver(MyBroker)
     ```
6. `其他局部绘图选项`[^3]
   * ```python
     plotinfo = dict(plot=True, # 是否绘制
                     subplot=True, # 是否绘制成子图
                     plotname='', # 图形名称
                     plotabove=False, # 子图是否绘制在主图的上方
                     plotlinelabels=False, # 主图上曲线的名称
                     plotlinevalues=True, # 是否展示曲线最后一个时间点上的取值
                     plotvaluetags=True, # 是否以卡片的形式在曲线末尾展示最后一个时间点上的取值
                     plotymargin=0.0, # 用于设置子图 y 轴的边界
                     plothlines=[a,b,...], # 用于绘制取值为 a,b,... 的水平线
                     plotyticks=[], # 用于绘制取值为 a,b,... y轴刻度
                     plotyhlines=[a,b,...], # 优先级高于plothlines、plotyticks，是这两者的结合
                     plotforce=False, # 是否强制绘图
                     plotmaster=None, # 用于指定主图绘制的主数据
                     plotylimited=True,
                     # 用于设置主图的 y 轴边界，
                     # 如果True，边界只由主数据 data feeds决定，无法完整显示超出界限的辅助指标；
                     # 如果False, 边界由主数据 data feeds和指标共同决定，能确保所有数据都能完整展示
     )
     ```
   * 请自行尝试不同配置

## “浏览器”的配置

1. `autostart`
   * `bool`
   * 是否自动打开浏览器。**live mode 和 参数优化模式时都不会自动打开浏览器**[^4]
   * `BacktraderBokeh(autostrart=True)` 和 `BacktraderBokehOptBrowser(autostrart=True)`
2. `address`
   * `str`
   * 网页地址。如果是当地运行 Backtrader_Bokeh，则配置如下
   * `BacktraderBokehOptBrowser(address='localhost', port=8889` (**参数优化模式**) 和 `cerebro.addanalyzer(address='localhost', port=9889)` (**Live Mode**)
3. `port`
   * `int`
   * 网页端口。默认是 80 端口，如果被占用可自行设置其他端口
   * `BacktraderBokehOptBrowser(address='localhost', port=8889` (**参数优化模式**) 和 `cerebro.addanalyzer(address='localhost', port=9889)` (**Live Mode**)

[^1]: 有些选项丢弃了，原因是不适合。请自行摸索，本文难以详述
[^2]:  本文仅仅列举部分，除了 Backtrader_Bokeh 特有选项外，更多详细请参考 https://backtrader.com/docu/plotting/plotting/
[^3]:  关于 plotlines 请查阅 https://backtrader.com/docu/plotting/plotting/ 
[^4]: 在常规模式下通过 BacktraderBokeh(autostrart=) 传参无效果，该模式默认自动打开浏览器