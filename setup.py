#!/usr/bin/python3
"""Application setup script.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

from setuptools import setup, find_packages

import rtdb_sync_pub


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    description = long_description.split('\n', 1)[0]

setup(
    name="rtdb-sync-pub",
    version=rtdb_sync_pub.__version__,
    url="https://gitlab.com/sorbotics/rtdb-sync-pub/",
    author="Yeiniel Suarez Sosa",
    author_email="yeiniel@gmail.com",
    packages=find_packages(exclude=['tests']),
    description=description,
    long_description=long_description,
    entry_points={
        "console_scripts": [
            "rtdb_sync_pub = rtdb_sync_pub.launcher"
        ]
    },
    install_requires=[
        "configargparse==0.13.0",
        "hiredis==0.2.0",
        "paho-mqtt==1.3.1",
        "redis==2.10.6"
    ]
)
