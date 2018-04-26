#!/usr/bin/python3
"""Application setup script.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

import rtdb_sync_pub


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        """Run at post install."""
        subprocess.check_call(['pipenv', 'install', '--deploy', '--system'])
        install.run(self)


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
    cmdclass={
        'install': PostInstallCommand,
    },
)
