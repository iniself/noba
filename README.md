# What is Noba
## Noba means not only backtrader :)

**You can visit noba documentation for more information: [EN(coming soon)](#) | [中文](https://aui.photos/noba-doc/zh/)**

The core of Noba is an `ioc container`, through which you can create `BB` service, which based on [Backtrader](https://www.backtrader.com/)*(one quantitative backtest system)* and [Bokeh](https://bokeh.org/) *(use bokeh as the backend, Backtrader can get richer plot effects)*    *\* BB service would like to thank [backtrader_plotting](https://github.com/verybadsoldier/backtrader_plotting) and [btplotting](https://github.com/happydasch/btplotting) for providing the main code for using bokeh as the backend for the backtrader*
```python
from noba import core
bt =  core.make('bb')
```

Of course, you can also create your own services based container. Combined with **Pipeline System** and **Event System** (which can be created directly through containers), noba can enable your quantitative projects to work in a more engineering methods
```python
from noba import core
pipline =  core.make('pipeline')
cleaned_data = pipline.via("handle").send(raw_data).through([ChangeDataType, RepeatRowData, ExceptionData, MissingData]).then(lambda raw_data:raw_data)
```

```python
from noba import core
event = core.make('event')
db_event = event.hub(['read_database_complete'])
db_event.watch('read_database_complete', lambda data:..., always=True)
...
db_event.fire('read_database_complete')
```

More importantly, Noba can create database service objects (dber) through containers. This is a **Database Abstraction Layer**. Through configuration files(one json file) and unified one set of APIs, you can operate the most common databases

```python
from noba import core
dber =  core.make('db')
stocks = db.table('daily').where('Open==3578.73').or_where('High==3652.46').set_index('Date').get_except('OpenInterest')
```

# Getting Started
* Python >= 3.6 is required.
* Suggest using conda to manage virtual environments


## Installation

```bash
pip install noba
# or
pip install git+https://github.com/iniself/noba
```


## Init noba project

```bash
mkdir your_noba_project
cd your_noba_project
noba init
```

## Preparation
Here you can do some project configuration and write your own service provider, and so on. Please refer to the **NOBA documentation** for details

## Write strategy
```bash
vim main.py
```

Only give **Live Mode** example, about **Normal Mode** and **Optstrategy Mode** pls refer to **NOBA documentation**
* Add to cerebro as an analyzer **(Live Mode)**:
  ```python
  from noba import core
    ...
    ...
  bt = core.make('bb')
  cerebro = bt.Cerebro()
  cerebro.addstrategy(MyStrategy)
  cerebro.adddata(LiveDataStream()) # Note! Data is must Live Data
  cerebro.addanalyzer(bt.analyzers.Live, force_plot_legend=True, autostart=True)
  cerebro.run()
  # cerebro.plot() # do not run this line unless your data is not real-time
  ```

* If you need to change the default port or share the plotting to public:

  ```python
  cerebro.addanalyzer(bt.analyzers.Live, address="localhost", port=8889)
  ```

* Note! In Jupyter you can plut to a single browser tab with iplot=False:

  ```python
  cerebro.plot(plot, iplot=False)
  ```

# Demos

<https://iniself.github.io/noba/>

# Contact us
Telegram Channel: [Aui_Say](https://t.me/aui_say)
Discord Server: [Aui and Friends](https://discord.gg/dhp8uzKSfR)


# Sponsoring

If you want to support the development of noba, consider to support this project.

* ETH: 0x0275779f70179748C6fCe1Fe5D7638DfA7e3F986
