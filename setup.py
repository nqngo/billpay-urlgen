#!/usr/bin/env python
# coding: utf-8
"""Packaging logic Billpay urlgen"""

from setuptools import find_packages
from setuptools import setup

setup(
    name="billpay",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click~=7.0",
        "pyyaml~=5.0",
    ],
    entry_points={
        "console_scripts": [
            "billpay=billpay:cli",
        ]
    },
)
