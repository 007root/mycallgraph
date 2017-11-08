#!/usr/bin/env python

sdict = {
    'name': 'mycallgraph',
    'version': "0.0.1",
    'packages': ['mycallgraph'],
    'install_requires': ['graphviz', 'pycallgraph'],
    'zip_safe': False,
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
