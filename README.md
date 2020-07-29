# bing-search
### A script to automate daily Bing rewards points
Please submit an issue or pull-request if you have an idea for a feature 

## **Features:**

* Spoofs user agent to appear as Mobile or Desktop Edge Browser using Chrome!
* Script auto-types searches, so must be run in a GUI environment. Great for AFK grinding once a day for those points
* Use a mobile user agent to get mobile points (`--mobile`)
* Configurable number of searches with `--count=`
* All files are local, makes no http(s) requests
* Only one external dependance (PyAutoGUI) 
***

## **Download:**

Download the [zip file](https://github.com/jack-mil/bing-search/archive/master.zip) and extract it somewhere, or using git:  
`$ git clone --depth=1 https://github.com/jack-mil/bing-search.git && cd bing-search`  


## **Requirements:**

- At least Python 3.6. Be careful if you also have Python 2 installed on your system (most Linux distros can invoke `python3`)  

- [PyAutoGUI](https://github.com/asweigart/pyautogui) package to automatically type Bing search URLS.   
WARNING: This script *will* take control away from the keyboard while running. PyAutoGUI performs key presses. i.e., it does not operate headless or in the background.  
Install PyAutoGUI with `pip`  
`$ python -m pip install -r requirements.txt`  OR  
`$ python -m pip install pyautogui`  

- `chrome` must be discoverable on the system PATH. [Download Google Chrome](https://www.google.com/intl/en/chrome/).  
If you use a different chromium based browser that supports setting user agents via the `--user-agent` option, you can change the command to run in [`bing_search.py` *`chrome_cmd()`*](https://github.com/jack-mil/bing-search/blob/6aa71887f22388ecb88dc54c634c12fa7ebff171/bing_search.py#L110)  
```py
return ['brave', '--new-window', f'--user-agent=\"{agent}\"']
```

- To earn points from searching, you must also have logged into [bing.com](https://www.bing.com) with your Microsoft account at least once, to save cookies. 

## **Usage:**

#### `python bing_search.py [-h] [--nowindow] [-c COUNT] [-n] [-d | -m]`

Ex:  
Complete mobile and desktop daily points

`$ python bing_search`

Run 10 searches with mobile user-agent in a new window

`$ python bing_search -m -c10`

`$ python bing_search --mobile --count=10`

Launches Chrome as a subprocess with special flags. Only tested on Windows 10, however it should work on other platforms

Will  now automatically create and close the Chrome processes as needed.


## **All options:**

Running with no options will complete mobile and desktop daily search quota. The following options are available to change the default behavior.
| Flag              | Option                           |
|-------------------|---------------------------------|
| `-h`, `--help`    | Display help and exit           |
| `-c`, `--count=N` | Override the number of searches to complete |
| `-d`, `--desktop`  | Only use desktop user agent                |
| `-m`, `--mobile`  | Only use a mobile user agent              |
| `-n`, `--dryrun`  | Do everything but type the search query       |
| `--nowindow`     | Don't open a new Chrome window, just type the keys|


## User agents:

If interested, the following user agents are passed to Chrome using the `--user-agent` argument. These are clearly defined at the top of `bing_search.py`.  

Edge Browser on Windows 10 desktop:  
> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37

Mobile Edge Browser on Windows 10 phone:  
> Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041 
***
