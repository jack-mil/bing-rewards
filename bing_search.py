# Author: Jackson Miller
# https://github.com/jack-mil/bing-search

from os import path, remove, system
import sys
import getopt
import platform
import random
import time
import webbrowser
from urllib.parse import quote_plus
import pyautogui
# import requests

mobile_agent = 'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041'
desktop_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'

DEFAULT_COUNT = 30

sleep_time = 2

url = 'https://www.bing.com/search?q='

word_file = 'keywords.txt'
temp_file = 'tempfile'

def win_command(url, agent):
    return f"start chrome {url} --new-window --user-agent=\"{agent}\""

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


def main(argv):
    new = False
    dryrun = False
    mobile = False
    count = DEFAULT_COUNT

    # Arg Parse
    try:
        opts, _ = getopt.getopt(argv, 'hnmc:', ['new', 'count=', 'dry-run', 'mobile'])

        for opt, arg in opts:
            if opt == '-h':
                print('<HELP TEXT>')
                sys.exit()
            elif opt in ('-n', '--new'):
                new = True
            elif opt in ('-c', '--count'):
                count = int(arg)
            elif opt in ('-m','--mobile'):
                mobile = True
            elif opt == '--dry-run':
                dryrun = True
    except (ValueError, getopt.GetoptError):
        print('Arg parse ERROR\nEx: python3 bing_search.py --new --count 10')
        sys.exit(2)

    try:
        with open(word_file, 'r') as f:
            words = f.read().splitlines()
            print(f'Using database of {len(words)} potential searches')

        if not path.exists(temp_file):
            with open(temp_file, 'x'):
                pass

        if new:
            agent = mobile_agent if mobile else desktop_agent
            system(win_command('www.bing.com', agent))
            # webbrowser.open_new('www.bing.com')

        for i in range(count):
            with open(temp_file, 'r') as f:
                used = f.read().splitlines()

            new = Diff(words, used)
            query = random.choice(new)
            address = url + quote_plus(query)

            with open(temp_file, 'a') as f:
                f.write(query + "\n")

            if not dryrun:
                time.sleep(sleep_time)
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.01)
                pyautogui.typewrite(address)
                pyautogui.typewrite('\n', interval=0.1)

            print(f"Search {i+1}: {query}")

    except FileNotFoundError:
        print(f'File {path.realpath("word_file")} not found')

    finally:
        if path.exists(temp_file):
            remove(temp_file)


if __name__ == "__main__":
    check_python_version()
    main(sys.argv[1:])
