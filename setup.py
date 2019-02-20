#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

__version__ = '1.0.4'
__author__ = 'Agus Makmun (Summon Agus)'
__author_email__ = 'summon.agus@gmail.com'

setup(
    name="nicepay",
    packages=['nicepay'],
    version=__version__,
    platforms=['Linux'],
    url='https://github.com/titipbeliin/nicepay-python-enterprise/',
    download_url='https://github.com/titipbeliin/nicepay-python-enterprise/tarball/v%s' % __version__,
    description="Python API for nicepay.",
    long_description=open("README.rst").read(),
    license='MIT',
    author=__author__,
    author_email=__author_email__,
    keywords=['nicepay', 'python api'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development'
    ]
)
