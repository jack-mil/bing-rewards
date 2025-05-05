# SPDX-FileCopyrightText: 2020 jack-mil
#
# SPDX-License-Identifier: MIT

"""Bing Rewards v{VERSION}.

Automatically perform Bing searches for Rewards Points!
Executing 'bing-rewards' with no arguments does {DESKTOP_COUNT} desktop searches
followed by {MOBILE_COUNT} mobile searches by default.

Examples
--------
    $ bing-search -dc30
    $ bing-search --count=50 --mobile --dryrun

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


def word_generator() -> Generator[str, None, None]:
    """Infinitely generate terms from the word file.

    Starts reading from a random position in the file.
    If end of file is reached, close and restart.
    Handles file operations safely and ensures uniform random distribution.

    Yields:
        str: A random keyword from the file, stripped of whitespace.

    Raises:
        OSError: If there are issues accessing or reading the file.
    """
    word_data = resources.files('bing_rewards').joinpath('data', 'keywords.txt')

    try:
        while True:
            with (
                resources.as_file(word_data) as p,
                p.open(mode='r', encoding='utf-8') as fh,
            ):
                # Get the file size of the Keywords file
                fh.seek(0, SEEK_END)
                size = fh.tell()

                if size == 0:
                    raise ValueError('Keywords file is empty')

                # Start at a random position in the stream
                fh.seek(random.randint(0, size - 1), SEEK_SET)

                # Read and discard partial line to ensure we start at a clean line boundary
                fh.readline()

                # Read lines until EOF
                for raw_line in fh:
                    stripped_line = raw_line.strip()
                    if stripped_line:  # Skip empty lines
                        yield stripped_line

                # If we hit EOF, seek back to start and continue until we've yielded enough words
                fh.seek(0)
                for raw_line in fh:
                    stripped_line = raw_line.strip()
                    if stripped_line:
                        yield stripped_line
    except OSError as e:
        print(f'Error accessing keywords file: {e}')
        raise
    except Exception as e:
        print(f'Unexpected error in word generation: {e}')
        raise


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
    if os.environ.get('XDG_SESSION_TYPE', '').lower() == 'wayland':
        cmd.append('--ozone-platform=x11')
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

        # If user's default search engine is Bing, type the query to the address bar directly
        # Otherwise, form the bing.com search url
        search_url = query if options.bing else options.search_url + quote_plus(query)

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

        print(f'Search {i + 1}: {query}')

        # Delay to let page load
        match options.search_delay:
            case int(x) | float(x) | [float(x)]:
                delay = x
            case [float(min_s), float(max_s)]:
                delay = random.uniform(min_s, max_s)
            case other:
                # catastrophic failure
                raise ValueError(f'Invalid configuration format: "search_delay": {other!r}')

        time.sleep(delay)

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

    def desktop(profile=''):
        # Complete search with desktop settings
        count = options.count if 'count' in options else options.desktop_count
        print(f'Doing {count} desktop searches using "{profile}"')

        temp_options = options
        temp_options.profile = profile
        search(count, words_gen, options.desktop_agent, temp_options)
        print('Desktop Search complete!\n')

    def mobile(profile=''):
        # Complete search with mobile settings
        count = options.count if 'count' in options else options.mobile_count
        print(f'Doing {count} mobile searches using "{profile}"')

        temp_options = options
        temp_options.profile = profile
        search(count, words_gen, options.mobile_agent, temp_options)
        print('Mobile Search complete!\n')

    def both(profile=''):
        desktop(profile)
        mobile(profile)

    # Execute main method in a separate thread
    if options.desktop:
        target_func = desktop
    elif options.mobile:
        target_func = mobile
    else:
        # If neither mode is specified, complete both modes
        target_func = both

    # Run for each specified profile (defaults to ['Default'])
    for profile in options.profile:
        # Start the searching in separate thread
        search_thread = threading.Thread(target=target_func, args=(profile,), daemon=True)
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
                        return  # Exit the entire function if ESC is pressed

        except KeyboardInterrupt:
            print('CTRL-C pressed, terminating')
            return  # Exit the entire function if CTRL-C is pressed

        # Wait for the current profile's searches to complete
        search_thread.join()

    # Open rewards dashboard
    if options.open_rewards and not options.dryrun:
        webbrowser.open_new('https://account.microsoft.com/rewards')


# Execute only if run as a command line script
if __name__ == '__main__':
    main()
