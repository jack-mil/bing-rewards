# SPDX-FileCopyrightText: 2020 jack-mil
#
# SPDX-License-Identifier: MIT

"""Defaults and helper functions related to getting user config and command line arguments."""

import dataclasses
import os
import shlex
import sys
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    BooleanOptionalAction,
    Namespace,
    RawDescriptionHelpFormatter,
)
from importlib import metadata, resources
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


def create_parser() -> ArgumentParser:
    """Create and return the main argument parser."""
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

    # Config generation options
    p.add_argument(
        '--init-config',
        help='Generate a template configuration file and exit',
        action='store_true',
    )
    p.add_argument(
        '--output',
        help='Output location for generated config (default: write to config file location)',
        type=str,
        metavar='FILE',
    )
    p.add_argument(
        '--force',
        help='Overwrite existing config file when using --init-config',
        action='store_true',
    )

    # Search options
    p.add_argument(
        '-c',
        '--count',
        help='Override the number of searches to perform. '
             'Format: desktop_count,mobile_count or single value for both. '
             'Examples: --count 50 (both), --count 40,25 (desktop,mobile)',
        type=valid_count,
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
        type=float,
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
    p.add_argument(
        '--search-url',
        help='Override the Bing search URL base',
        type=str,
        metavar='URL',
    )

    return p


def parse_args() -> Namespace:
    """Parse all command line arguments and return Namespace."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle config generation first
    if args.init_config:
        generate_config_template(args)
        sys.exit(0)

    return args


def generate_config_template(args: Namespace) -> None:
    """Generate a configuration template file with all available options."""
    config_content = generate_config_content()

    # Output to stdout
    if args.output == '-' or (args.output is None and sys.stdout.isatty() is False):
        print(config_content)
        return

    # Determine output path to use if specified or default
    output_path = Path(args.output) if args.output else config_location()

    # Check if file exists and has force flag
    if output_path.exists() and not args.force:
        print(f'Config file already exists at {output_path}')
        print('Use --force to overwrite, or --output to specify a different location')
        sys.exit(1)

    # Create parent directories if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with output_path.open('w') as f:
            f.write(config_content)
        print(f'Generated config template at {output_path}')
    except OSError as e:
        print(f'Error writing config file: {e}')
        sys.exit(1)


def generate_config_content() -> str:
    """Read and return the content from the configuration template file."""
    template_file = resources.files('bing_rewards').joinpath('templates', 'config')
    with template_file.open('r', encoding='utf-8') as f:
        return f.read()


def valid_count(value: str) -> int | tuple[int, int]:
    """
    Check that a string is a valid format for the --count flag.
    A valid format looks like:
    --count 50,25
    --count 50
    """
    match value.split(','):
        case [count] if count.isdecimal():
            return int(count)
        case [desktop_count, mobile_count] if (
            desktop_count.isdecimal()
            and mobile_count.isdecimal()
        ):
            return int(desktop_count), int(mobile_count)
        case _:
            raise ArgumentTypeError('Invalid format. Use single number or desktop,mobile counts.')


def valid_range(value: str) -> float | tuple[float, float]:
    """
    Check that a string is a valid format for the --search-delay flag.
    A valid format looks like:
    --search-delay 10,45
    --search-delay 20
    """
    match value.split(','):
        case [sec] if sec.replace('.', '').isdecimal():
            return float(sec)
        case [min_val, max_val] if (
            min_val.replace('.', '').isdecimal()
            and max_val.replace('.', '').isdecimal()
        ):
            min_s, max_s = float(min_val), float(max_val)
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
    r"""Check these locations in order for config.

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

    return config_home.joinpath('config')


def read_cli_config_file() -> Namespace:
    """
    Read a plaintext configuration file and parse it as CLI arguments.

    Returns:
        Namespace with configuration options, or empty Namespace if no config file.
    """
    config_file = config_location()

    if not config_file.is_file():
        return Namespace()

    try:
        with config_file.open('r', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError as e:
        print(f'Error reading config file {config_file}: {e}')
        return Namespace()

    # Parse lines and extract CLI arguments
    config_args = []
    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        try:
            # Use shlex to properly parse quotes
            args = shlex.split(line)
            config_args.extend(args)
        except ValueError as e:
            print(f'Error parsing config file line {line_num}: "{line}"')
            print(f'Parse error: {e}')
            sys.exit(1)

    if not config_args:
        return Namespace()

    # Parse the collected arguments using our argument parser
    parser = create_parser()
    try:
        # Parse config file args, but don't exit on error
        config_namespace = parser.parse_args(config_args)
        return config_namespace
    except SystemExit:
        print(f'Error: Invalid configuration in {config_file}')
        print(f'Config arguments: {" ".join(config_args)}')
        sys.exit(1)


def get_options() -> Namespace:
    """Combine the defaults, config file options, and command line arguments into one Namespace."""
    # 1st - defaults
    default_config = Config()
    merged_dict = dataclasses.asdict(default_config)

    # 2nd - config file
    file_config = read_cli_config_file()
    for key, value in vars(file_config).items():
        if value is not None:
            merged_dict[key] = value

    # 3rd - command line arguments
    args = parse_args()
    for key, value in vars(args).items():
        if value is not None:
            merged_dict[key] = value

    # Handle new --count format (desktop,mobile or single value)
    if hasattr(args, 'count') and args.count is not None:
        if isinstance(args.count, tuple):
            # Format: --count 40,25 (desktop,mobile)
            merged_dict['desktop_count'], merged_dict['mobile_count'] = args.count
        else:
            # Format: --count 50 (both)
            merged_dict['desktop_count'] = args.count
            merged_dict['mobile_count'] = args.count

    result = Namespace(**merged_dict)

    # Ensure all boolean options are set
    result.no_window = not result.window
    result.no_exit = not result.exit

    return result
