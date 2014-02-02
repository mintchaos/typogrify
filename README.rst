Typogrify provides a set of custom filters that automatically apply various
transformations to plain text in order to yield typographically-improved HTML.
While often used in conjunction with Jinja_ and Django_ template systems, the
filters can be used in any environment.

.. _Jinja: http://jinja.pocoo.org/
.. _Django: https://www.djangoproject.com/


Installation
============

The following command will install via ``pip``. Pay particular attention to the
package name::

    pip install typogrify

Alternatively, you can run the following command inside the project's root
directory::

    python setup.py install

Last but not least, you can simply move the enclosed ``typogrify`` folder
into your Python path.


Requirements
============

Python 2.3 and above is supported, including Python 3. The only dependency is
SmartyPants_, a Python port of a project by John Gruber.

Installing Jinja_ or Django_ is only required if you intend to use the optional
template filters that are included for those frameworks.

.. _SmartyPants: http://web.chad.org/projects/smartypants.py/


Usage
=====

The filters can be used in any environment by importing them from
``typogrify.filters``::

    from typogrify.filters import typogrify
    content = typogrify(content)

All content within ``<pre>`` and ``<code>`` tags will not be
processed by default. There is an optional second argument that 
lets one incorporate additional tags whose content will be
ignored. Assuming in addition to ``<pre>`` and ``<code>``, 
``<math>`` should also be ignored::

    from typogrify.filters import typogrify
    content = typogrify(content, ["math"])

Seeing as this argument is a list, it can be used to ignore
multiple tags::

    from typogrify.filters import typogrify
    content = typogrify(content, ["list","of","tags"])

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
