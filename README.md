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
`python bing_search.py [-h] [--nowindow] [-c COUNT] [-n] [-d | -m | -a]`
##
Ex:  
Complete mobile and desktop daily points

*`$ python bing_search`*   

Run 10 searches with mobile user-agent in a new window

*`$ python bing_search -m -c10`*  

*`$ python bing_search --mobile --count=10`*

Executes a system command to launch Chrome with special flags. If it fails on your OS, manually modify the command used to launch Chrome in the script.

Will  now automatically create and close the Chrome processes as needed.
## **Requirements:**
***
At least Python 3.6. Be careful if you also have Python 2 installed on your system (most Linux distros can invoke `python3`)  

Uses the [PyAutoGUI](https://github.com/asweigart/pyautogui) package to automatically type Bing search URLS.   
WARNING: This script *will* take control away from the keyboard while running. PyAutoGUI performs key presses. i.e., it does not operate headless or in the background. This feature is being researched.

*`$ pip install pyautogui`*

`chrome` must be discoverable on the system PATH  
Alternatively, open your preferred browser and run with `--nowindow` argument. Custom user agent will not be set in this case.

You must also have logged into www.bing.com with your Microsoft account at least once. 
The tool will still search without doing this, but you won't earn rewards points

## **All options**
| Flag              | Option                                                        |
|-------------------|---------------------------------------------------------------|
| `-h`, `--help`    | Display help and exit                                         |
| `-c`, `--count=N` | Perform N searches total (default per search type)                         |
| `-a`, `--all`  |(default) Do both types of searches, to complete daily (34 Desktop; 40 Mobile)               |
| `-d`, `--desktop`  | Use a desktop user agent                |
| `-m`, `--mobile`  | Use a mobile user agent, to appear on a phone                 |
| `-n`, `--dryrun`       | Do everything but type the search query                       |
| `--nowindow`     | Don't open a new Chrome window, just type the keys|

## User agents
***
If interested, the following user agents are passed to chrome using the `--user-agent` argument. These are clearly defined at the top of `bing_search.py`.  

Edge Browser on Windows 10 desktop:  
> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37

Mobile Edge Browser on Windows 10 phone:  
> Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041 