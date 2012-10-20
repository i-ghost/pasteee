*pasteee*
-------------------------

A python module for posting pastes to http://paste.ee

Example usage:

```python
from pasteee import Paste

pasteText = """Some text to paste
Some more text
Foo bar baz
"""
paste = Paste(pasteText, private=1, desc="My first paste")
```

The above will send a private paste with the contents of pasteText with the description "My first paste" using the anonymous API access.

See pasteee.py for more documentation.

Running pasteee.py from the command line will run the included doctests.

Tested on Python 2.6