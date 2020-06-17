#!/usr/bin/env python3
"""Bing Search

Automatically perform MS Bing searches to earn rewards points

Usage:

    $ bing_search.py
    $ bing_search.py -nmc30
    $ bing_search.py --new --count=50 --mobile --dryrun

try
    $ python bing_search.py --help

for more info


* By: Jackson Miller

* Repository and issues: https://github.com/jack-mil/bing-search
"""
import argparse as argp
import platform
import random
import subprocess
import sys
import time
from os import path, remove, system
from urllib.parse import quote_plus

import pyautogui

# Edge Browser user agents
# Makes Google Chrome look like MS Edge to Bing
mobile_agent = ('Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041')

desktop_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37')

# Number of searches to make
DESKTOP_COUNT = 34
MOBILE_COUNT = 40

# Time to allow Chrome to load in seconds
LOAD_DELAY = 1.5
# Time between searches in seconds
SEARCH_DELAY = 2

# Bing Search base url
URL = 'https://www.bing.com/search?q='

# Internal files
word_file = 'keywords.txt'
temp_file = 'tempfile'

# Set of used keywords
used = set()


def parse_args():
    """
    Parse all command line arguments and return Namespace
    """
    desc = ('Automatically perform Bing searches for Rewards Points!\n'
            f'Does {DESKTOP_COUNT} desktop searches \n'
            f'followed by {MOBILE_COUNT} mobile searches by default')
    p = argp.ArgumentParser(description=desc)

    p.add_argument(
        '--nowindow',
        help='don\'t open a new Chrome window (just press keys)',
        action='store_true',
        default=False)
    p.add_argument(
        '-n', '--dryrun',
        help='do everything but search',
        action='store_true',
        default=False)
    p.add_argument(
        '-c', '--count',
        help=f'override the number of searches to perform',
        type=int)

    # Mutually exclusive options. Only one can be present
    group = p.add_mutually_exclusive_group()
    group.add_argument(
        '-d', '--desktop',
        help='do only desktop searches',
        action='store_true')
    group.add_argument(
        '-m', '--mobile',
        help='do only mobile searches (appear as phone browser)',
        action='store_true')

    return p.parse_args()


def check_python_version():
    """
    Ensure the correct version of Python is being used.
    """
    minimum_version = ('3', '6')
    if platform.python_version_tuple() < minimum_version:
        message = 'Only Python %s.%s and above is supported.' % minimum_version
        raise Exception(message)


def chrome_cmd(agent):
    """
    Generate command to open Google Chrome with user-agent `agent`
    """
    return ['chrome', '--new-window', f'--user-agent=\"{agent}\"']


def diff(li1, li2):
    """
    Computes the difference of two lists
    """
    return list(set(li1) - set(li2))


def search(count, words, agent, args):
    """
    Opens a Chrome window with specified `agent` string, completes `count`
    searches from list `words`,
    finally terminating Chrome process on completion
    """
    try:
        # Open Chrome as a subprocess
        # Only if a new window should be opened
        if not args.nowindow:
            chrome = subprocess.Popen(chrome_cmd(agent))
    except FileNotFoundError as e:
        print(e)
        print("Unexpected error:", sys.exc_info()[0])
        print('ERROR: Chrome could not be found on system PATH\n'
              'Make sure it is installed and added to PATH')
        sys.exit(1)

    # Wait for Chrome to load
    time.sleep(LOAD_DELAY)

    for i in range(count):
        # Get new random search query
        new = diff(words, used)
        query = random.choice(new)

        # Concatenate url with correct characters
        search_url = URL + quote_plus(query)

        # Use PyAutoHotkey to trigger keyboard events and auto search
        if not args.dryrun:
            # Alt + D to focus the address bar in Chrome
            pyautogui.hotkey('alt', 'd')
            time.sleep(0.01)

            # Type the url into the address bar
            pyautogui.typewrite(search_url)
            pyautogui.typewrite('\n', interval=0.1)

        used.add(query)
        time.sleep(SEARCH_DELAY)
        print(f"Search {i+1}: {query}")

    if not args.nowindow:
        # Close the Chrome window
        chrome.terminate()


def main(args):
    """
    Main program execution. Reads keywords from a file,
    interprets command line arguments,
    and executes search function
    """
    try:
        # Read search keywords from file
        f = open(word_file, 'r')
    except FileNotFoundError:
        print(f'File {path.realpath(word_file)} not found')
        sys.exit(1)
    else:
        # Store all words in a list if successful
        words = f.read().splitlines()
        print(f'Using database of {len(words)} potential searches')
        f.close()

    def desktop():
        # Complete search with desktop settings
        count = args.count if args.count else DESKTOP_COUNT
        print(f'Doing {count} desktop searches')

        search(count, words, desktop_agent, args)
        print(f'Desktop Search complete! {5*count} MS rewards points\n')

    def mobile():
        # Complete search with mobile settings
        count = args.count if args.count else MOBILE_COUNT
        print(f'Doing {count} mobile searches')

        search(count, words, mobile_agent, args)
        print(f'Mobile Search complete! {5*count} MS rewards points\n')

    # If neither mode is specified, complete both modes
    if args.desktop:
        desktop()
    elif args.mobile:
        mobile()
    else:
        desktop()
        mobile()


# Execute only if run as a command line script
if __name__ == "__main__":
    check_python_version()
    args = parse_args()
    main(args)
else:
    print('bing_search is intended to be run as a command line application.\n'
          'try "python3 bing_search.py --help" for more info.')
    sys.exit()
