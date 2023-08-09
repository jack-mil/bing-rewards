# Bing-Rewards

<div align="center">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/bing-rewards?style=flat-square&label=Python&logo=python&logoColor=yellow">
<a href="https://pypi.org/project/bing-rewards/"> <img alt="PyPi" src="https://img.shields.io/pypi/v/bing-rewards?label=PyPI&style=flat-square&logo=pypi&logoColor=yellow"></a>
<a href="https://pypi.org/project/bing-rewards/"> <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/bing-rewards?style=flat-square&label=Downloads&color=orange"></a>
<br>
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/bing-rewards?style=flat-square&label=License&color=blueviolet">
<a href="https://github.com/psf/black"> <img alt="Formatting" src="https://img.shields.io/badge/Code%20Style-Black-000000?style=flat-square"> </a>

</div>

### A CLI app to perform Bing searches
Please submit an issue or pull-request if you have an idea for a feature

- [Install](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Config](#configuration)

## **Features**

* Script types search queries into the address bar, so must be run in a GUI environment.
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* All files are local, makes no http(s) requests
* Only one external dependance (pynput)
* Fine tune delay and set browser executable with [config](#configuration) at `$XDG_CONFIG_HOME` or `%APPDATA%` on Windows
* Best Value: gift cards: **1,050 points / $1** (current rate)
***

## **Installation**
```bash
pip install bing-rewards
```
Will make the executable `bing-rewards` available on your PATH.
Look below or try the `--help` flag to see detailed usage.

**Recommended**: Use a virtual environment or [`pipx`](https://pypa.github.io/pipx/) to avoid poluting your global package path with executable apps. See: [pipx](https://pypa.github.io/pipx/)
```bash
pipx install bing-rewards
```

**NEW IN 2.0:** Now using the `pynput` backend with significantly less dependencies than the old `PyAutoGUI`. Delete any old virtual enviroment and reinstall to clean up old depdendencies.

## **Requirements**

- At least Python 3.8

- [pynput](https://github.com/moses-palmer/pynput) package is used to control keypresses and type Bing search URLS.
WARNING: This script *will* take control away from the keyboard while running. **Pynput** performs key presses. i.e., it does not operate headless or in the background.

- `chrome` must be discoverable on the system PATH. [Download Google Chrome](https://www.google.com/intl/en/chrome/).
If your chromium based browser has a different name use the `--exe` flag with an absolute path to the browser executable to use (e.g. `--exe=$(which brave-browser)`). Also see the `"browser-path"` key in the [config](#configuration) file.

- To earn points from searching, you *must* also have logged into [bing.com](https://www.bing.com) with your Microsoft account at least once, to save cookies.

## **Usage**

#### `bing-rewards [-h] [--no-window] [-n] [--exe EXE] [-c COUNT] [-d | -m] [--profile "Profile X"]`

Ex:
Complete mobile and desktop daily points

`$ bing-rewards`

Run 10 searches with mobile user-agent in a new window

`$ bing-rewards -m -c10`

`$ bing-rewards --mobile --count=10`

Complete mobile and desktop daily points using specified chrome profile "Profile 1"

`$ bing-rewards --profile "Profile 1"`

Launches Chrome as a subprocess with special flags. Tested on Windows 10 and Linux (Ubuntu + Arch), however it should work on Mac OS as well.

⚠️Known Issue: No other instance of chrome.exe can be open when the script runs. Chrome prevents different user agents in each window. The script will run, but Chrome will not appear as Edge


## **Configuration**

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
| `--open-rewards`        | Open the rewards page at the end of the run                                           |
| `-X`, `--no-exit`       | Do not close the browser after completing a search                                    |
| `--load-delay`          | Override the time given to Chrome to load in seconds                                  |
| `--search-delay`        | Override the time between searches in seconds                                         |
| `--exe EXE`             | The full path of the Chrome compatible browser executable (Brave and Chrome tested)   |
| `--nowindow`            | Don't open a new Chrome window, just type the keys                                    |
| `--profile "Profile N"` | Launches chrome using the specified profile. Otherwise use default.                   |
| `--ime`                 | Triggers Windows IME to switch to English input by pressing "shift"                   |

A config file is also generated in $XDG_CONFIG_HOME or %APPDATA% on Windows
where precise delay modifications can be made.

Example config `~/.config/bing-rewards/config.json`
```json
{
    "desktop-count": 30,
    "mobile-count": 20,
    "load-delay": 1.5,
    "search-delay": 2,
    "search-url": "https://www.bing.com/search?q=",
    "desktop-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    "mobile-agent": "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041",
    "browser-path": "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
}
```
Delay timings are in seconds

## User agents

If interested, the following user agents are passed to Chrome using the `--user-agent` argument.
These are clearly defined at the top of `bing-rewards.py`.

Edge Browser on Windows 10 desktop:
> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37

Mobile Edge Browser on Windows 10 phone:
> Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041
***

## Words:
The [keywords](https://www.myhelpfulguides.com/keywords.txt) included in this repo where taken from this site
https://www.myhelpfulguides.com/2018/07/19/bing-rewards-auto-searcher-with-python-3/.

This script provided the original inspiration but has since been complelty rewritten and expanded.
The original author was contacted for the original source of keywords, but declined to respond
