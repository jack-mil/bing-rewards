#!python
from setuptools import setup, find_packages
import sys

assert sys.version_info >= (3, 6), "bing-rewards requires Python 3.6"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    return Path(CURRENT_DIR, "README.md").read_text(encoding="utf8")


def get_requirments() -> str:
    return Path(CURRENT_DIR, "requirements.txt").read_text(encoding="utf8").splitlines()


setup(
    name="bing-rewards",
    version="0.2.0",
    author="jack-mil",
    description="Perform automated Bing Rewards searches",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="automation bing search pyautogui points xbox",
    url="https://github.com/jack-mil/bing-rewards",
    license="MIT",
    packages=find_packages(),
    package_data={
        # If any package contains text files, indlude them
        "": ["data/*.txt"]
        },
    zip_safe=False,
    install_requires=get_requirments(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["bing-rewards = bing_rewards:main"]},
)
