#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='typogrified',
    version='0.0.0',
    packages=find_packages(),
    author='Justin Mayer',
    author_email='entroP@gmail.com',
    license='BSD',
    description='Filters to enhance web typography, including support for Django & Jinja templates',
    long_description=open('README.rst').read(),
    url='https://github.com/justinmayer/typogrify',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Framework :: Flask',
        'Topic :: Utilities'
    ],

    install_requires=['smartypants>=1.6']
)
