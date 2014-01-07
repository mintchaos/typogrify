#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='typogrify',
    version=__import__('typogrify').__version__,
    packages=find_packages(),
    author='Christian Metts, Justin Mayer, Chris Drackett',
    author_email='entroP@gmail.com',
    license='BSD',
    description='Filters to enhance web typography, including support for Django & Jinja templates',
    long_description=open('README.rst').read(),
    url='https://github.com/mintchaos/typogrify',
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
