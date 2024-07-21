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

from __future__ import annotations

import os
import random
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from importlib import resources
from io import SEEK_END, SEEK_SET
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import quote_plus

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Generator

if os.name == 'posix':
    import signal


from pynput import keyboard
from pynput.keyboard import Key

import bing_rewards.options as app_options


def word_generator() -> Generator[str]:
    """Infinitely generate terms from the word file.

    Starts reading from a random position in the file.
    If end of file is reached, close and restart.
    """
    word_data = resources.files('bing_rewards').joinpath('data', 'keywords.txt')
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


def browser_cmd(exe: Path, agent: str, profile: str = '') -> list[str]:
    """Validate command to open Google Chrome with user-agent `agent`."""
    exe = Path(exe)
    if exe.is_file() and exe.exists():
        cmd = [str(exe.resolve())]
    elif pth := shutil.which(exe):
        cmd = [str(pth)]
    else:
        print(
            f'Command "{exe}" could not be found.\n'
            'Make sure it is available on PATH, '
            'or use the --exe flag to give an absolute path.'
        )
        sys.exit(1)

    cmd.extend(['--new-window', f'--user-agent="{agent}"'])
    # Switch to non default profile if supplied with valid string
    # NO CHECKING IS DONE if the profile exists
    if profile:
        cmd.extend([f'--profile-directory={profile}'])
    return cmd


def open_browser(cmd: list[str]) -> subprocess.Popen:
    """Try to open a browser, and exit if the command cannot be found.

    Returns the subprocess.Popen object to handle the browser process.
    """
    try:
        # Open browser as a subprocess
        # Only if a new window should be opened
        if os.name == 'posix':
            chrome = subprocess.Popen(
                cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, start_new_session=True
            )
        else:
            chrome = subprocess.Popen(cmd)
    except OSError as e:
        print('Unexpected error:', e)
        print(f"Running command: '{' '.join(cmd)}'")
        sys.exit(1)

    print(f'Opening browser [{chrome.pid}]')
    return chrome


def close_browser(chrome: subprocess.Popen | None):
    """Close the browser process if it needs to be closed."""
    if chrome is None:
        return
    # Close the Chrome window
    print(f'Closing browser [{chrome.pid}]')
    if os.name == 'posix':
        os.killpg(chrome.pid, signal.SIGTERM)
    else:
        chrome.kill()


def search(count: int, words_gen: Generator, agent: str, options: Namespace):
    """Perform the actual searches in a browser.

    Open a chromium browser window with specified `agent` string, complete `count`
    searches from list `words`, finally terminate browser process on completion.
    """
    cmd = browser_cmd(options.browser_path, agent, options.profile)
    chrome = None
    if not options.no_window and not options.dryrun:
        chrome = open_browser(cmd)

    # Wait for Chrome to load
    time.sleep(options.load_delay)

    # keyboard controller from pynput
    key_controller = keyboard.Controller()

    # Ctrl + E to open address bar with the default search engine
    # Alt + D focuses address bar without using search engine
    key_mod, key = (Key.ctrl, 'e') if options.bing else (Key.alt, 'd')

    for i in range(count):
        # Get a random query from set of words
        query = next(words_gen)

        if options.bing:
            # If the --bing flag is set, type the query to the address bar directly
            search_url = query
        else:
            # Concatenate url with correct url escape characters
            search_url = options.search_url + quote_plus(query)

        # Use pynput to trigger keyboard events and type search queries
        if not options.dryrun:
            with key_controller.pressed(key_mod):
                key_controller.press(key)
                key_controller.release(key)

            if options.ime:
                # Incase users use a Windows IME, change the language to English
                # Issue #35
                key_controller.tap(Key.shift)
            time.sleep(0.08)

            # Type the url into the address bar
            # This is very fast and hopefully reliable
            key_controller.type(search_url + '\n')

        print(f'Search {i+1}: {query}')
        # Delay to let page load
        time.sleep(options.search_delay)

    # Skip killing the window if exit flag set
    if options.no_exit:
        return

    close_browser(chrome)


def main():
    """Program entrypoint.

    Loads keywords from a file, interprets command line arguments
    and executes search function in separate thread.
    Setup listener callback for ESC key.
    """
    options = app_options.get_options()

    words_gen = word_generator()

    def desktop():
        # Complete search with desktop settings
        count = options.count if 'count' in options else options.desktop_count
        print(f'Doing {count} desktop searches')

        search(count, words_gen, options.desktop_agent, options)
        print('Desktop Search complete!\n')

    def mobile():
        # Complete search with mobile settings
        count = options.count if 'count' in options else options.mobile_count
        print(f'Doing {count} mobile searches')

        search(count, words_gen, options.mobile_agent, options)
        print('Mobile Search complete!\n')

    def both():
        desktop()
        mobile()

    # Execute main method in a separate thread
    if options.desktop:
        target = desktop
    elif options.mobile:
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
    if options.open_rewards and not options.dryrun:
        webbrowser.open_new('https://account.microsoft.com/rewards')


# Execute only if run as a command line script
if __name__ == '__main__':
    main()
