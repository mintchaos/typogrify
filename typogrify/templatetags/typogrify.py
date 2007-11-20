# from django.conf import settings
import re
from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def amp(text):
    """Wraps apersands in html with ``<span class="amp">`` so they can be
    styled with CSS. Apersands are also normalized to ``&amp;``. Requires 
    ampersands to have whitespace or an ``&nbsp;`` on both sides.
    
    >>> amp('One & two')
    'One <span class="amp">&amp;</span> two'
    >>> amp('One &amp; two')
    'One <span class="amp">&amp;</span> two'
    >>> amp('One &#38; two')
    'One <span class="amp">&amp;</span> two'

    >>> amp('One&nbsp;&amp;&nbsp;two')
    'One&nbsp;<span class="amp">&amp;</span>&nbsp;two'

    It won't mess up & that are already wrapped, in entities or URLs

    >>> amp('One <span class="amp">&amp;</span> two')
    'One <span class="amp">&amp;</span> two'
    >>> amp('&ldquo;this&rdquo; & <a href="/?that&amp;test">that</a>')
    '&ldquo;this&rdquo; <span class="amp">&amp;</span> <a href="/?that&amp;test">that</a>'

    """
    amp_finder = re.compile(r"(\s|&nbsp;)(&|&amp;|&\#38;)(\s|&nbsp;)")
    return amp_finder.sub(r"""\1<span class="amp">&amp;</span>\3""", text)
# amp = stringfilter(amp)

def caps(text):
    """Wraps multiple capital letters in ``<span class="caps">`` 
    so they can be styled with CSS. 
    
    >>> caps("A message from KU")
    'A message from <span class="caps">KU</span>'
    
    Uses the smartypants tokenizer to not screw with HTML or with tags it shouldn't.
    
    >>> caps("<PRE>CAPS</pre> more CAPS")
    '<PRE>CAPS</pre> more <span class="caps">CAPS</span>'

    >>> caps("A message from 2KU2 with digits")
    'A message from <span class="caps">2KU2</span> with digits'
        
    >>> caps("Dotted caps followed by spaces should never include them in the wrap D.O.T.   like so.")
    'Dotted caps followed by spaces should never include them in the wrap <span class="caps">D.O.T.</span>  like so.'

    >>> caps("<i>D.O.T.</i>HE34T<b>RFID</b>")
    '<i><span class="caps">D.O.T.</span></i><span class="caps">HE34T</span><b><span class="caps">RFID</span></b>'
    """
    try:
        import smartypants
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% caps %} filter: The Python SmartyPants library isn't installed."
        return text
        
    tokens = smartypants._tokenize(text)
    result = []
    in_skipped_tag = False    
    
    cap_finder = re.compile(r"""(
                            (\b[A-Z\d]*        # Group 2: Any amount of caps and digits
                            [A-Z]\d*[A-Z]      # A cap string much at least include two caps (but they can have digits between them)
                            [A-Z\d]*\b)        # Any amount of caps and digits
                            | (\b[A-Z]+\.\s?   # OR: Group 3: Some caps, followed by a '.' and an optional space
                            (?:[A-Z]+\.\s?)+)  # Followed by the same thing at least once more
                            (?:\s|\b|$))
                            """, re.VERBOSE)

    def _cap_wrapper(matchobj):
        """This is necessary to keep dotted cap strings to pick up extra spaces"""
        if matchobj.group(2):
            return """<span class="caps">%s</span>""" % matchobj.group(2)
        else:
            if matchobj.group(3)[-1] == " ":
                caps = matchobj.group(3)[:-1]
                tail = ' '
            else:
                caps = matchobj.group(3)
                tail = ''
            return """<span class="caps">%s</span>%s""" % (caps, tail)

    tags_to_skip_regex = re.compile("<(/)?(?:pre|code|kbd|script|math)[^>]*>", re.IGNORECASE)
    
    
    for token in tokens:
        if token[0] == "tag":
            # Don't mess with tags.
            result.append(token[1])
            close_match = tags_to_skip_regex.match(token[1])
            if close_match and close_match.group(1) == None:
                in_skipped_tag = True
            else:
                in_skipped_tag = False
        else:
            if in_skipped_tag:
                result.append(token[1])
            else:
                result.append(cap_finder.sub(_cap_wrapper, token[1]))
            
    return "".join(result)
# caps = stringfilter(caps)

def initial_quotes(text):
    """Wraps initial quotes in ``class="dquo"`` for double quotes or  
    ``class="quo"`` for single quotes. Works in these block tags ``(h1-h6, p, li, dt, dd)``
    and also accounts for potential opening inline elements ``a, em, strong, span, b, i``
    
    >>> initial_quotes('"With primes"')
    '<span class="dquo">"</span>With primes"'
    >>> initial_quotes("'With single primes'")
    '<span class="quo">\\'</span>With single primes\\''
    
    >>> initial_quotes('<a href="#">"With primes and a link"</a>')
    '<a href="#"><span class="dquo">"</span>With primes and a link"</a>'
    
    >>> initial_quotes('&#8220;With smartypanted quotes&#8221;')
    '<span class="dquo">&#8220;</span>With smartypanted quotes&#8221;'
    """
    quote_finder = re.compile(r"""((<(p|h[1-6]|li|dt|dd)[^>]*>|^)              # start with an opening p, h1-6, li, dd, dt or the start of the string
                                  \s*                                          # optional white space! 
                                  (<(a|em|span|strong|i|b)[^>]*>\s*)*)         # optional opening inline tags, with more optional white space for each.
                                  (("|&ldquo;|&\#8220;)|('|&lsquo;|&\#8216;))  # Find me a quote! (only need to find the left quotes and the primes)
                                                                               # double quotes are in group 7, singles in group 8 
                                  """, re.VERBOSE)
    def _quote_wrapper(matchobj):
        if matchobj.group(7): 
            classname = "dquo"
            quote = matchobj.group(7)
        else:
            classname = "quo"
            quote = matchobj.group(8)
        return """%s<span class="%s">%s</span>""" % (matchobj.group(1), classname, quote) 
        
    return quote_finder.sub(_quote_wrapper, text)
# initial_quotes = stringfilter(initial_quotes)

def smartypants(text):
    """Applies smarty pants to curl quotes.
    
    >>> smartypants('The "Green" man')
    'The &#8220;Green&#8221; man'
    """
    try:
        import smartypants
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% smartypants %} filter: The Python smartypants library isn't installed."
        return text
    else:
        return smartypants.smartyPants(text)
# smartypants = stringfilter(smartypants)

def typogrify(text):
    """The super typography filter
    
    Applies the following filters: widont, smartypants, caps, amp, initial_quotes
    
    >>> typogrify('<h2>"Jayhawks" & KU fans act extremely obnoxiously</h2>')
    '<h2><span class="dquo">&#8220;</span>Jayhawks&#8221; <span class="amp">&amp;</span> <span class="caps">KU</span> fans act extremely&nbsp;obnoxiously</h2>'
    """
    text = amp(text)
    text = widont(text)
    text = smartypants(text)
    text = caps(text)
    text = initial_quotes(text)
    return text
# typogrify = stringfilter(typogrify)

def widont(text):
    """Replaces the space between the last two words in a string with ``&nbsp;``
    Works in these block tags ``(h1-h6, p, li, dd, dt)`` and also accounts for 
    potential closing inline elements ``a, em, strong, span, b, i``
    
    >>> widont('A very simple test')
    'A very simple&nbsp;test'

    Single word items shouldn't be changed
    >>> widont('Test')
    'Test'
    >>> widont(' Test')
    ' Test'
    >>> widont('<ul><li>Test</p></li><ul>')
    '<ul><li>Test</p></li><ul>'
    >>> widont('<ul><li> Test</p></li><ul>')
    '<ul><li> Test</p></li><ul>'
    
    >>> widont('<p>In a couple of paragraphs</p><p>paragraph two</p>')
    '<p>In a couple of&nbsp;paragraphs</p><p>paragraph&nbsp;two</p>'
    
    >>> widont('<h1><a href="#">In a link inside a heading</i> </a></h1>')
    '<h1><a href="#">In a link inside a&nbsp;heading</i> </a></h1>'
    
    >>> widont('<h1><a href="#">In a link</a> followed by other text</h1>')
    '<h1><a href="#">In a link</a> followed by other&nbsp;text</h1>'

    Empty HTMLs shouldn't error
    >>> widont('<h1><a href="#"></a></h1>') 
    '<h1><a href="#"></a></h1>'
    
    >>> widont('<div>Divs get no love!</div>')
    '<div>Divs get no love!</div>'
    
    >>> widont('<pre>Neither do PREs</pre>')
    '<pre>Neither do PREs</pre>'
    
    >>> widont('<div><p>But divs with paragraphs do!</p></div>')
    '<div><p>But divs with paragraphs&nbsp;do!</p></div>'
    """
    widont_finder = re.compile(r"""((?:</?(?:a|em|span|strong|i|b)[^>]*>)|[^<>\s]) # must be proceeded by an approved inline opening or closing tag or a nontag/nonspace
                                   \s+                                # the space to replace
                                   ([^<>\s]+                            # must be flollowed by non-tag non-space characters
                                   \s*                                  # optional white space! 
                                   (</(a|em|span|strong|i|b)>\s*)* # optional closing inline tags with optional white space after each
                                   ((</(p|h[1-6]|li|dt|dd)>)|$))                 # end with a closing p, h1-6, li or the end of the string
                                   """, re.VERBOSE)
    return widont_finder.sub(r'\1&nbsp;\2', text)
# widont = stringfilter(widont)

register.filter('amp', amp)
register.filter('caps', caps)
register.filter('initial_quotes', initial_quotes)
register.filter('smartypants', smartypants)
register.filter('typogrify', typogrify)
register.filter('widont', widont)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
