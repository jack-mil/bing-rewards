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

    parts[2] = str(int(parts[2]) + 1)
    version = ".".join(parts)

    # Print the version
    print("{}".format(version))
    if args.inplace:
        with open(args.versionfile, "w") as outfile:
            print(version, file=outfile)


if __name__ == "__main__":
    _main()
