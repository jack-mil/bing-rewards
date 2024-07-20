"""Defaults and helper functions related to getting user config and command line arguments."""

import json
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from importlib import metadata
from pathlib import Path

import bing_rewards

try:
    __version = metadata.version('bing_rewards')
except metadata.PackageNotFoundError:
    __version = 'X.X.X+local'

# Number of searches to make
DESKTOP_COUNT = 33
MOBILE_COUNT = 23

# Time to allow Chrome to load in seconds
LOAD_DELAY = 1.5
# Time between searches in seconds
# Searches does not count if they are done earlier than ~6 seconds
SEARCH_DELAY = 6

# Bing Search base url, with new form= parameter (code differs per browser?)
URL = 'https://www.bing.com/search?form=QBRE&q='

# Edge Browser user agents
# Makes Google Chrome look like MS Edge to Bing
MOBILE_AGENT = (
    'Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/AP2A.240605.024) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/121.0.0.0 Mobile Safari/537.36 Edge/121.0.2277.138'
)

DESKTOP_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/126.0.0.0 Safari/537.36 Edge/126.0.0.0'
)
# Default Settings dict
SETTINGS = {
    'desktop-count': DESKTOP_COUNT,
    'mobile-count': MOBILE_COUNT,
    'load-delay': LOAD_DELAY,
    'search-delay': SEARCH_DELAY,
    'search-url': URL,
    'desktop-agent': DESKTOP_AGENT,
    'mobile-agent': MOBILE_AGENT,
    'browser-path': 'chrome',
}


def parse_args():
    """Parse all command line arguments and return Namespace."""
    p = ArgumentParser(
        description=bing_rewards.__doc__.format(
            DESKTOP_COUNT=DESKTOP_COUNT,
            MOBILE_COUNT=MOBILE_COUNT,
            VERSION=__version,
            CONFIG=pick_file_location(),
        ),
        epilog='* Repository and issues: https://github.com/jack-mil/bing-search',
        formatter_class=RawDescriptionHelpFormatter,
    )
    p.add_argument('--version', action='version', version=f'%(prog)s v{__version}')
    p.add_argument(
        '-c',
        '--count',
        help='Override the number of searches to perform',
        type=int,
    )
    p.add_argument(
        '--exe',
        help='The full path of the Chrome compatible browser executable',
        type=valid_file,
    )
    p.add_argument(
        '-b',
        '--bing',
        help='Add this flag if your default search engine is Bing',
        action='store_true',
    )
    # Mutually exclusive options. Only one can be present
    group = p.add_mutually_exclusive_group()
    group.add_argument(
        '-d',
        '--desktop',
        help='Do only desktop searches',
        action='store_true',
    )
    group.add_argument(
        '-m',
        '--mobile',
        help='Do only mobile searches (appear as phone browser)',
        action='store_true',
    )

    # Other options
    p.add_argument(
        '--load-delay',
        help='Override the time given to Chrome to load in seconds',
        type=int,
    )
    p.add_argument(
        '--search-delay',
        help='Override the time between searches in seconds',
        type=int,
    )
    p.add_argument(
        '-n',
        '--dryrun',
        help='Do everything but search',
        action='store_true',
    )
    p.add_argument(
        '--open-rewards',
        help='Open the rewards page at the end of the run',
        action='store_true',
    )
    p.add_argument(
        '--no-window',
        help="Don't open a new Chrome window (just press keys)",
        action='store_true',
    )
    p.add_argument(
        '-X',
        '--no-exit',
        help="Don't close the browser window after searching",
        action='store_true',
    )
    p.add_argument(
        '--profile',
        help='Sets the chrome profile for launch',
        type=str,
    )
    p.add_argument(
        '--ime',
        help='Triggers windows IME to switch to english by pressing SHIFT',
        action='store_true',
    )
    args = p.parse_args()
    print(args)
    return args


def valid_file(path: str) -> Path:
    """Check that a string is a file and exists handler for the --exe= flag."""
    exe = Path(path)
    if exe.is_file:
        return exe
    raise FileNotFoundError(path)


def pick_file_location() -> Path:
    r"""Check these locations in order for config.json.

    - %APPDATA%\bing-rewards\
    - $XDG_CONFIG_HOME/bing-rewards/
    - $HOME/.config/bing-rewards/
    """
    # Config file in .config or APPDATA on Windows
    config_home = Path(
        os.environ.get('APPDATA')
        or os.environ.get('XDG_CONFIG_HOME')
        or Path(os.environ['HOME'], '.config'),
        'bing-rewards',
    )

    return config_home.joinpath('config.json')


def read_config() -> dict:
    """Read a configuration file if it exists, otherwise write (and return) default settings."""
    config_file: Path = pick_file_location()

    if not config_file.is_file():
        # Make directories and default config if it doesn't exist
        print(f'Generating config at {config_file}')
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with config_file.open('x') as f:
            json.dump(SETTINGS, f, indent=4)
        return SETTINGS

    # Otherwise, try to read the config from a file
    config = SETTINGS.copy()
    with config_file.open() as f:
        try:
            config = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(e)
            print('Config JSON format error. Reverting to default.')
    # return new dict with values from config taking priority
    return SETTINGS | config
