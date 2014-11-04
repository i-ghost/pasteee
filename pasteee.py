#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
pasteee module
Allows pasting to http://paste.ee
http://github.com/i-ghost/pasteee
"""

import urllib
import urllib2
import json


class PasteError(Exception):
    """Exception class for this module"""
    pass


class Paste(object):
    """A paste.ee dictionary object

    Returns a dictionary containing the following on a successful paste:
    {
        "id":"foobar",
        "link":"http://paste.ee/p/foobar",
        "raw":"http://paste.ee/r/foobar",
        "download":"http://paste.ee/d/foobar"
    }

    Raises a PasteError on an unsuccessful paste.

    Options:
    ----
    paste - str, paste data to send.
    private - bool, indicates if paste should be private or public. \
    Default: True
    lang - str, indicates the syntax highlighting.
    key - str, API key. Default: "public".
    desc - str, paste description. Default: ""
    expire - int, expiration time in minutes.
    views - int, expire after this many views.
    encrypted - bool, Doesn't seem to return anything meaningful.

    http://paste.ee/wiki/API:Basics
    ----

    Doctests:
    >>> from pasteee import Paste
    >>> paste = Paste(u"Foo bar\\nBaz")
    >>> print paste.keys()
    [u'download', u'raw', u'link', u'id', u'min']

    Exception doctest:
    >>> paste = Paste(u"Foo bar\\nBaz", lang=123456789)
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    PasteError: Invalid paste option: error_invalid_language

    >>> paste = Paste(u"Foo bar\\nBaz", expire=15, views=10)
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    PasteError: Options 'expire' and 'views' are mutually exclusive
    """
    def __new__(cls, paste,
                private=True, lang=u"plain",
                key=u"public", desc=u"",
                expire=0, views=0, encrypted=False):
        if not paste:
            raise PasteError(u"No paste provided")
        if expire and views:
            # API incorrectly returns success so we raise error locally
            raise PasteError(u"Options 'expire' and 'views' are mutually exclusive")
        request = urllib2.Request(
            "https://paste.ee/api",
            data=urllib.urlencode(
                {
                    'paste': paste,
                    'private': bool(private),
                    'language': lang,
                    'key': key,
                    'description': desc,
                    'expire': expire,
                    'encrypted': bool(encrypted),
                    'format': "json"
                }
            )
        )
        try:
            result = json.loads(urllib2.urlopen(request).read())
            return result["paste"]
        except urllib2.HTTPError:
            print(u"Couldn't send paste")
            raise
        except KeyError:
            raise PasteError(u"Invalid paste option: %s" % (result["error"]))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
