用过 Backtrader 都知道它的可视化是用的 `matplotlib` , 好处是开箱即用，因为 `matplotlib` 是 Backtrader的默认可视化后端，但缺点就是 `matplotlib`的绘图还是不够日常需要。说到图片文字的展示，有没有可能在浏览器里展示策略数据和分析结果的呢？答案就是 Backtrader和 Bokeh 的结合产品：[Backtrader_Bokeh](https://github.com/iniself/backtrader_bokeh)。 在 [示例](https://iniself.github.io/backtrader_bokeh/) 这里可以感受 Backtrader_Bokeh 的可视化效果。 *\* 只展示部分示例，全部示例请自行运行 [demos](https://github.com/iniself/backtrader_bokeh/tree/main/demos/) 下的代码*

`Backtrader_Bokeh`继承自 [backtrader_plotting](https://github.com/verybadsoldier/backtrader_plotting) 和 [btplotting](https://github.com/happydasch/btplotting) ，对两者的问题做了修正并且计划推出更加适合量化框架 Backtrader 的一系列新特性。欢迎来 github 上关注及讨论，并积极通过 **star**、**issue** 等方式来支持该项目。同时推荐 **Aui 团队**的另外两个产品：[Aui(在线相册+应用)](https://aui.photos/aui/about/)、[检查指标小帮手(微信小程序)](https://aui.photos/helper/about/)

QQ群：**908547278**  
TG：[Aui_Channel](https://t.me/aui_say)  
Discord Server: [Aui and Friends](https://discord.gg/dhp8uzKSfR)  
  
ETH：**0x0275779f70179748C6fCe1Fe5D7638DfA7e3F986** （感谢赞助我们一杯咖啡）

# 安装
```
pip install git+https://github.com/iniself/backtrader_bokeh
```
*\* 如果在依赖包安装和使用过程中出现错误提示，建议创建新 Python 环境安装 Backtrader_Bokeh。同时避免如下安装方式：*
```
pip install --force-reinstall git+https://github.com/iniself/backtrader_bokeh
```

# 快速上手

使用 Backtrader_Bokeh 非常容易，它对原 Backtrader 是无侵入的，你只需要在你的 Python 文件中如下引入就可以获得 Backtrader_Bokeh 所带来诸多好处。包括：
1. 一个 Bokeh 可视化的后端
2. 通过**补丁方式**增加 Backtrader 的功能及解决 Backtrader 的错误。*\* 不会修改 Backtrader 的原文件*
3. 更简单的 Api 调用
   
```python
from backtrader_bokeh import bt
# import backtraer as bt  此引入已经不再需要
```

有多种方式使用 Backtrader_Bokeh 。本文只介绍 3 种，其他更多你可以参考 [Demo](https://github.com/iniself/backtrader_bokeh/tree/main/demos):

## 把  Backtrader_Bokeh 当作分析器使用（适用于实时数据模式）

* 使用默认 80 端口：

  ```python
  from backtrader_bokeh import bt
    ...
    ...
  
  cerebro = bt.Cerebro()
  cerebro.addstrategy(MyStrategy)
  cerebro.adddata(LiveDataStream())
  cerebro.addanalyzer(bt.analyzers.Live, force_plot_legend=True, autostart=True)
  cerebro.run() # 注意如果上面添加的数据不是实数数据，则打开浏览器失败
  ```

* 如果你的 80 端口被占用，比如你同时运行了 `nginx`，此时需要指定其他端口启动 Backtrader_Bokeh：

  ```python
  cerebro.addanalyzer(bt.analyzers.Live, address="localhost", port=8889, force_plot_legend=True, autostart=True)
  ```

## 把  Backtrader_Bokeh 实例化为 Plot 对象

* 普通模式（常用）：对一套策略参数的回测

  ```python
  from backtrader_bokeh import bt
    ...
    ...
    
  plot = bt.Bokeh(style = 'bar', scheme=bt.schemes.Black(), force_plot_legend=True) # bt.schemes.Black 是样式主题
  cerebro.plot(plot, iplot=False) # 如果你在 Jupyter 中运行，需要传入 iplot 参数
  ```

  

* 参数优化模式：对多套策略参数的回测。可以选择在不同参数下展示策略的效果

  ```python
  from backtrader_bokeh import bt
    ...
    ...
  	
  cerebro.optstrategy(MyStrategy, buydate=range(40, 180, 30))  	
  result = cerebro.run(optreturn=False)
  
  b = bt.Bokeh(style='bar', scheme=bt.schemes.White(), force_plot_legend=True)
  browser = bt.Opt(b, result, address='localhost', port=8889, autostart= True)
  browser.start()
  ```

# 新特性
**会在这里集中介绍一些不好单独放入其他内容的 Backtrader_Bokeh 内容**
* **额外的 DataFeeds 数据如何被绘制：**  
  通过继承 DataFeeds 类的方法，然后修改 lines 参数，你可以增加 DataFeeds 数据列，但 Backtrader 并不会绘制这些列数据，你只能在策略中使用它。从 Backtrader_Bokeh `v0.0.9` 版本后，你可以实现这一绘图功能，并且不需要做额外的工作
  ```python
  from backtrader_bokeh import bt
  class MyYahooData(bt.feeds.YahooFinanceCSVData):
    lines = ('extradata',) #增加额外的数据线，这是 Backtrader 需要的设置
    extradataline = {  #注意这里是lines中字符 + line 这个后缀。如果不设置或则错误将不会生效，但依然能按默认方法绘制出 extradata 这条数据线
        # plotinfo 中的选项都可以在下面进行设置
        'plotname':"linename",  
        'subplot':True
        ...
    }    
    ...
  ```
  通过上面可以看到，绘制附加的数据线不需要你做任何额外的工作，除非你想通过 `extradataline` 这个选项来定制数据线的绘制方式，一般来说，不设置就默认的也可以

* **设置特殊的交易规则：**   
  不同的证券市场有不同的规则：比如中国大陆的 A 股有涨停限制。从 Backtrader_Bokeh `v0.1.0` 版本后支持对这些交易规则进行设置。目前可以设置的是“涨停限制”、“是否可以做空”和“是否有最小购买数限制”。如果不做如下设置，默认的规则是**没有涨停限制**、**可以做空**和**无最小购买数限制**
  ```python
  cerebro.broker.set_rule({
    'limit':0.2, # 20%的涨跌停限制
    'short':False, #不能做空
    'least':100, #购买时每手的最小单位
  })
  ```
  * 当 `'limit':0.2` 时，如果遇到涨停行情不能买入股票，遇到跌停行情不能卖出股票。*\*虽然涨跌停时当日不能交易股票，但该订单会持续有效，如果你想限制该订单有效期，则传入 **`valid`** 选项，举例：`self.buy(size=1000, valid=timedelta(3))`* 

  * 当 `'short':False` 时，仅能在**已有**的仓位数内卖出证券。举例：如果你的仓位数是 100 手，但你的卖单是 150 手，则会自动按照 100 手的卖单进行交易，多出的 50 手**自动作废**。当仓位数是 0 时，则整个卖单作废。*\*打印 `order` 时增加 `Adj Size` 显示调整后的订单数量*

  * 当 `'least':100` 时，购买数量只能是该参数的整数倍。举例：订单数量是680，那么最终会成交的数量是 6 手 600 份，多出的 80 份会**自动作废**。*\*打印 `order` 时增加 `Adj Size` 显示调整后的订单数量*  

* **LogTab：**   
  除了可视化图表外，很多时候我们都需要打印一些额外的信息，此时通常的办法是用 `print` 在命令行中把信息打印出来，比如 `order` 的历史信息。但这种打印非常不友好，所以我们把要打印的信息从命令行迁移到 LogTab 这个页面，通过网页来展示你想要的内容：
  * 不同的打印结果会在 LogTab 页面的不同表格中展示
  * 支持显示相关信息，比如本次打印的 title 等
  * 支持不同级别的 log 控制。*\*CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET*
  * 可以对日志进行排序等操作
  * 其他
  
  启用 LogTab：
  ```python
  from backtrader_bokeh import bt

  class MyStrategy(bt.Strategy):
      def next(self):
          open([self.data.open[0]]) # 默认是用 info 来打印
          close.info([self.data.open[0]])

  if __name__ == '__main__':
      # get logger with default log level INFO
      open = bt.getlogger(['open'], name='Open Price') # name 将显示为表格的标题
      close = bt.getlogger(['close'], name='Close Price',  stdout=True, level=logging.DEBUG) # stdout 控制是否同时在命令行打印结果。默认 False。level 是控制日志等级，详情参阅 logging 模块
      ...
      cerebro.run()

      p = bt.Bokeh(style='bar', use_default_tabs=False,  tabs=[bt.tabs.LogTabs(2)]) # 数字2是控制 Logtab 页面一行会显示几个表格
      cerebro.plot(p)    
  ```
* **ConfigTab：**  
  由于 Backtrader_Bokeh 可配置的选项比较多，所以用户在调用函数时经常需要传入大量参数，并且每写一个回测程序就要传一次。虽然我们已经为 Backtrader_Bokeh 默认了很多初始值，但这种优化还是不够。于是我们推出了 **ConfigTab** 这个配置面板。这个配置是全局性的，一旦你进行了配置，所有新建项目都会默认采用这个配置。**用户应该专心去做他们的策略研究，而配置就交给 ConfigTab**

  * 新安装的 Backtrader_Bokeh 会默认开启 ConfigTab，你可以通过配置来定制你自己的 Backtrader_Bokeh
  * 在配置面板的 `tabs` 你可以点击关闭 ConfigTab。这样下次启动 Backtrader_Bokeh 时就不会再自动加载 ConfigTab
  * 关闭后，如果想重新进行配置，只需如下方式传入参数 *\*这其实就是在本文档里 “系统和主题的绘图选项 ”中的内容*
    ```python
    bt.Bokeh(tabs=[bt.tabs.ConfigTab])
    ```
  * 该全局配置优先级低于函数传参。也就是说通过 ConfigTab 进行全局配置后，依然可以在具体项目中通过函数传参来改变 Backtrader_Bokeh 的行为
  * 其他更多内容请自行探索

* **支持键盘操作**  
  自从 v0.6.0 后，Backtrader_Bokeh 开始逐步支持键盘操作。键盘操作能让你更加准确和快捷地操作你的回测结果。这项功能无需做任何配置，开箱即用

  * 支持通过左右键及组合键来操作 Crosshair 和 tooltip。你有三种操作速度：最慢的是`← →`，较快的是 `Option` + `← →`，最快的是 `Shift` + `← →`
  * 支持通过 `Shift` + `Control` + `← →` 组合键来平移图形。 *\*也支持通过鼠标滚轮来平移图像，但需要先选中 `Wheel Pan` 工具*
  * 支持通过组合键对图形进行放大(Zoom Out)和缩小(Zoom In)。有四种模式：
    1. `Shift` + `↑ ↓` 沿横轴快速放大(或缩小)
    2. `Shift` + `Option` + `↑ ↓` 沿横轴慢速放大(或缩小)
    3. `Shift` + `Ctrl` + `↑ ↓` 沿横轴和纵轴快速放大(或缩小)
    4. `Shift` + `Ctrl` + `Option` + `↑ ↓` 沿横轴和纵轴慢速放大(或缩小)

# 参数列表

先介绍 Backtrader_Bokeh 涉及到需要传入参数几个函数：

* Live Mode 时
  ```python
  cerebro.addanalyzer(...)
  ```
* 常规回测模式时
  ```python
  bt.Bokeh(...)
  ```
* 参数优化模式时
  ```python
  bt.Bokeh(...)
  bt.Opt(...)
  ```

本文从如下几个方面介绍 Backtrader_Bokeh 参数配置：

* 该参数的类型
* 该参数的用途
* 该参数适合哪些函数。本文除了特殊说明外，**适合 `bt.Bokeh()` 的参数同样适合 `cerebro.addanalyzer()`**

## 前置知识

回忆一下 **Backtrader** 自带的绘图选项：
* Options affecting the plotting behavior of the entire object：对象的绘图选项，该配置对应 **plotinfo**。*\* 比如一个指标就是一个对象，它会自带默认的**plotinfo**(控制这个指标的整体绘图) 和 **plotlines**(控制每条 lines 的绘图)*
* Options affecting the plotting behavior of individual lines：该配置对应绘图对象的 **plotlines** 配置
* Options affecting the SYSTEM wide plotting options：Backtrader 最上层的配置和某个主题的配置

Backtrader_Bokeh 也是以这样的分类来配置绘图选项的。在继承了大部分 Backtrader 配置的前提下，Backtrader_Bokeh 根据 Bokeh 的需要还增加了大量配置。简言之，`Backtrader_Bokeh Options = Backtrader Options + Bokeh Options`


##  “系统”和“主题”的绘图选项

1. **style**
   * `str`
   * 控制主图显示的类型。`single` 显示收盘价的线条图，`bar` 或则 `candle`显示包含了开盘价、收盘价、最高价、最低价的 K 线柱状图。另外，从 `v0.07` 版本后，还可以分别为每一个数据源定制样式：
      ```python
        data = bt.feeds.YahooFinanceCSVData(...)
        data.plotinfo.plotstyle = 'bar' 
      ```
   * `bt.Bokeh(style='bar')`
2. **resources**
   * `str`
   * 除非如下显示传入该选项，Backtrader_Bokeh 默认加载当地 Bokeh 的资源文件而不是通过 CDN 网络：
   * `bt.Bokeh(resources='cdn')`
3. **scheme**
   * `object`
   * 告诉 Backorder_Bokeh 绘图时选择哪个主题：目前有两个主题 Black（深色主题）和 White（浅色主题）。**默认是浅色主题**
   * `bt.Bokeh(scheme=bt.schemes.Black())`
4. **filename**
   * `str`
   * 在常规回测时，用指定的文件名代替 Backtrader_Bokeh 默认的临时文件名。 **仅适应于生成的静态网页，所以在 “Live Mode” 和“参数优化” 时此选项无效**
   * `bt.Bokeh(filename='yourfile.html')`
5. **output_mode**
   * `str`
   * 在常规回测时:  
     `save`：只保存文件，不打开浏览器  
     `show`：保存文件同时打开浏览器  
     `memory`：不保存文件，但返回模型
6. **use_default_tabs**
   * `bool`
   * 如果设置成 `true` ，则 Backtrader_Bokeh 默认的网页 tab 会被添加进去
   * `bt.Bokeh(use_default_tabs=False)`
7. **tabs**
   * `list`
   * 在网页中希望添加的 tab。当 `use_default_tabs=False` 时生效
   * `bt.Bokeh(tabs=[bt.tabs.AnalyzerTab])`
8. **show_headline**
   * `bool`
   * 是否显示页面标题
   * `bt.Bokeh(show_headline=False)`
9. **headline**
   * `str`
   * 改变页面标题。默认是 "Backtrader Results"
   * `bt.Bokeh(headline='Your backtrader')`
10. **force_plot_legend**
    * `bool`
    * 是否强制显示所有图例(legend)。当遇到有图列不显示时设置成 `True`。**默认值是 True**
    * `bt.Bokeh(force_plot_legend=True)`
11.  **hover_tooltip_config**
     * `str`
     * 控制鼠标指向图形时的提示内容。在没有传入该参数时，Backtrader_Bokeh 会默认用该数据类型（Data Feed、Indicators、Observer）的默认方式提示。比如 Data Feed 会显示时间、开盘价、收盘价、最高价、最低价、交易量，但如果想显示额外数据，就需要用到这个选项
     * `IND-DATA`: 把 Indicators 的数据添加到主图 (Data Feed) 的 tooltip 
     * `DATA-OBS`: 把主图数据添加到 Observer 
     * `IND-OBS`:   把 Indicators 的数据添加到 Observer
     * ……
12.  **plotconfig**
     * `dict`
     * 用于控制 **局部绘图** 的参数配置（具体见**局部绘图选项**）。Backtrader_Bokeh 的 `plotconfig` 相当于 [Plotting - Backtrader](https://backtrader.com/docu/plotting/plotting/)  中的 **Object-wide plotting options**
     * ```python
        plotconfig = {
          'id: sm5': dict(
              subplot=False,
              plotname='sm5 indicator'
          )
        }
      
        bt.Bokeh(plotconfig=plotconfig)
       ```
13.  **usercolumns**
     * `dict`
     * 自定义列可以添加到结果列表中，用于显示结果中感兴趣的特殊属性。要使用它，需要传递一个字典，其中键是列的标签，值是一个可调用的值，该值需要一个优化结果来计算属性。该参数只适用于**参数优化模式**
     * ```python
       def get_pnl_gross(strats):
          a = strats[0].analyzers.tradeanalyzer.get_analysis()
          return a.pnl.gross.total if 'pnl' in a else 0
      
        b = bt.Bokeh(style='bar', scheme=bt.schemes.White())
        browser = bt.Opt(b, result, usercolumns=dict(pnl=get_pnl_gross), sortcolumn='pnl', sortasc=False)
        browser.start()
        ```
14.  **其他主题参数**
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
     * 主题参数可以直接在 `cerebro.addanalyzer()` 和 `bt.Bokeh()`中传入这些参数。或则可以在主题构建函数中传入：
       * ```python
         bt.Bokeh(hovertool_timeformat='%F %R:%S')
          ```
       * ```python
         bt.Bokeh(scheme=Black(hovertool_timeformat='%F %R:%S'))
          ```
        
## “局部绘图”选项

在 **前置知识** 中已经说过 局部选项 就是针对每个对象（比如某个指标）的 **plotinfo** 和 **plotlines**  的设置。在 Backtrader 配置此选项有 三种方式：
1. **通过继承类：**
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
2. **传参修改：**
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
3. **Backtrader_Bokeh 多了一种可以在一个地方处理所有对象绘图参数的方法：**
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
**局部绘图**的部分选项 *\* 只列举 plotinfo，关于 plotlines 的配置请自行查阅Backtrader*：
1. **plot**
   * `bool`
   * 是否绘制此图
   * `plot=True`
2. **subplot**
   * `bool`
   * 是否绘制成子图，否则将在主图中统一显示
   * `subplot=True`
3. **plotmaster**
   * `object`
   * 用哪个绘图对象作为自己的主图。比如默认情况下，indicators 是和 主图（股价、交易量）绘制在一起。通过如下代码可以把 indicators 单独绘制
   * ```python
     class MyStrategy(bt.Strategy):
         def __init__(self):
             self.sma5 = bt.indicators.SMA(period=5, subplot=True)
             self.sma10 = bt.indicators.SMA(period=10, plotmaster=sma5)
     ```
4. **plotname**
   * `str`
   * 图例名字
   * `plotname='somename'`
5. **plotorder**
   * `int`
   * 各绘图对象在页面上的绘图顺序。数字越小则越在上面。默认所有为`0`。 下面代码会让 Observer 绘制在 Data Feed (股价、交易量等的主图)
   * ```python
     class MyBroker(bt.observers.Broker):
         def __init__(self):
             self.plotinfo.plotorder = 5
             
     cerebro.addobserver(MyBroker)
     ```
6. **其他局部绘图选项**
   * ```python
     plotinfo = dict(plot=True, # 是否绘制该对象
                     subplot=True, # 是否绘制成子图
                     plotname='', # 图形对象名称
                     plotorder=0, # 各子图绘制的顺序
                     plotlinelabels=False, # 主图上曲线的名称
                     plotlinevalues=True, # 是否显示曲线最后一个时间点上的值
                     plotvaluetags=True, # 是否以卡片形式在曲线末尾展示最后一个时间点上的值
                     plotymargin=0.0, # 用于设置子图 y 轴的边界
                     plothlines=[a,b,...], # 用于绘制取值为 a,b,... 的水平线
                     plotyticks=[], # 用于绘制取值为 a,b,... y轴刻度
                     plotyhlines=[a,b,...], # 优先级高于plothlines、plotyticks，是这两者的结合
                     plotforce=False, # 是否强制绘图
                     plotmaster=None, # 用于指定主图绘制的主数据源
                     plotylimited=True,
                     # 用于设置主图的 y 轴边界，
                     # 如果True，边界只由主数据 data feeds决定，无法完整显示超出界限的辅助指标；
                     # 如果False, 边界由主数据 data feeds和指标共同决定，能确保所有数据都能完整展示
     )
     ```
   * 请自行尝试不同配置

## “浏览器”的配置

1. **autostart**
   * `bool`
   * 是否自动打开浏览器。**适合“参数优化模式” 和 “Live Mode”，因为该两种模式都不会自动打开浏览器**。**默认值是 True**
   * `bt.Opt(autostart=True)`(**参数优化模式**) 和 `cerebro.addanalyzer(autostart=True)`(**Live Mode**)
2. **address**
   * `str`
   * 网页地址。如果是当地运行 Backtrader_Bokeh，则配置如下
   * `bt.Opt(address='localhost', port=8889` (**参数优化模式**) 和 `cerebro.addanalyzer(address='localhost', port=9889)` (**Live Mode**)
3. **port**
   * `int`
   * 网页端口。默认是 80 端口，如果被占用可自行设置其他端口
   * `bt.Opt(address='localhost', port=8889` (**参数优化模式**) 和 `cerebro.addanalyzer(address='localhost', port=9889)` (**Live Mode**)