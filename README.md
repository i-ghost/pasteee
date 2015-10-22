*pasteee*
-------------------------

[![Build Status](https://travis-ci.org/i-ghost/pasteee.svg)](https://travis-ci.org/i-ghost/pastee)

A python module for posting pastes to http://paste.ee

Example usage:

```python
from pasteee import Paste

pasteText = """Some text to paste
Some more text
Foo bar baz
"""
paste = Paste(pasteText, private=False, desc="My first paste", views=15)
```

The above will send a public paste with the contents of pasteText with the description "My first paste" using the anonymous API access, and the paste will expire after fifteen views.

Pastes are sent privately by default.

See pasteee.py for more documentation.

Running pasteee.py from the command line will run the included doctests.

Tested on Python 2.6