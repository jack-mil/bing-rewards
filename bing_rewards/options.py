# SPDX-FileCopyrightText: 2020 jack-mil
#
# SPDX-License-Identifier: MIT

"""Defaults and helper functions related to getting user config and command line arguments."""

import dataclasses
import json
import os
import sys
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    BooleanOptionalAction,
    Namespace,
    RawDescriptionHelpFormatter,
)
from importlib import metadata
from pathlib import Path

import bing_rewards

try:
    __version = metadata.version('bing_rewards')
except metadata.PackageNotFoundError:
    __version = 'unknown+local'

# Number of searches to make
DESKTOP_COUNT = 33
MOBILE_COUNT = 23

# Time to allow Chrome to load in seconds
LOAD_DELAY = 1.5

# Time between searches in seconds
# Searches may not be counted if done too quickly
SEARCH_DELAY = 6.0

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


@dataclasses.dataclass()
class Config:
    """Default settings for file config and types."""

    desktop_count: int = DESKTOP_COUNT
    mobile_count: int = MOBILE_COUNT
    load_delay: float = LOAD_DELAY
    search_delay: float | tuple[float, float] = SEARCH_DELAY
    search_url: str = URL
    desktop_agent: str = DESKTOP_AGENT
    mobile_agent: str = MOBILE_AGENT
    browser_path: str = 'chrome'
    bing: bool = False  # True means Bing is default search engine
    open_rewards: bool = False
    window: bool = True
    exit: bool = True
    ime: bool = False
    profile: list[str] = dataclasses.field(default_factory=lambda: ['Default'])


def parse_args() -> Namespace:
    """Parse all command line arguments and return Namespace."""
    p = ArgumentParser(
        description=bing_rewards.__doc__.format(
            DESKTOP_COUNT=DESKTOP_COUNT,
            MOBILE_COUNT=MOBILE_COUNT,
            VERSION=__version,
            CONFIG=config_location(),
        ),
        epilog='* Repository and issues: https://github.com/jack-mil/bing-search',
        formatter_class=RawDescriptionHelpFormatter,
        prog=Path(sys.argv[0]).name,
    )

    if sys.version_info >= (3, 14):
        p.suggest_on_error = True  # pyright: ignore[reportUnreachable]
        p.color = True

    p.add_argument('--version', action='version', version=f'%(prog)s v{__version}')
    p.add_argument(
        '-c',
        '--count',
        help='Override the number of searches to perform',
        type=int,
    )
    p.add_argument(
        '-b',
        '--bing',
        help='Add this flag if your default search engine is Bing',
        action=BooleanOptionalAction,
        default=None,
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
        '--exe',
        help='The full path of the Chrome compatible browser executable',
        type=valid_file,
        dest='browser_path',
    )
    p.add_argument(
        '--load-delay',
        help='Override the time given to Chrome to load in seconds',
        metavar='SEC',
        type=int,
    )
    p.add_argument(
        '--search-delay',
        help=(
            'Override the time between searches in seconds.\t'
            'Can be a single value, or comma separated range (e.g. 10,45)'
        ),
        metavar='MIN[,MAX]',
        type=valid_range,
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
        action=BooleanOptionalAction,
        default=None,
    )
    p.add_argument(
        '--window',
        help='Open a new Chrome window (default: True)',
        action=BooleanOptionalAction,
        default=None,
    )
    p.add_argument(
        '-X',
        '--exit',
        help='Close the browser window after searching (default: True)',
        action=BooleanOptionalAction,
        default=None,
    )
    p.add_argument(
        '--ime',
        help='Triggers windows IME to switch to english by pressing SHIFT',
        action=BooleanOptionalAction,
        default=None,
    )
    p.add_argument(
        '--profile',
        help='Sets one or more chrome profiles to run sequentially (space separated)',
        type=str,
        nargs='+',
    )
    args = p.parse_args()
    return args


def valid_range(value: str) -> float | tuple[float, float]:
    """
    Check that a string is a valid format for the --search-delay flag.
    A valid format looks like:
    --search-delay 10,45
    --search-delay 20
    """
    match value.split(','):
        case [sec] if sec.isdecimal():
            return float(sec)
        case [min, max] if min.isdecimal() and max.isdecimal():
            min_s, max_s = float(min), float(max)
            if max_s <= min_s:
                raise ArgumentTypeError('Max delay should be greater than min.')
            return min_s, max_s
        case _:
            raise ArgumentTypeError('Invalid format. Use numeric value or range.')


def valid_file(path: str) -> Path:
    """Check that a string is a file and exists handler for the --exe= flag."""
    exe = Path(path)
    if exe.is_file:
        return exe
    raise FileNotFoundError(path)


def config_location() -> Path:
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


def read_config() -> Config:
    """Read a configuration file if it exists, otherwise write (and return) default settings."""
    config_file: Path = config_location()

    if not config_file.is_file():
        # Make directories and default config if it doesn't exist
        print(f'Generating config at {config_file}')
        config_file.parent.mkdir(parents=True, exist_ok=True)
        default_options = Config()
        with config_file.open('x') as f:
            json.dump(dataclasses.asdict(default_options), f, indent=2)
        return default_options

    # Otherwise, try to read the config from a file
    config = {}
    with config_file.open() as f:
        try:
            config = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(e)
            print('Config JSON format error. Reverting to default.')
    # return dataclass with values from config taking priority
    return Config(**config)


def get_options() -> Namespace:
    """Combine the defaults, config file options, and command line arguments into one Namespace."""
    file_config = read_config()
    args = parse_args()

    # Start with config file values
    merged_dict = dataclasses.asdict(file_config)

    # Override config values with command line args if provided
    for key, value in vars(args).items():
        if value is not None:
            merged_dict[key] = value
    result = Namespace(**merged_dict)

    # Ensure all boolean options are set
    result.no_window = not result.window
    result.no_exit = not result.exit

    return result
