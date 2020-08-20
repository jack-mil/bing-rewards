from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="bing-rewards",
    version="0.2.0",
    author="jack-mil",
    description="Perform automated Bing rewards searches",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jack-mil/bing-rewards",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['bing-rewards = bing_rewards.bing_rewards:main']},
    python_requires='>=3.6',
)