Typogrify |build-status| |pypi-version|
#######################################

Typogrify provides a set of custom filters that automatically apply various
transformations to plain text in order to yield typographically-improved HTML.
While often used in conjunction with Jinja_ and Django_ template systems, the
filters can be used in any environment.

.. _Jinja: https://jinja.palletsprojects.com/
.. _Django: https://www.djangoproject.com/


Installation
============

The following command will install via ``pip``. Pay particular attention to the
package name::

    python -m pip install typogrify


Requirements
============

Python 3.6 and above is supported. The only dependency is SmartyPants_,
a Python port of a project by John Gruber.

Installing Jinja_ or Django_ is only required if you intend to use the optional
template filters that are included for those frameworks.

.. _SmartyPants: http://web.chad.org/projects/smartypants.py/


Usage
=====

The filters can be used in any environment by importing them from
``typogrify.filters``::

    from typogrify.filters import typogrify
    content = typogrify(content)

For use with Django, you can add ``typogrify`` to the ``INSTALLED_APPS`` setting
of any Django project in which you wish to use it, and then use
``{% load typogrify_tags %}`` in your templates to load the filters it provides.

Experimental support for Jinja is in ``typogrify.templatetags.jinja_filters``.


Included filters
================

``amp``
-------

Wraps ampersands in HTML with ``<span class="amp">`` so they can be
styled with CSS. Ampersands are also normalized to ``&amp;``. Requires
ampersands to have whitespace or an ``&nbsp;`` on both sides. Will not
change any ampersand which has already been wrapped in this fashion.


``caps``
--------

Wraps multiple capital letters in ``<span class="caps">`` so they can
be styled with CSS.


``initial_quotes``
------------------

Wraps initial quotes in ``<span class="dquo">`` for double quotes or
``<span class="quo">`` for single quotes. Works inside these block
elements:

* ``h1``, ``h2``, ``h3``, ``h4``, ``h5``, ``h6``

* ``p``

* ``li``

* ``dt``

* ``dd``

Also accounts for potential opening inline elements: ``a``, ``em``,
``strong``, ``span``, ``b``, ``i``.


``smartypants``
---------------

Applies ``SmartyPants``.


``typogrify``
-------------

Applies all of the following filters, in order:

* ``amp``

* ``widont``

* ``smartypants``

* ``caps``

* ``initial_quotes``


``widont``
----------

Based on Shaun Inman's PHP utility of the same name, replaces the
space between the last two words in a string with ``&nbsp;`` to avoid
a final line of text with only one word.

Works inside these block elements:

* ``h1``, ``h2``, ``h3``, ``h4``, ``h5``, ``h6``

* ``p``

* ``li``

* ``dt``

* ``dd``

Also accounts for potential closing inline elements: ``a``, ``em``,
``strong``, ``span``, ``b``, ``i``.


Development
===========

To set up your development environment, first clone the project. Then create
and activate a new virtual environment. From within the project, run::

    python -m pip install invoke
    invoke setup

Each time you make changes to Typogrify, there are two things to do regarding
tests: check that the existing tests pass, and add tests for any new features
or bug fixes. You can run the tests via::

    invoke tests

In addition to running the test suite, it is important to also ensure that any
lines you changed conform to code style guidelines. You can check that via::

    invoke lint


.. |build-status| image:: https://img.shields.io/github/workflow/status/mintchaos/typogrify/build
   :target: https://github.com/mintchaos/typogrify/actions
   :alt: GitHub Actions CI: continuous integration status
.. |pypi-version| image:: https://img.shields.io/pypi/v/typogrify.svg
   :target: https://pypi.org/project/typogrify/
   :alt: PyPI Version
