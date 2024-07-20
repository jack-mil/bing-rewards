"""Bing Rewards v{VERSION}.

Automatically perform Bing searches for Rewards Points!
Executing 'bing-rewards' with no arguments does {DESKTOP_COUNT} desktop searches
followed by {MOBILE_COUNT} mobile searches by default.

Examples
--------
    $ bing-search -nmc30
    $ bing-search --new --count=50 --mobile --dryrun

Config file: {CONFIG}
CLI arguments always override the config file.
Delay timings are in seconds.
"""

import os
import random
import subprocess
import sys
import threading
import time
import webbrowser
from collections.abc import Generator
from importlib import resources
from io import SEEK_END, SEEK_SET
from pathlib import Path
from urllib.parse import quote_plus

import bing_rewards.options as options

if os.name == 'posix':
    import signal

from pynput import keyboard
from pynput.keyboard import Key


def browser_cmd(exe: Path, agent: str, profile: str | None = None) -> list[str]:
    """Generate command to open Google Chrome with user-agent `agent`."""
    cmd = [str(exe), '--new-window', f'--user-agent="{agent}"']
    # Switch to non default profile if supplied with valid string
    # NO CHECKING IS DONE if the profile exists
    if profile is not None:
        cmd.extend([f'--profile-directory={profile}'])
    return cmd


def word_generator() -> Generator[str]:
    """Infinitely generate terms from the word file.

    Starts reading from a random position in the file.
    If end of file is reached, close and restart.
    """
    word_data = resources.files().joinpath('data', 'keywords.txt')
    while True:
        with (
            resources.as_file(word_data) as p,
            p.open(mode='r', encoding='utf-8') as fh,
        ):
            fh.seek(0, SEEK_END)
            size = fh.tell()  # Get the filesize of the Keywords file
            # Start at a random position in the stream
            fh.seek(random.randint(0, (size * 3 // 4)), SEEK_SET)
            for line in fh:
                # Use the built in file handler generator
                yield line.strip()


def open_browser(args, config, agent: str) -> subprocess.Popen:
    """Try to open a browser, and exit if the command cannot be found.

    Returns the subprocess.Popen object to handle the browser process.
    """

    cmd = browser_cmd(args.exe or config.get('browser-path'), agent, args.profile)
    try:
        # Open browser as a subprocess
        # Only if a new window should be opened
        if os.name == 'posix':
            chrome = subprocess.Popen(
                cmd,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                preexec_fn=os.setsid,
            )
        else:
            chrome = subprocess.Popen(cmd)
    except FileNotFoundError as e:
        print('Unexpected error:', e)
        print(
            f'Command "{cmd[0]}" could not be found.\n'
            'Make sure it is available on PATH, '
            'or use the --exe flag to give an absolute path.'
        )
        sys.exit(1)

    print(f'Opening browser with pid {chrome.pid}')
    return chrome


def close_browser(chrome):
    """Close the browser process if it needs to be closed."""
    if chrome is None:
        return
    # Close the Chrome window
    print(f'Closing browser [{chrome.pid}]')
    if os.name == 'posix':
        os.killpg(chrome.pid, signal.SIGTERM)
    else:
        chrome.kill()


def search(count, words_gen: Generator, agent: str, args, config):
    """Perform the actual searches in a browser.

    Open a chromium browser window with specified `agent` string, complete `count`
    searches from list `words`, finally terminate browser process on completion.
    """
    chrome = None
    if not args.no_window and not args.dryrun:
        chrome = open_browser(args, config, agent)

    # Wait for Chrome to load
    time.sleep(args.load_delay or config.get('load-delay'))

    # keyboard controller from pynput
    key_controller = keyboard.Controller()

    # Ctrl + E to open address bar with the default search engine
    # Alt + D focuses address bar without using search engine
    key_combo = (Key.ctrl, 'e') if args.bing else (Key.alt, 'd')

    for i in range(count):
        # Get a random query from set of words
        query = next(words_gen)

        if args.bing:
            # If the --bing flag is set, type the query to the address bar directly
            search_url = query
        else:
            # Concatenate url with correct url escape characters
            search_url = config.get('search-url') + quote_plus(query)

        # Use pynput to trigger keyboard events and type search queries
        if not args.dryrun:
            with key_controller.pressed(key_combo[0]):
                key_controller.press(key_combo[1])
                key_controller.release(key_combo[1])

            if args.ime:
                # Incase users use a Windows IME, change the language to English
                # Issue #35
                key_controller.tap(Key.shift)
            time.sleep(0.08)

            # Type the url into the address bar
            # This is very fast and hopefully reliable
            key_controller.type(search_url + '\n')

        print(f'Search {i+1}: {query}')
        # Delay to let page load
        time.sleep(args.search_delay or config.get('search-delay'))

    # Skip killing the window if exit flag set
    if args.no_exit:
        return

    close_browser(chrome)


def main():
    """Program entrypoint.

    Loads keywords from a file, interprets command line arguments
    and executes search function in separate thread.
    Setup listener callback for ESC key.
    """
    config = options.read_config()
    args = options.parse_args()

    words_gen = word_generator()

    def desktop():
        # Complete search with desktop settings
        count = config.get('desktop-count') if args.count is None else args.count
        print(f'Doing {count} desktop searches')

        search(count, words_gen, config.get('desktop-agent'), args, config)
        print('Desktop Search complete!\n')

    def mobile():
        # Complete search with mobile settings
        count = config.get('mobile-count') if args.count is None else args.count
        print(f'Doing {count} mobile searches')

        search(count, words_gen, config.get('mobile-agent'), args, config)
        print('Mobile Search complete!\n')

    def both():
        desktop()
        mobile()

    # Execute main method in a separate thread
    if args.desktop:
        target = desktop
    elif args.mobile:
        target = mobile
    else:
        # If neither mode is specified, complete both modes
        target = both

    # Start the searching in separate thread
    search_thread = threading.Thread(target=target, daemon=True)
    search_thread.start()

    print('Press ESC to quit searching')

    try:
        # Listen for keyboard events and exit if ESC pressed
        while search_thread.is_alive():
            with keyboard.Events() as events:
                event = events.get(timeout=0.5)  # block for 0.5 seconds
                # Exit if ESC key pressed
                if event and event.key == Key.esc:
                    print('ESC pressed, terminating')
                    break
    except KeyboardInterrupt:
        print('CTRL-C pressed, terminating')

    # Open rewards dashboard
    if args.open_rewards and not args.dryrun:
        webbrowser.open_new('https://account.microsoft.com/rewards')


# Execute only if run as a command line script
if __name__ == '__main__':
    main()
