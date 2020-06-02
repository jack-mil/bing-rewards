# bing_search

### A script to automate daily Bing rewards points

## **Features**
***
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* All files are local, makes no http(s) requests

## **Usage**
***
> Ex: `py bing_search -n`   

*Run 30 searches in desktop mode in a new Chrome window*
> Ex: `py bing_search -n -m -c10
> `py bing_search --new --mobile --count=10`  

*Run 10 searches with mobile user-agent in a new window

## **Requirements:**
***
Uses the PyAutoGUI package to automatically type search queries into bing. 
WARNING: This script *will* take control away from the keyboard while running. PyAutoGUI performs key presses.

> `pip install pyautogui`  

`chrome.exe` must be discoverable on the system PATH  
Alternatively, open your preferred browser before running the script with the `-n, --new` argument

## **All options**
| Flag              | Option                                                        |
|-------------------|---------------------------------------------------------------|
| `-h`, `--help`    | Display help and exit                                         |
| `-n`, `--new`     | Open in a new window instead of whatever is currently focused |
| `-c`, `--count=N` | Perform N searches total (default 30)                         |
| `-m`, `--mobile`  | Use a mobile user agent, to appear on a phone                 |
| `--dry-run`       | Do everything but type the search query                       |