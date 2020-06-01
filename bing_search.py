from os import path, remove
import sys
import getopt
import platform
import random
import time
import webbrowser
from urllib.parse import quote_plus
import pyautogui
import requests

# header = {
#   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"
# }
# header_mobile = {
#   "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
# }

count = 30
sleep_time = 2

url = 'https://www.bing.com/search?q='

# word_site = "https://raw.githubusercontent.com/jack-mil/bing_search/master/keywords.txt?token=AOZQVABAHBKOKE4X5LVPEY262TU7O"
word_site = "keywords.txt"

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

    try:
        opts, args = getopt.getopt(argv, 'hnc:', ['new', 'count='])

        for opt, arg in opts:
            if opt == '-h':
                print('<HELP TEXT>')
                sys.exit()
            elif opt in ('-n', '--new'):
                new = True
            elif opt in ('-c', '--count'):
                count = int(arg)
    except (ValueError, getopt.GetoptError):
        print('Ex: python3 bing_search.py --new --count 10')
        sys.exit(2)

    try:

        response = requests.get(word_site)
        words = response.text.splitlines()

        if not path.exists('tempfile'):
            with open('tempfile', 'x'):
                pass

        if new:
            webbrowser.open_new('www.bing.com')

        for i in range(count):
            with open('tempfile', 'r') as f:
                used = f.read().splitlines()

            new = Diff(words, used)
            query = random.choice(new)
            address = url + quote_plus(query)

            with open('tempfile', 'a') as f:
                f.write(query + "\n")

            time.sleep(sleep_time)
            pyautogui.hotkey('alt', 'd')
            time.sleep(0.01)
            pyautogui.typewrite(address)
            pyautogui.typewrite('\n', interval=0.1)

            print(
                f"Search {i+1}: {query}")
    finally:
        remove('tempfile')


if __name__ == "__main__":
    check_python_version()
    main(sys.argv[1:])
