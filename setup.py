#!/usr/bin/env python3
# coding: UTF-8

from setuptools import setup

setup(
    name="ida-plugin-installer",
    version="0.0.1",
    description="installer for IDA plugin",
    author="tkmru",
    packages=['installer'],
    entry_points={
        'console_scripts': [
            'idai = installer.cli:main',
        ],
    },
    install_requires=[
        'colorama',
    ],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)