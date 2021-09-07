"""
Bing Search

Automatically perform Bing searches for Rewards Points!
Executing 'bing-rewards' with no arguments does {DESKTOP_COUNT} desktop searches
followed by {MOBILE_COUNT} mobile searches by default

Usage:

    $ bing-search -nmc30
    $ bing-search --new --count=50 --mobile --dryrun

Try:
    bing-search --help
for more info

A config file is generated in $XDG_CONFIG_HOME or %APPDATA% on Windows
where precise delay modifications can be made
Delay timings are in seconds

* By: jack-mil

* Repository and issues: https://github.com/jack-mil/bing-search
"""

import argparse as argp
import json
import os
import random
import subprocess
import sys
import time
import webbrowser
from io import SEEK_END, SEEK_SET
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict, Generator, List
from urllib.parse import quote_plus

import pyautogui

# Edge Browser user agents
# Makes Google Chrome look like MS Edge to Bing
MOBILE_AGENT = (
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/70.0.3538.102 Mobile Safari/537.36 Edge/18.19041"
)

DESKTOP_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"
)


# Number of searches to make
DESKTOP_COUNT = 34
MOBILE_COUNT = 40

# Time to allow Chrome to load in seconds
LOAD_DELAY = 1.5
# Time between searches in seconds
SEARCH_DELAY = 2

# Bing Search base url
URL = "https://www.bing.com/search?q="

# Reference Keywords from package files
KEYWORDS = Path(Path(__file__).parent, "data", "keywords.txt")

SETTINGS = {
    "desktop-count": DESKTOP_COUNT,
    "mobile-count": MOBILE_COUNT,
    "load-delay": LOAD_DELAY,
    "search-delay": SEARCH_DELAY,
    "search-url": URL,
    "desktop-agent": DESKTOP_AGENT,
    "mobile-agent": MOBILE_AGENT,
    "browser-path": "",
}


def check_path(path: str) -> Path:
    exe = Path(path)
    if exe.is_file and exe.exists:
        return exe
    raise FileNotFoundError(path)


def parse_args():
    """
    Parse all command line arguments and return Namespace
    """
    p = argp.ArgumentParser(
        description=__doc__.format(
            DESKTOP_COUNT=DESKTOP_COUNT, MOBILE_COUNT=MOBILE_COUNT
        ),
        formatter_class=argp.RawDescriptionHelpFormatter,
    )

    p.add_argument(
        "--no-window",
        help="Don't open a new Chrome window (just press keys)",
        action="store_true",
    )
    p.add_argument(
        "-n",
        "--dryrun",
        help="Do everything but search",
        action="store_true",
    )
    p.add_argument(
        "--exe",
        help="The full path of the Chrome compatible browser executable (Brave or Chrome tested)",
        type=check_path,
    )
    p.add_argument(
        "-c",
        "--count",
        help="Override the number of searches to perform",
        type=int,
    )

    # Mutually exclusive options. Only one can be present
    group = p.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--desktop",
        help="Do only desktop searches",
        action="store_true",
    )
    group.add_argument(
        "-m",
        "--mobile",
        help="Do only mobile searches (appear as phone browser)",
        action="store_true",
    )

    return p.parse_args()


def parse_config(default_config: Dict) -> Dict:
    config_home = Path(
        os.environ.get("APPDATA")
        or os.environ.get("XDG_CONFIG_HOME")
        or Path(os.environ["HOME"], ".config"),
        "bing-rewards",
    )

    config_file = config_home / "config.json"

    try:
        # Read config from json dictionary
        with config_file.open() as f:
            return json.load(f)

    except FileNotFoundError:
        # Make directories and default config if it doesn't exist
        print(f"Autogenerating config at {str(config_file)}")
        os.makedirs(config_home, exist_ok=True)

        with config_file.open("x") as f:
            json.dump(default_config, f, indent=4)
            return default_config
    except JSONDecodeError as e:
        print(e)
        print("Error parsing JSON config. Please check your modifications.")
        sys.exit(1)


def check_python_version():
    """
    Ensure the correct version of Python is being used.
    """
    minimum_version = (3, 6)
    assert (
        sys.version_info >= minimum_version
    ), "Only Python {}.{} and above is supported.".format(*minimum_version)


def browser_cmd(exe: Path, agent: str) -> List[str]:
    """
    Generate command to open Google Chrome with user-agent `agent`
    """
    if exe is not None:
        browser = str(exe)
    else:
        browser = "chrome"
    return [browser, "--new-window", f'--user-agent="{agent}"']


def get_words_gen() -> str:
    while True:
        # Wrapped in an infinite loop to support circular reading of the file
        with KEYWORDS.open(mode="r", encoding="utf8") as fh:
            fh.seek(0, SEEK_END)
            size = fh.tell()  # Get the filesize of the Keywords file
            fh.seek(
                random.randint(0, (size * 3 // 4)), SEEK_SET
            )  # Start at a random position in the stream
            for line in fh:
                # Use the built in file handler generator
                yield line.strip()


def search(count, words_gen: Generator, agent, args, config):
    """
    Opens a Chrome window with specified `agent` string, completes `count`
    searches from list `words`,
    finally terminating Chrome process on completion
    """
    try:
        # Open Chrome as a subprocess
        # Only if a new window should be opened
        if not args.no_window and not args.dryrun:
            chrome = subprocess.Popen(
                browser_cmd(args.exe or config.get("browser-path") or None, agent)
            )
    except FileNotFoundError as e:
        print("Unexpected error:", e)
        print(
            "ERROR: Chrome could not be found on system PATH\n"
            "Make sure it is installed and added to PATH,"
            "or use the --exe flag to give an absolute path"
        )
        sys.exit(1)

    # Wait for Chrome to load
    time.sleep(config.get("load-delay", LOAD_DELAY))

    for i in range(count):
        # Get a random query from set of words
        query = next(words_gen)

        # Concatenate url with correct url escape characters
        search_url = URL + quote_plus(query)

        # Use PyAutoHotkey to trigger keyboard events and auto search
        if not args.dryrun:
            # Alt + D to focus the address bar in Chrome
            pyautogui.hotkey("alt", "d")
            time.sleep(0.01)

            # Type the url into the address bar
            pyautogui.typewrite(search_url)
            pyautogui.typewrite("\n", interval=0.1)

        print(f"Search {i+1}: {query}")
        time.sleep(config.get("search-delay", SEARCH_DELAY))

    if not args.no_window and not args.dryrun:
        # Close the Chrome window
        chrome.terminate()


def main():
    """
    Main program execution. Loads keywords from a file,
    interprets command line arguments,
    and executes search function
    """

    check_python_version()
    config = parse_config(SETTINGS)
    args = parse_args()

    if args.dryrun:
        config["search-delay"] = 0
        config["load-delay"] = 0

    words_gen = get_words_gen()

    def desktop():
        # Complete search with desktop settings
        count = args.count or config.get("desktop-count") or DESKTOP_COUNT
        print(f"Doing {count} desktop searches")

        search(
            count, words_gen, config.get("desktop-agent") or DESKTOP_AGENT, args, config
        )
        print(f"Desktop Search complete! {5*count} MS rewards points\n")

    def mobile():
        # Complete search with mobile settings
        count = args.count or config.get("mobile-count") or MOBILE_COUNT
        print(f"Doing {count} mobile searches")

        search(
            count, words_gen, config.get("mobile-agent") or MOBILE_AGENT, args, config
        )
        print(f"Mobile Search complete! {5*count} MS rewards points\n")

    # If neither mode is specified, complete both modes
    if args.desktop:
        desktop()
    elif args.mobile:
        mobile()
    else:
        desktop()
        mobile()
        # Open rewards dashboard
        if not args.dryrun:
            webbrowser.open_new("https://account.microsoft.com/rewards")


# Execute only if run as a command line script
if __name__ == "__main__":
    main()
