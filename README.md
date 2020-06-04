# bing_search
:exclamation: **Warning, this project is incomplete and a WIP; bugs likely.**  
Please submit an issue or pull-request if you have an idea for a feature 
### A script to automate daily Bing rewards points

## **Features**
***
* Script basically auto-types searches, so must be run in a GUI environment. Great for AFK grinding once a day for those points
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* All files are local, makes no http(s) requests
* Spoofs user agent to appear as Edge Browser on Mobile or Desktop in Chrome!
* Timings can be tweaked to speed up the automation  

## **Usage**
***
> Run 30 searches in desktop mode in a new Chrome window

*`> python bing_search -n`*   

> Run 10 searches with mobile user-agent in a new window

*`> python bing_search -n -m -c10`*  

*` > python bing_search --new --mobile --count=10`*

Executes a system command to launch Chrome with special flags. If it fails on your OS, manually modify the command used to launch Chrome in the script.

Note: Due to how Chrome processes work, you must close all chrome windows to reset the user agent. (e.g. when switching from desktop to mobile mode)
## **Requirements:**
***
At least Python 3.6. Be careful if you also have Python 2 installed on your system (most Linux distros can invoke `python3`)  

Uses the [PyAutoGUI](https://github.com/asweigart/pyautogui) package to automatically type Bing search URLS.   
WARNING: This script *will* take control away from the keyboard while running. PyAutoGUI performs key presses. i.e., it does not operate headless or in the background. This feature is being researched.

*`> pip install pyautogui`*

`chrome` must be discoverable on the system PATH  
Alternatively, open your preferred browser before running the script without the `-n, --new` argument. Custom user agent will not be set in this case.

You must also have logged into www.bing.com with your Microsoft account at least once. 
The tool will still search without doing this, but you won't earn rewards points

## **All options**
| Flag              | Option                                                        |
|-------------------|---------------------------------------------------------------|
| `-h`, `--help`    | Display help and exit                                         |
| `-n`, `--new`     | Open in a new window instead of whatever is currently focused (*this is the preferred method*) |
| `-c`, `--count=N` | Perform N searches total (default 30)                         |
| `-m`, `--mobile`  | Use a mobile user agent, to appear on a phone                 |
| `--dry-run`       | Do everything but type the search query                       |

## User agents
***
If interested, the following user agents are passed to chrome using the `--user-agent` argument. These are clearly defined at the top of `bing_search.py`.  

Edge Browser on Windows 10 desktop:  
> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37

Mobile Edge Browser on Windows 10 phone:  
> Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041 