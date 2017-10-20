# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='c2xt',
    version='0.1.0',
    description='command-line tool for translating C header files into xtlang code',
    long_description=readme,
    author='Ben Swift',
    author_email='ben@benswift.me',
    url='https://github.com/benswift/c2xt',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

