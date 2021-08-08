#!/usr/bin/env python
"""
Script for bumping the version
"""

import argparse
import re


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "versionfile",
        type=str,
        help="The version file to manage",
    )
    parser.add_argument(
        "--major",
        action="store_true",
        help="Update major",
    )
    parser.add_argument(
        "--minor",
        action="store_true",
        help="Update major",
    )
    parser.add_argument(
        "--micro",
        action="store_true",
        help="Update micro",
    )
    parser.add_argument(
        "--inplace",
        "-i",
        action="store_true",
        help="Update the version file in place",
    )
    args = parser.parse_args()

    with open(args.versionfile) as infile:
        line = infile.readline()
        res = re.match(r"^([0-9]+(\.[0-9]+){2})", line)
        if not res:
            raise RuntimeError("Unable to parse version file")
        version = res.group(1)

    parts = version.split(".")
    if args.major:
        parts[0] = str(int(parts[0]) + 1)
    elif args.minor:
        parts[1] = str(int(parts[1]) + 1)
    else:  # Micro
        parts[2] = str(int(parts[2]) + 1)

    version = ".".join(parts)

    # Print the version
    print("{}".format(version))
    if args.inplace:
        with open(args.versionfile, "w", newline="\n") as outfile:
            outfile.write(version)


if __name__ == "__main__":
    _main()
