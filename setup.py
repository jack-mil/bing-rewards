#!python
import sys

from setuptools import find_packages, setup

assert sys.version_info >= (3, 6), "bing-rewards requires Python 3.6"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    return Path(CURRENT_DIR, "README.md").read_text(encoding="utf8")


def get_version() -> str:
    return Path(CURRENT_DIR, "VERSION").read_text(encoding="utf8")


extras = {
    "dev": ["twine"],
    "lint": [
        "black",
        "flake8",
        "flake8-bugbear",
        "isort",
    ],
}
extras["dev"] += extras["lint"]


setup(
    name="bing-rewards",
    version=get_version(),
    author="jack-mil",
    description="Perform automated Bing Rewards searches",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/jack-mil/bing-rewards",
    project_urls={
        "Issue Tracker": "https://github.com/jack-mil/bing-rewards/issues",
        "Source Code": "https://github.com/jack-mil/bing-rewards",
    },
    keywords="automation bing search pyautogui points xbox",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=["PyAutoGUI"],
    extras_require=extras,
    packages=find_packages(),
    package_data={
        # If any package contains text files, indlude them
        "": ["data/*.txt"]
    },
    zip_safe=False,
    entry_points={"console_scripts": ["bing-rewards = bing_rewards:main"]},
)
