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
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Options](#options)
- [Config](#config)
- [Development](#development)


## Features

* Enter random search queries into your browser *a-la* Auto Hotkey.
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* Install as self-contained python application with minimal dependencies (`pynput`)
* Fine tune delay and set browser executable with [config](#configuration) at `$XDG_CONFIG_HOME` or `%APPDATA%` on Windows
* Not intended as an automated or headless service. Simply assists with what would regularly be a manual task.


> [!Important]
> This was originally created in a different age, when Bing & MS was much simpler and less bloated with AI ~~slop~~ tools. Users have reported a wide variety of success on whether this method works at all with the new systems. See some of the pinned or closed issues for reports from others that may improve success. I maintain the *code* in a working state as an excersie in Python packaging, but do *not* personally use the utility, and **cannot guarantee this method will even generate points anymore**!

## Installation
Bing-rewards is a CLI application distributed on PyPI. You can install it however you prefer to manage Python applications on your system. I recommend `pipx` or `uv`.

### With [`pipx`](https://pipx.pypa.io/stable/) or `pip`
```bash
pipx install bing-rewards
```

### With [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
```sh
uv tool install bing-rewards
```

These commands will make the executable `bing-rewards` available on your PATH.
Look below or try the `--help` flag to see detailed usage.

> [!Tip]
> Use a virtual environment or [`pipx`](https://pypa.github.io/pipx/) to avoid polluting your global package space with executable apps. See: [pipx](https://pypa.github.io/pipx/)

### Locally
Clone the repo and install locally. See: [Developing](#development--contribution)

## Dependencies

- At least Python 3.10

- [pynput](https://github.com/moses-palmer/pynput) (installed with package). Used to control keypresses and type Bing search URLS.
  > [!Warning]
  >  Bing-Rewards *will* take control away from the keyboard while running. **Pynput** performs key presses. i.e., it does not operate headless or in the background.

- `chrome` must be discoverable on the system PATH. [Download Google Chrome](https://www.google.com/intl/en/chrome/).
  If your Chromium based browser has a different name use the `--exe` flag with an absolute path to the browser executable to use (e.g. `--exe=$(which brave-browser)`).
  See also: `"browser-path"` option in the [config](#configuration) file.

- To earn points from searching, you *must* also have logged into [bing.com](https://www.bing.com) with your Microsoft account at least once, to save cookies.

## Usage

> [!Tip]
> Press <kbd>ESC</kbd> to exit early and regain control

Complete mobile and desktop daily points

`$ bing-rewards`

Run 10 searches with mobile user-agent in a new window

`$ bing-rewards -m -c10`

`$ bing-rewards --mobile --count=10`

Complete mobile and desktop daily points using specified Chrome profile "Profile 1"

`$ bing-rewards --profile "Profile 1"`

Run searches sequentially across multiple Chrome profiles

`$ bing-rewards --profile "Default" "Profile 1" "Profile 2"`

Launches Chrome as a subprocess with special flags. Tested on Windows 10 and Linux (Ubuntu + Arch), however it should work on Mac OS as well.

> [!Warning]
> No other instance of chrome.exe can be open when the script runs. Chrome prevents different user agents in each window. The script will run, but Chrome will not appear as Edge


## Options

Running with no options will complete mobile and desktop daily search quota.
The following options are available to change the default behavior.
Options supplied at execution time override any config.
| Flag                       | Option                                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| `-h`, `--help`             | Display help and exit                                                                                  |
| `-c`, `--count=N`          | Override the number of searches to complete                                                            |
| `-b`, `--bing`             | Use this flag if Bing is already your default search engine. Bypasses constructing a bing.com URL      |
| `-d`, `--desktop`          | Only use desktop user agent                                                                            |
| `-m`, `--mobile`           | Only use a mobile user agent                                                                           |
| `-n`, `--dryrun`           | Do everything but type the search query                                                                |
| `--exe PATH`               | The full path of the Chrome compatible browser executable (Brave and Chrome tested)                    |
| `--load-delay SEC`         | Override the time given to Chrome to load in seconds                                                   |
| `--search-delay MIN[,MAX]` | Set the time between individual searches, in seconds. Can specify a range to get random delays         |
| `--open-rewards`           | Open the rewards page at the end of the run                                                            |
| `--nowindow`               | Don't open a new Chrome window, just type the keys                                                     |
| `-X`, `--no-exit`          | Do not close the browser after completing a search                                                     |
| `--profile`                | Run searches using specified Chrome profile(s). Multiple profiles can be specified to run sequentially |
| `--ime`                    | Triggers Windows IME to switch to English input by pressing "shift"                                    |

## Config
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
> [!Note]
> The format has slightly changed in version >= 3.0, so delete and regenerate accordingly.

### User agents

The default user agents that are passed to the Chrome process are below.
You may want to experiment with different user agents, or update versions accordingly.
Alternate user agents can be set in the config file.

Edge Browser on Windows 10 desktop:
> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edge/126.0.0.0

Mobile Edge Browser on Pixel 6 phone:
>  Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/AP2A.240605.024) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 Edge/121.0.2277.138


## Words
The [keywords](https://web.archive.org/web/20220523083250/https://www.myhelpfulguides.com/keywords.txt) included in this repo where taken from this site
[https://www.myhelpfulguides.com/2018/07/19/bing-rewards-auto-searcher-with-python-3/](https://web.archive.org/web/20220331033847/https://www.myhelpfulguides.com/2018/07/19/bing-rewards-auto-searcher-with-python-3/).

Their script provided the original inspiration but has since been completely rewritten and expanded.
The original author was contacted for the source of keywords, but declined to respond

## Development

This project is managed by the [`uv`](https://docs.astral.sh/uv) toolchain.
Ensure you have `uv` installed on your system. This is probably available in your package manager,
or can be installed with `pip` or `pipx`

Then, fork the repository on Github and clone to your machine. The first invocation of any `uv` command will install the `bing-rewards` package in editable mode, with the dev dependencies (`ruff` and `pre-commit`) automatically.

Install the defined pre-commit hooks: `uv run pre-commit install --install-hooks`

Launch bing-rewards in the editable dev environment: `uv run bing-rewards --help`

Feel free to open a PR against the `master` branch with additional features or fixes!
