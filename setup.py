#!/usr/bin/env python3
# coding: UTF-8

from setuptools import setup
import idapm

setup(
    name="idapm",
    version="0.1.0",
    description="IDA Plugin Manager",
    author="tkmru",
    packages=['idapm'],
    entry_points={
        'console_scripts': [
            'idapm = idapm.cli:main',
        ],
    },
    install_requires=[
        'colorama',
    ],
    license='GPLv3',
    classifiers=[
        'OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
