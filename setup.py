#!/usr/bin/env python

USE_SETUPTOOLS = False
try:
    from setuptools import setup, Extension
    USE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup, Extension


setup_kwargs = dict(
    name='greendns',
    description='''A module for providing greened DNS access via dnspython ''',
    version='0.1.0',
    author='R. Tyler Ballance',
    author_email='tyler@monkeypox.org',
    py_modules=['greendns',],
    url='http://rtyler.github.com/greendns')

if USE_SETUPTOOLS:
    setup_kwargs.update({'test_suite' : 'test_greendns'})

setup(**setup_kwargs)
