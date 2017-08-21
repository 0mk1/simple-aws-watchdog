#!/usr/bin/env python3from codecs import open
from setuptools import find_packages, setup

from aws_watchdog import __version__


setup(
    name='aws_watchdog',
    version=__version__,
    description='',
    url='https://bitbucket.org/toffi9/aws-watchdog',
    author='Mateusz Kamycki',
    author_email='mateusz.kamycki@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'click==6.7',
        'boto3==1.4.6',
        'python-daemon==2.1.2',
    ],
    entry_points={
        'console_scripts': [
            'aws_watchdog=aws_watchdogd',
        ],
    },
)
