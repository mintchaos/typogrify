from typogrify import Typogrify, TypogrifyError
from functools import wraps
from django.conf import settings
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

register = template.Library()

def make_safe(f):
    @wraps(f)
    def wrapper(text):
        text = force_unicode(text)
        f.is_safe = True
        out = text
        try:
            out = f(text)
        except TypogrifyError, e:
            if settings.DEBUG:
                raise template.TemplateError(e.message)
            return text
        return mark_safe(out)
    wrapper.is_safe = True
    return wrapper

@make_safe
def amp(text):
    """Wraps apersands in HTML with ``<span class="amp">`` so they can be
    styled with CSS. Apersands are also normalized to ``&amp;``. Requires
    ampersands to have whitespace or an ``&nbsp;`` on both sides.

    >>> amp('One & two')
    u'One <span class="amp">&amp;</span> two'
    >>> amp('One &amp; two')
    u'One <span class="amp">&amp;</span> two'
    >>> amp('One &#38; two')
    u'One <span class="amp">&amp;</span> two'

    >>> amp('One&nbsp;&amp;&nbsp;two')
    u'One&nbsp;<span class="amp">&amp;</span>&nbsp;two'

    It won't mess up & that are already wrapped, in entities or URLs

    >>> amp('One <span class="amp">&amp;</span> two')
    u'One <span class="amp">&amp;</span> two'
    >>> amp('&ldquo;this&rdquo; & <a href="/?that&amp;test">that</a>')
    u'&ldquo;this&rdquo; <span class="amp">&amp;</span> <a href="/?that&amp;test">that</a>'

    It should ignore standalone amps that are in attributes
    >>> amp('<link href="xyz.html" title="One & Two">xyz</link>')
    u'<link href="xyz.html" title="One & Two">xyz</link>'
    """
    return Typogrify.amp(text)

@make_safe
def caps(text):
    """Wraps multiple capital letters in ``<span class="caps">``
    so they can be styled with CSS.

    >>> caps("A message from KU")
    u'A message from <span class="caps">KU</span>'

    Uses the smartypants tokenizer to not screw with HTML or with tags it shouldn't.

    >>> caps("<PRE>CAPS</pre> more CAPS")
    u'<PRE>CAPS</pre> more <span class="caps">CAPS</span>'

    >>> caps("A message from 2KU2 with digits")
    u'A message from <span class="caps">2KU2</span> with digits'

    >>> caps("Dotted caps followed by spaces should never include them in the wrap D.O.T.   like so.")
    u'Dotted caps followed by spaces should never include them in the wrap <span class="caps">D.O.T.</span>  like so.'

    All caps with with apostrophes in them shouldn't break. Only handles dump apostrophes though.
    >>> caps("JIMMY'S")
    u'<span class="caps">JIMMY\\'S</span>'

    >>> caps("<i>D.O.T.</i>HE34T<b>RFID</b>")
    u'<i><span class="caps">D.O.T.</span></i><span class="caps">HE34T</span><b><span class="caps">RFID</span></b>'
    """
    return Typogrify.caps(text)

@make_safe
def initial_quotes(text):
    """Wraps initial quotes in ``class="dquo"`` for double quotes or
    ``class="quo"`` for single quotes. Works in these block tags ``(h1-h6, p, li, dt, dd)``
    and also accounts for potential opening inline elements ``a, em, strong, span, b, i``

    >>> initial_quotes('"With primes"')
    u'<span class="dquo">"</span>With primes"'
    >>> initial_quotes("'With single primes'")
    u'<span class="quo">\\'</span>With single primes\\''

    >>> initial_quotes('<a href="#">"With primes and a link"</a>')
    u'<a href="#"><span class="dquo">"</span>With primes and a link"</a>'

    >>> initial_quotes('&#8220;With smartypanted quotes&#8221;')
    u'<span class="dquo">&#8220;</span>With smartypanted quotes&#8221;'
    """
    return Typogrify.initial_quotes(text)

@make_safe
def smartypants(text):
    """Applies smarty pants to curl quotes.

    >>> smartypants('The "Green" man')
    u'The &#8220;Green&#8221; man'
    """
    return Typogrify.smartypants(text)

@make_safe
def titlecase(text):
    """Support for titlecase.py's titlecasing

    >>> titlecase("this V that")
    u'This v That'

    >>> titlecase("this is just an example.com")
    u'This Is Just an example.com'
    """
    return Typogrify.titlecase(text)

@make_safe
def typogrify(text):
    """The super typography filter

    Applies the following filters: widont, smartypants, caps, amp, initial_quotes

    >>> typogrify('<h2>"Jayhawks" & KU fans act extremely obnoxiously</h2>')
    u'<h2><span class="dquo">&#8220;</span>Jayhawks&#8221; <span class="amp">&amp;</span> <span class="caps">KU</span> fans act extremely&nbsp;obnoxiously</h2>'

    Each filters properly handles autoescaping.
    >>> conditional_escape(typogrify('<h2>"Jayhawks" & KU fans act extremely obnoxiously</h2>'))
    u'<h2><span class="dquo">&#8220;</span>Jayhawks&#8221; <span class="amp">&amp;</span> <span class="caps">KU</span> fans act extremely&nbsp;obnoxiously</h2>'
    """
    text = force_unicode(text)
    return Typogrify.typogrify(text)

@make_safe
def widont(text):
    """Replaces the space between the last two words in a string with ``&nbsp;``
    Works in these block tags ``(h1-h6, p, li, dd, dt)`` and also accounts for
    potential closing inline elements ``a, em, strong, span, b, i``

    >>> widont('A very simple test')
    u'A very simple&nbsp;test'

    Single word items shouldn't be changed
    >>> widont('Test')
    u'Test'
    >>> widont(' Test')
    u' Test'
    >>> widont('<ul><li>Test</p></li><ul>')
    u'<ul><li>Test</p></li><ul>'
    >>> widont('<ul><li> Test</p></li><ul>')
    u'<ul><li> Test</p></li><ul>'

    >>> widont('<p>In a couple of paragraphs</p><p>paragraph two</p>')
    u'<p>In a couple of&nbsp;paragraphs</p><p>paragraph&nbsp;two</p>'

    >>> widont('<h1><a href="#">In a link inside a heading</i> </a></h1>')
    u'<h1><a href="#">In a link inside a&nbsp;heading</i> </a></h1>'

    >>> widont('<h1><a href="#">In a link</a> followed by other text</h1>')
    u'<h1><a href="#">In a link</a> followed by other&nbsp;text</h1>'

    Empty HTMLs shouldn't error
    >>> widont('<h1><a href="#"></a></h1>')
    u'<h1><a href="#"></a></h1>'

    >>> widont('<div>Divs get no love!</div>')
    u'<div>Divs get no love!</div>'

    >>> widont('<pre>Neither do PREs</pre>')
    u'<pre>Neither do PREs</pre>'

    >>> widont('<div><p>But divs with paragraphs do!</p></div>')
    u'<div><p>But divs with paragraphs&nbsp;do!</p></div>'
    """
    return Typogrify.widont(text)

register.filter('amp', amp)
register.filter('caps', caps)
register.filter('initial_quotes', initial_quotes)
register.filter('smartypants', smartypants)
register.filter('titlecase', titlecase)
register.filter('typogrify', typogrify)
register.filter('widont', widont)

def _test():
    """
    How to run this:
    go two levels up to the root typogrify directory.
    $ ls
    INSTALL.txt MANIFEST    README.markdown typogrify
    LICENSE.txt MANIFEST.in setup.py
    $ python -m typogrify.templatetags.filters
    """
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    _test()
