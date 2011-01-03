    Note: This fork tries to separate the general purpose logic from django
    related code so that it can be used with other template engines like
    Jinja2.

typogrify: Filters to make web typography easier
================================================================


This application provides a set of custom filters for the Django
template system which automatically apply various transformations to
plain text in order to yield typographically-improved HTML.


Requirements
============

``typogrify`` is designed to work with `Django`_, and so requires a
functioning installation of Django 0.96 or later. Also requires `the
Python port of John Gruber's SmartyPants`_ for tokenization.

.._ Django: http://www.djangoproject.com/
.._ The Python port of John Gruber's SmartyPants: http://web.chad.org/projects/smartypants.py/


Installation
============

To install a packaged version of ``typogrify``, download `the latest
package from Google Code`_, and -- in the directory in which you
downloaded it -- open a command line and do the following::

    tar zxvf typogrify-0.2.tar.gz
    cd typogrify-0.2
    python setup.py install

This will perform a standard installation of ``typogrify``.

Alternately, you can perform a Subversion checkout of the latest code;
execute the following in a directory that's on your Python path::

    svn checkout http://typogrify.googlecode.com/svn/trunk/typogrify/

Once ``typogrify`` is installed on your system, you can add it to the
``INSTALLED_APPS`` setting of any Django project in which you wish to
use it, and then use ``{% load typogrify %}`` in your templates to
load the filters it provides.


.._ the latest package from Google Code: http://typogrify.googlecode.com/files/typogrify-0.1.tar.gz


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
