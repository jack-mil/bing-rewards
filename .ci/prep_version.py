#!/usr/bin/env python
"""
Script to help manage the version file during the CI process.
"""

import argparse
import re
import subprocess


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
    parser.add_argument(
        "--master",
        action="store_true",
        help="Return version for master branch CI",
    )
    parser.add_argument(
        "--develop",
        action="store_true",
        help="Return version for develop branch CI",
    )
    parser.add_argument(
        "--staging",
        action="store_true",
        help="Return version for staging branch CI",
    )
    parser.add_argument(
        "--hotfix",
        action="store_true",
        help="Return version for hotfix branch CI",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Only print post version tag info",
    )
    args = parser.parse_args()

    with open(args.versionfile) as infile:
        line = infile.readline()
        res = re.match(r"^([0-9]+(\.[0-9]+){2})", line)
        if not res:
            raise RuntimeError("Unable to parse version file")
        version = res.group(1)

    proc = subprocess.run(
        "git describe --tags --match build".split(),
        stdout=subprocess.PIPE,
        check=True,
    )

    if not args.master:
        # Pre-version letters
        if args.staging:
            pre_stage = "c"
        elif args.develop:
            pre_stage = "b"
        else:
            pre_stage = "a"

        # Replace string, hotfix vs development branches
        if args.hotfix:
            rep_str = r"-\1"
        else:
            rep_str = pre_stage + r"\1+git.\2"

        # Update the version string
        build = re.sub(r"build-(\d+)-g(\w+)", rep_str, proc.stdout.decode())
        if args.build_only:
            version = build
        else:
            version += build

    # Print the version
    print("{}".format(version))
    if args.inplace:
        with open(args.versionfile, "w") as outfile:
            outfile.write(version)


if __name__ == "__main__":
    _main()
