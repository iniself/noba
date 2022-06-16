# 更新日志
本项目比较重要的更新内容将会记录在此文件中，详细功能介绍请查阅项目 [wiki](https://github.com/iniself/backtrader_bokeh/wiki/wiki-zh)

QQ 群：908547278  
TG：[Aui_Channel](https://t.me/aui_say)   
Discord Server: [Aui and Friends](https://discord.gg/dhp8uzKSfR)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [未发行]
- 等待更新

## [0.2.6] - 2022.06.16
### 提交Hash
- cb3d648a254f349fec15f4dd6a38e21189be7028

### 增加
- 无

### 修正
- 修正一些已知 bug

### 改变
- 为主题`Blackly`, `Tradimo`分别取别名`Black`, `White`

## [0.2.0] - 2022.06.13
### 提交Hash
- dd5b2954fc9aa7fb2f27d7aa8bf4ba3bc8a2956d

### 增加
- 增加 `Logtab` 的功能，能按照不同级别和不同样式显示多次 log 信息。详见 wiki

### 修正
- 修正一些已知 bug

### 改变
- 无

## [0.1.2] - 2022.06.08
### 提交Hash
- e37eb7bd32058815c20cb048d802268cf0b89fae

### 增加
- 无

### 修正
- 无

### 改变
- 改变一些参数的默认值如下，方便用户传入更少参数就能实现同样的功能
    * 样式从默认的深色主题修改为默认浅色主题
    * `autostart` 默认值设置为 `True`。不再需要传入 `autostart` 就能自动打开浏览器
    * `force_plot_legend` 默认值设置为 `True`。不再需要传入 `force_plot_legend` 就能修订 Backtrader 图例`legend` 显示不全的问题

## [0.1.1] - 2022.06.08
### 提交Hash
- a27dd6aea434922d681005d72d70ffc55eb050de

### 增加
- 无

### 修正
- 无

### 改变
- 修改 HTML 样式
- 更新 Github 文档

## [0.1.0] - 2022.05.31
### 提交Hash
- 987bc8fa634ce8e4513d993493ab30be980a39d6

### 增加
- 通过参数可以设定如何加载 Bokeh 的资源文件
- 增加了一个 analyzers 并且能够把结果自动在 Analyzers 标签页中进行显示，而不再需再通过命令行进行结果打印

### 修正
- 修正大量已知 Bug

### 改变
- 更新了 wiki 文档

## [0.1.0] - 2022.05.23
### 提交Hash
- bcc19c0c0268e87bedcd31f1fe5d966b9743a155

### 增加
- 能够针对特定市场的交易规则进行设置，比如涨跌停等
- 当打印订单信息时会展示更多信息，比如因为交易规则而导致订单的一部分被取消的信息

### 修正  
- 修正大量已知 Bug

### 改变
- 修改 HTML 框架
- 更新 wiki 文档

## [0.0.9] - 2022.05.13
### 提交Hash
- 45bd077ba5d474fd36ac5336f6e8209bcb415744

### 增加
- 数据源中除了 OHLC 等默认信息，你手动添加的额外信息也会被自动绘制出来。并且支持对绘制样式进行设置

### 修正  
- 无

### 改变
- 无

## [0.0.8] - 2022.05.08
### 提交Hash
- e8af78183190190c1e6a19b6ab9380115b1bda3b

### 增加
- 通过补丁模式修正一些属于 Bactrader 的 Bug，并且是借助 Backtrader_Bokeh 而不是直接修改 Bakctrader 源码

### 修正  
- 修正 `autostart` 选项在 **Live Mode** 时的 Bug
- 其他已知 Bug

### 改变
- 整合 Backtrader 和 Backtrader_Bokeh 的 Api，使整个 Api 看上去更加干净和整洁
- 用新 Api 更新了所有 Demo 文件
- 更新 README.md
- 更新**WIKI.EN.md**和**WIKI.ZH.md**

## [0.0.7] - 2022.05.02
### 提交Hash
- e481f4d7972203e359999a7f6e3d76733788218f

### 增加
- 能够对不同数据源分别通过 `BacktraderBokeh(style='bar')` 定制样式，如下
    ```python
    data = bt.feeds.YahooFinanceCSVData(
        ...
    )
    data.plotinfo.plotstyle = 'bar'    
    ```

### 修正
- 修正Bug : TypeError: unhashable type: 'slice' for pandas

### 改变
- 无

## [0.0.6] - 2022.04.13
### 提交Hash
- e3b4bff790dfb7216409a552baf7ea3e8f2ffe26

### 增加
- 在 `Live Mode` 和 `Optstrategy Mode`,  通过传入 `autostart = True`  选项能够自动打开浏览器

### 修正  
- 修正 hover-tooltips Bug：现在真正能够通过传入 `hover_tooltip_config` 选项把不同图区的数据添加到各个 tooltips 中！

### 改变
- 更新 README.md 和 CHANGELOG.md

## [0.0.5] - 2022.04.11
### 提交Hash
- e32927931318932b318beb07f13d1b8c592d981b

### 增加
- 无

### 改变
- 无

### 删除
- 无
  
### 修正
- 由于 `optbrowser address` 和 `port` 分配错误, 当 80 端口被占用时，`optimization mode` 模式会运行出错
- 非常重要！由于 Backtrader 自身问题会导致在`observer` 和 `indicators` 图区中 图例 (legend) 不能完整显示，通过 `force_plot_legend = True` 可以强制显示所有图例

## [0.0.1] - 2022.04.10
### 提交Hash
- e11863504b7948c2bb9743313ba66279eedf2031

### 增加
- 初始化仓库
- 把已实现基本功能的 Backtrader_Bokeh 进行提交：用 Bokeh 作为 Backtrader 的绘图可视化后端
- 初始化各种文档，包括 `README.md`，`CHANGELOG.md`，`WIKI.EN.md`，`WIKI.ZH.md`

### 改变
- 无

### 删除
- 无
  
### 修正
- 
