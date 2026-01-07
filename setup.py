#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from setuptools import setup, find_packages

"""Setup script for jiraffe"""

pwd = os.path.abspath(os.path.dirname(__file__))
# README
with open(os.path.join(pwd, "README.md"), encoding="utf-8") as f:
    README = f.read()
    f.close()

# call setup
setup(
    name="jiraffe",
    version="2.2.0",
    description="One stop place for exploiting all Jira instances in your proximity.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/0x48piraj/jiraffe",
    author="Piyush Raj <0x48piraj>",
    author_email="piyush@linuxmail.org",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "beautifulsoup4", "packaging"],
    entry_points={"console_scripts": ["jiraffe=jiraffe.__main__:main"]},
)
