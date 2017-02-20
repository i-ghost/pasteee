#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
pasteee module
Allows pasting to https://paste.ee
https://github.com/i-ghost/pasteee
"""

# 2 <-> 3
try:
    from urllib.request import urlopen
    from urllib.request import Request as urlrequest
    from urllib.parse import urlencode
    from urllib import error as urlerror
except ImportError:
    from urllib2 import urlopen
    from urllib2 import Request as urlrequest
    from urllib import urlencode
    import urllib2 as urlerror
import json


class PasteError(Exception):
    """Exception class for this module"""
    pass


class Paste(object):
    """A paste.ee dictionary object

    Returns a dictionary containing the following on a successful paste:
    {
        "id":"foobar",
        "link":"https://paste.ee/p/foobar",
        "min":"https://min.paste.ee/foobar",
        "raw":"https://paste.ee/r/foobar",
        "download":"https://paste.ee/d/foobar"
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
    expire - int, expiration time in seconds.
    views - int, expire after this many views.
    encrypted - bool, Doesn't seem to return anything meaningful.

    http://paste.ee/wiki/API:Basics
    ----

    Doctests:
    >>> from pasteee import Paste
    >>> paste = Paste(u"Foo bar\\nBaz")
    >>> print(sorted(paste.keys())) # doctest: +ELLIPSIS
    [...'download', ...'id', ...'link', ...'raw']

    Exception doctest:
    >>> paste = Paste(u"Foo bar\\nBaz", lang=123456789) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    PasteError: Invalid paste option: error_invalid_language

    >>> paste = Paste(u"Foo bar\\nBaz", expire=15, views=10) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    PasteError: Options 'expire' and 'views' are mutually exclusive
    """
    def __new__(cls, paste,
                private=True, lang="plain",
                key="public", desc="",
                expire=0, views=0, encrypted=False):
        if not paste:
            raise PasteError("No paste provided")
        if expire and views:
            # API incorrectly returns success so we raise error locally
            raise PasteError("Options 'expire' and 'views' are mutually exclusive")
        request = urlrequest(
            "https://paste.ee/api",
            data=urlencode(
                {
                    'paste': paste,
                    'private': bool(private),
                    'language': lang,
                    'key': key,
                    'description': desc,
                    'expire': expire,
                    'views': views,
                    'encrypted': bool(encrypted),
                    'format': "json"
                }
            ).encode("utf-8"),
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        try:
            result = json.loads(urlopen(request).read().decode("utf-8"))
            return result["paste"]
        except urlerror.HTTPError:
            print("Couldn't send paste")
            raise
        except KeyError:
            raise PasteError("Invalid paste option: %s" % (result["error"]))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
