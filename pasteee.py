#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
pastee module
Allows pasting to http://paste.ee
http://github.com/i-ghost/pasteee
"""

import urllib, urllib2, json

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
	paste - str, paste data to send
	private - bool, indicates if paste should be private or public. Default: 0
	lang - str, indicates the syntax highlighting
	key - str, API key. Default: "public"
	desc - str, paste description. Default: ""
	----
	
	Doctests:
	>>> from pasteee import Paste
	>>> paste = Paste(u"Foo bar\\nBaz")
	>>> print paste.keys()
	[u'download', u'raw', u'link', u'id']
	
	Exception doctest:
	>>> from pasteee import Paste
	>>> paste = Paste(u"Foo bar\\nBaz", lang=123456789)
	Traceback (most recent call last):
		File "<stdin>", line 1, in ?
	PasteError: Invalid paste option: invalid_language
	"""
	def __new__(cls, paste, private=0, lang=u"plain", key=u"public", desc=u""):
		if not paste:
			raise PasteError(u"No paste provided")
		request = urllib2.Request("http://paste.ee/api",
						data=urllib.urlencode({
						'paste' : paste,
						'private' : private,
						'language' : lang,
						'key' : key,
						'description' : desc
						}))
		try:
			result = json.loads(urllib2.urlopen(request).read())
			return result["paste"]
		except urllib2.HTTPError:
			print(u"Couldn't send paste")
			raise
		except KeyError:
			raise PasteError(u"Invalid paste option: %s" %(result["error"]))
			
if __name__ == "__main__":
    import doctest
    doctest.testmod()