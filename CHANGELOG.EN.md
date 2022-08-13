# Changelog
All notable changes to this project will be documented in this file. Please refer to the [project wiki](https://github.com/iniself/backtrader_bokeh/wiki) for detail.

Telegram Channel: [Aui_Say](https://t.me/aui_say)  
Discord Server: [Aui and Friends](https://discord.gg/dhp8uzKSfR)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- More, waiting for update

## [0.7.0] - 2022.08.06
### Commit Hash
- 39ffb44123cb47677dc7c822b74700a228d78159

### Added
- Added keyboard operation: now you can zooming in or out through the combination of up direction keys(or down) and shift|option|control: this function is available without any configuration.
- Added keyboard operation: now you can translate graphic through the combination of left direction keys(or right) and shift|control: this function is available without any configuration.
- Added keyboard operation: now you can translate graphic through mouse wheel: this function is available without any configuration.

### Fixes
- None

### Changed
- Update doc

## [0.6.0] - 2022.07.13
### Commit Hash
- 2df5faa8a24856bd410d3230c0948cae1bed6d28

### Added
- Support keyboard operation: now you can operate crosshair and tooltip through left and right direction keys and key combinations: this function is available without any configuration.

### Fixes
- Fixed the bug that the crosshair color setting in the scheme is invalid.

### Changed
- Update doc

## [0.5.0] - 2022.06.28
### Commit Hash
- 07179f756c5a349bac693f674d744998613e9f45

### Added
- ConfigTab: one configure panel. You can customize your own backtrader through configuration_ Bokeh, These configuration is global. Once you configure it, all new projects will adopt this configuration by default.

### Fixes
- Fix some bug

### Changed
- Update doc

## [0.2.6] - 2022.06.16
### Commit Hash
- cb3d648a254f349fec15f4dd6a38e21189be7028

### Added
- None

### Fixes
- None

### Changed
- The schemes `Black` is alias of `Blackly`,  and  `White`  is alias of  `Tradimo`

## [0.2.0] - 2022.06.13
### Commit Hash
- dd5b2954fc9aa7fb2f27d7aa8bf4ba3bc8a2956d

### Added
- New feature `Logtab`: the tab can display multiple log  according to different levels and styles. See wiki for details

### Fixes
- None

### Changed
- None

## [0.1.2] - 2022.06.08
### Commit Hash
- e37eb7bd32058815c20cb048d802268cf0b89fae

### Added
- None

### Fixes
- None

### Changed
- Set the default values of some options as follows, so that users can get the same result with fewer parameters
    * Change the default dark theme to the default light theme
    * `autostart` default is `True`. You no longer need to pass in `autostart` to automatically open the browser
    * `force_plot_legend` default is `True`。You no longer need to pass in `force_plot_legend` to automatically fix the legend bug

## [0.1.1] - 2022.06.08
### Commit Hash
- a27dd6aea434922d681005d72d70ffc55eb050de

### Added
- None

### Fixes
- None

### Changed
- Modify html style
- Update doc

## [0.1.0] - 2022.05.31
### Commit Hash
- 987bc8fa634ce8e4513d993493ab30be980a39d6

### Added
- Add resources option
- More analyzers can be displayed in Analyzers Tab

### Fixes
- Fix lots of bug

### Changed
- Update wiki

## [0.1.0] - 2022.05.23
### Commit Hash
- bcc19c0c0268e87bedcd31f1fe5d966b9743a155

### Added
- Can set special transaction rules
- Add more content of order when printing

### Fixes  
- Fix lots of bug

### Changed
- Modify rendered HTML
- Update wiki

## [0.0.9] - 2022.05.13
### Commit Hash
- 45bd077ba5d474fd36ac5336f6e8209bcb415744

### Added
- In addition to OHLC, additional datafeed line can be plotted

### Fixes  
- None

### Changed
- None

## [0.0.8] - 2022.05.08
### Commit Hash
- e8af78183190190c1e6a19b6ab9380115b1bda3b

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
### Commit Hash
- e481f4d7972203e359999a7f6e3d76733788218f

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
### Commit Hash
- e3b4bff790dfb7216409a552baf7ea3e8f2ffe26

### Added
- In live mode,  the option `autostart = True`  can open the browser automatically

### Fixes  
- Fixed hover-tooltips bug: now, more data lines can be added exactly using the scheme option hover_tooltip_config!

### Changed
- Update README.md and CHANGELOG.md

## [0.0.5] - 2022.04.11
### Commit Hash
- e32927931318932b318beb07f13d1b8c592d981b

### Added
- None

### Changed
- None

### Removed
- None
  
### Fixes
- Because of optbrowser address and port assignment mistake problem, if port 80 is occupied, the web page will not be opened in the optimization mode
- Very imortant, fixed the legend can't be displayed in the observer or indicators's figuer

## [0.0.1] - 2022.04.10
### Commit Hash
- e11863504b7948c2bb9743313ba66279eedf2031

### Added
- init repo
- Implement the basic functions of Backtrader_Bokeh: use bokeh as the backend of Backtrader
- init doc: `README.md`，`CHANGELOG.md`，`WIKI.EN.md`，`WIKI.ZH.md`

### Changed
- None

### Removed
- None
  
### Fixes
- None