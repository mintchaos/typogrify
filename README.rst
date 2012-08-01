typogrify: Filters to make web typography easier
================================================================


This application provides a set of custom filters for the Django
template system which automatically apply various transformations to
plain text in order to yield typographically-improved HTML.


Version 2 changes
-----------------

* Django is no longer a requirement. The typogrify filters can be used in any
  environment by importing them from typogrify.filters


Requirements
============

``typogrify`` is a set of functions that take text or html input and mark them up with HTML.
it requires `the Python port of John Gruber's SmartyPants`_ for tokenization.

It includes optional template filters for Django. So you'll need Django if you want to use those.

.._ The Python port of John Gruber's SmartyPants: http://web.chad.org/projects/smartypants.py/


To use with Django
==================

BACKWARDS INCOMPATIBILTY NOTE: Version 2 of typogrify has moved the typogrify
tag to {% load typogrify_tags %} – This necessary to allow the tags files to
import from the rest of the library.

Once ``typogrify`` is installed on your system, you can add it to the
``INSTALLED_APPS`` setting of any Django project in which you wish to
use it, and then use ``{% load typogrify_tags %}`` in your templates to
load the filters it provides.


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
