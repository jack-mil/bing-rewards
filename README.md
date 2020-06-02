# bing_search
- [ ] **Warning, this project is incomplete and a WIP; bugs likely**
### A script to automate daily Bing rewards points

## **Features**
***
* Script basically auto-types searches, so must be run in a GUI environment. Great for AFK grinding once a day for those points
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* All files are local, makes no http(s) requests
* Timings could be tweaked to speed up the automation  

## **Usage**
***
> Run 30 searches in desktop mode in a new Chrome window

*`> python bing_search -n`*   

> Run 10 searches with mobile user-agent in a new window

*`> python bing_search -n -m -c10`*  

*` > python bing_search --new --mobile --count=10`*


## **Requirements:**
***
At least Python 3.6. Be careful if you also have Python 2 installed on your system (most Linux distros can invoke `python3`)  

Uses the PyAutoGUI package to automatically type search queries into bing.   
WARNING: This script *will* take control away from the keyboard while running. PyAutoGUI performs key presses.

> `> pip install pyautogui`  

`chrome.exe` must be discoverable on the system PATH  
Alternatively, open your preferred browser before running the script with the `-n, --new` argument

You must also make sure to have chrome set to log into your Microsoft account automatically. 
The tool will still work without this, but you won't earn rewards points

## **All options**
| Flag              | Option                                                        |
|-------------------|---------------------------------------------------------------|
| `-h`, `--help`    | Display help and exit                                         |
| `-n`, `--new`     | Open in a new window instead of whatever is currently focused (useful to guarantee focus for PyAutoGUI) |
| `-c`, `--count=N` | Perform N searches total (default 30)                         |
| `-m`, `--mobile`  | Use a mobile user agent, to appear on a phone                 |
| `--dry-run`       | Do everything but type the search query                       |
