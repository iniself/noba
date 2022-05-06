# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Waiting for update

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
- 

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
