"""Bing Search

Automatically perform MS Bing searches to earn rewards points

Usage:

    `bing_search.py`  
    `bing_search.py -nmc30`  
    `bing_search.py --new --count=50 --mobile --dryrun`  

try 
> `python bing_search.py --help`  
for more info

* By: Jackson Miller 
 
* Repository and issues: https://github.com/jack-mil/bing-search  
"""
from os import path, remove, system
import platform
import sys
import random
import time
import webbrowser
from urllib.parse import quote_plus
import pyautogui

# Edge Browser user agents
# Makes Google Chrome look like MS Edge to Bing
mobile_agent = 'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041'
desktop_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'

# Number of searches to make
DEFAULT_COUNT = 30

# Time to allow Chrome to load in seconds
LOAD_DELAY = 3
# Time between searches in seconds
SEARCH_DELAY = 2

URL = 'https://www.bing.com/search?q='

# Internal files
word_file = 'keywords.txt'
temp_file = 'tempfile'


def chrome_command(url, agent):
    """
    Generate OS specific command to open Google Chrome with user-agent `agent` at `url`
    """
    sys_type = platform.system()
    if sys_type == 'Windows':
        prefix = 'start '
    elif sys_type in ('Darwin', 'Linux'):
        prefix = ''
    else:
        message = 'ERROR: OS undetected. Please manually add the correct command to run chrome for your platform\n\
            On line 35 in function \"chrome_command\"'
        raise OSError(message)

    return f"{prefix}chrome {url} --new-window --user-agent=\"{agent}\""


def Diff(li1, li2):
    """
    Computes the difference of two lists
    """
    return list(set(li1) - set(li2))


def check_python_version():
    """
    Ensure the correct version of Python is being used.
    """
    minimum_version = ('3', '6')
    if platform.python_version_tuple() < minimum_version:
        message = 'Only Python %s.%s and above is supported.' % minimum_version
        raise Exception(message)


def parse_args():
    """
    Parse all command line arguments and return Namespace
    """
    import argparse as argp

    desc = 'Automatically perform Bing searches for Rewards Points!'
    p = argp.ArgumentParser(
        description=desc, formatter_class=argp.ArgumentDefaultsHelpFormatter)
    p.add_argument(
        '-n', '--new',
        help='Open in a new Chrome window (grabs focus). Uses Edge Browser\'s user agent',
        action='store_true',
        default=False)
    p.add_argument(
        '-c', '--count',
        help='The number of searches to perform',
        default=DEFAULT_COUNT,
        type=int)
    p.add_argument(
        '-m', '--mobile',
        help='Use a mobile user agent (appear as phone browser)',
        action='store_true',
        default='False')
    p.add_argument(
        '--dryrun',
        help='Do everything but search',
        action='store_true',
        default=False)

    return p.parse_args()


def main(args):
    try:
        with open(word_file, 'r') as f:
            words = f.read().splitlines()
            print(f'Using database of {len(words)} potential searches')

        if not path.exists(temp_file):
            with open(temp_file, 'x'):
                pass

        if args.new:
            agent = mobile_agent if args.mobile else desktop_agent
            # Execute system command. E.g. 'start chrome URL --user-agent AGENT 
            system(chrome_command('www.bing.com', agent))
            # Delay a bit to allow Chrome to load
            time.sleep(LOAD_DELAY)

        for i in range(args.count):
            with open(temp_file, 'r') as f:
                used = f.read().splitlines()

            new = Diff(words, used)
            query = random.choice(new)
            address = URL + quote_plus(query)

            with open(temp_file, 'a') as f:
                f.write(query + "\n")

            # Use PyAutoHotkey to trigger keyboard events and auto search
            if not args.dryrun:
                time.sleep(SEARCH_DELAY)
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.01)
                pyautogui.typewrite(address)
                pyautogui.typewrite('\n', interval=0.1)

            print(f"Search {i+1}: {query}")
        print(f'Done! Earned potentially {5*args.count} MS rewards points\n')

    except FileNotFoundError:
        print(f'File {path.realpath("word_file")} not found')

    finally:
        # Clean up
        if path.exists(temp_file):
            remove(temp_file)


# Main execution
if __name__ == "__main__":
    check_python_version()
    args = parse_args()
    main(args)
