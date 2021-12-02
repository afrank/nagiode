import os
import setuptools
from setuptools import setup, find_packages

setup(
    name="nagiode",
    version="0.0.1",
    description="Python tool accessing nagios resources",
    python_requires=">=3.4",
    author="Adam Frank",
    author_email="pkgmaint@antilogo.org",
    packages=find_packages(),
    entry_points={"console_scripts": ["nagiode=nagiode.main:main",],},
    install_requires=["bs4","requests"],
    project_urls={"Source": "https://github.com/afrank/nagiode",},
)

