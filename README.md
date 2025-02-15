# Bing-Rewards

<div align="center">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/bing-rewards?style=flat-square&label=Python&logo=python&logoColor=yellow">
<a href="https://pypi.org/p/bing-rewards/"> <img alt="PyPi" src="https://img.shields.io/pypi/v/bing-rewards?label=PyPI&style=flat-square&logo=pypi&logoColor=yellow"></a>
<a href="https://pypi.org/p/bing-rewards/"> <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/bing-rewards?style=flat-square&label=Downloads&color=orange"></a>
<br>
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/bing-rewards?style=flat-square&label=License&color=blueviolet">
</div>

### A CLI app to perform Bing searches
Please submit an issue or pull-request if you have an idea for a feature

- [Features](#features)
- [Install](#installation)
- [Usage](#usage)
- [Config](#options)
- [Development](#development--contribution)

## **Features**

* Enter random search queries into your browser a la Auto Hotkey.
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* Install as self-contained python application with minimal dependencies (`pynput`)
* Fine tune delay and set browser executable with [config](#configuration) at `$XDG_CONFIG_HOME` or `%APPDATA%` on Windows
* Not intended as a automated or headless service. Simply assists with what would regularly be a manual task.

## ⚠️**Here Be Dragons**
This was originally created in a different age, when Bing & MS was much simpler and less bloated with AI ~~slop~~ tools. Users have reported a wide variety of success on whether this method works at all with the new systems. See some of the pinned or closed issues for reports from others that may improve success. I maintain the *code* in a working state as an excersie in Python packaging, but do *not* personally use the utility, and **cannot guarantee this method will even generate points anymore**! 

## **Installation**
Bing-rewards is a Python CLI utility application distributed on PyPI. You can install it however you prefer to manage Python applications on your system. I recommend `pipx`.

### With [`pipx`](https://pipx.pypa.io/stable/) or `pip`
```bash
pipx install bing-rewards
```
Will make the executable `bing-rewards` available on your PATH.
Look below or try the `--help` flag to see detailed usage.

**Recommended**: Use a virtual environment or [`pipx`](https://pypa.github.io/pipx/) to avoid polluting your global package path with executable apps. See: [pipx](https://pypa.github.io/pipx/)

### From releases
Download the latest release wheel and install with pip locally.

## **Dependencies**

- At least Python 3.10

- [pynput](https://github.com/moses-palmer/pynput) (installed with package). Used to control keypresses and type Bing search URLS.
⚠️: Bing-Rewards *will* take control away from the keyboard while running. **Pynput** performs key presses. i.e., it does not operate headless or in the background.

- `chrome` must be discoverable on the system PATH. [Download Google Chrome](https://www.google.com/intl/en/chrome/).
If your chromium based browser has a different name use the `--exe` flag with an absolute path to the browser executable to use (e.g. `--exe=$(which brave-browser)`). Also see the `"browser-path"` key in the [config](#configuration) file.

- To earn points from searching, you *must* also have logged into [bing.com](https://www.bing.com) with your Microsoft account at least once, to save cookies.

## **Usage**
Complete mobile and desktop daily points

`$ bing-rewards`

Run 10 searches with mobile user-agent in a new window

`$ bing-rewards -m -c10`

`$ bing-rewards --mobile --count=10`

Complete mobile and desktop daily points using specified chrome profile "Profile 1"

`$ bing-rewards --profile "Profile 1"`

Run searches sequentially across multiple Chrome profiles

`$ bing-rewards --profile "Default" "Profile 1" "Profile 2"`

Launches Chrome as a subprocess with special flags. Tested on Windows 10 and Linux (Ubuntu + Arch), however it should work on Mac OS as well.

⚠️Known Issue: No other instance of chrome.exe can be open when the script runs. Chrome prevents different user agents in each window. The script will run, but Chrome will not appear as Edge


## **Options**

Running with no options will complete mobile and desktop daily search quota.
The following options are available to change the default behavior.
Options supplied at execution time override any config.
| Flag                    | Option                                                                                |
| ----------------------- | --------------------------------------------------------------------------------------|
| `-h`, `--help`          | Display help and exit                                                                 |
| `-c`, `--count=N`       | Override the number of searches to complete                                           |
| `-d`, `--desktop`       | Only use desktop user agent                                                           |
| `-m`, `--mobile`        | Only use a mobile user agent                                                          |
| `-n`, `--dryrun`        | Do everything but type the search query                                               |
| `-b`, `--bing`          | Use this flag if Bing is already your default search engine. Bypasses constructing a bing.com URL |
| `--open-rewards`        | Open the rewards page at the end of the run                                           |
| `-X`, `--no-exit`       | Do not close the browser after completing a search                                    |
| `--load-delay`          | Override the time given to Chrome to load in seconds                                  |
| `--search-delay`        | Override the time between searches in seconds                                         |
| `--exe EXE`             | The full path of the Chrome compatible browser executable (Brave and Chrome tested)   |
| `--nowindow`            | Don't open a new Chrome window, just type the keys                                    |
| `--profile`             | Run searches using specified Chrome profile(s). Multiple profiles can be specified to run sequentially |
| `--ime`                 | Triggers Windows IME to switch to English input by pressing "shift"                   |

A config file is also generated in $XDG_CONFIG_HOME or %APPDATA% on Windows
where precise delay modifications can be made. If updates make changes to the default configs, you will have to remove and regenerate the file.

Example config `~/.config/bing-rewards/config.json`
```json
{
    "desktop_count": 30,
    "mobile_count": 20,
    "load_delay": 1.5,
    "search_delay": 2,
    "search_url": "https://www.bing.com/search?FORM=CHROMN&q=",
    "desktop_agent": "Mozilla/5.0 ... <snip>",
    "mobile_agent": "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) ... <snip>",
    "browser_path": "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
}
```
Delay timings are in seconds.  
Note: the format has slightly changed in version >= 3.0, so delete and regenerate accordingly.

## User agents

If interested, the following user agents are passed to Chrome using the `--user-agent` argument.
These are clearly defined at the top of `bing-rewards.py`.

Edge Browser on Windows 10 desktop:
> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edge/126.0.0.0

Mobile Edge Browser on Pixel 6 phone:
>  Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/AP2A.240605.024) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 Edge/121.0.2277.138


## Words:
The [keywords](https://web.archive.org/web/20220523083250/https://www.myhelpfulguides.com/keywords.txt) included in this repo where taken from this site
[https://www.myhelpfulguides.com/2018/07/19/bing-rewards-auto-searcher-with-python-3/](https://web.archive.org/web/20220331033847/https://www.myhelpfulguides.com/2018/07/19/bing-rewards-auto-searcher-with-python-3/).

This script provided the original inspiration but has since been completely rewritten and expanded.
The original author was contacted for the original source of keywords, but declined to respond

## Development & Contribution

This project uses [`hatch`](https://hatch.pypa.io/latest/) as the build backend for dependency management and packaging.

```
pipx install hatch
```

Then, fork the repo, clone and install the project and dependencies with `hatch env create`.

Install the defined pre-commit hooks: `hatch run pre-commit install`

Launch bing-rewards in the editable dev environment: `hatch run bing-rewards --help`

Feel free to open a PR with additional features or fixes.
