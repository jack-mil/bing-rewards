from os import path, remove
import sys, getopt
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

def Diff(li1, li2):
    """ Computes the difference of two lists """
    return list(set(li1) - set(li2))

count = 30
new = False

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hnc:', ['new', 'count='])

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
    url = 'https://www.bing.com/'

    word_site = "https://www.myhelpfulguides.com/keywords.txt"

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
        address = f"http://www.bing.com/search?q={quote_plus(query)}"

        with open('tempfile', 'a') as f:
            f.write(query + "\n")

        sleep_time = 2
        time.sleep(sleep_time)
        pyautogui.hotkey('alt', 'd')
        time.sleep(0.01)
        pyautogui.typewrite(address)
        pyautogui.typewrite('\n', interval=0.1)

        print(
            f"Search {i+1}: {query}")
finally:
    remove('tempfile')
