#!/usr/bin/env python3
# coding: UTF-8

from setuptools import setup
import idapm


setup(
    name="idapm",
    version="0.0.1",
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
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)