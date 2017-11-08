#!/usr/bin/env python

sdict = {
    'name': 'pycall',
    'version': "0.0.1",
    'packages': ['pycall'],
    'zip_safe': False,
    'install_requires': ['django'],
    'author': 'WZS',
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**sdict)
