# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- More, waiting for update

## [0.1.0] - 2022.05.23
### Added
- Can set special transaction rules
- Add more content of order when printing

### Fixes  
- Fix lots of bug

### Changed
- Modify rendered HTML
- Update wiki

## [0.0.9] - 2022.05.13
### Added
- In addition to OHLC, additional datafeed line can be plotted

### Fixes  
- None

### Changed
- None

## [0.0.8] - 2022.05.08
### Added
- Fix many bugs of Backtrader through Backtrader_Bokeh's patch, instead of modifying the source code of backtrader

### Fixes  
- fix `autostart` bug in **Live Mode**
- Other bug

### Changed
- A set of easier and clearer Api 
- Update all demo according to new api
- Update README.md
- Update wiki homepage include **en** and **cn**

## [0.0.7] - 2022.05.02
### Added
- Can customize the style of each data. Besides passing in the `style`  like `BacktraderBokeh(style='bar')` , you can do the following
    ```
    data = bt.feeds.YahooFinanceCSVData(
        ...
    )
    data.plotinfo.plotstyle = 'bar'    
    ```

### Fixes  
- fix : TypeError: unhashable type: 'slice' for pandas

### Changed
- None

## [0.0.6] - 2022.04.13
### Added
- In live mode,  the option `autostart = True`  can open the browser automatically

### Fixes  
- Fixed hover-tooltips bug: now, more data lines can be added exactly using the scheme option hover_tooltip_config!

### Changed
- Update README.md and CHANGELOG.md

## [0.0.5] - 2022.04.10
### Added
- None

### Changed
- None

### Removed
- None
  
### Fixes
- Because of optbrowser address and port assignment mistake problem, if port 80 is occupied, the web page will not be opened in the optimization mode
- Very imortant, fixed the legend can't be displayed in the observer or indicators's figuer
