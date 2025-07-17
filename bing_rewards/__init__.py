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

# This package does not export any programmatic API
# Run as an installed application or as a module
