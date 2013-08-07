Newbook TEI Autotagger
======================

This script produces [TEI](http://tei-c.org/)-XML from a
plain text source formatted according to some strict criteria.

This script is part of software created by and for the Newbook
[Digital Texts in the Humanities](http://depts.washington.edu/newbook/).


Dependencies
------------
python3

Usage
-----
The autotagger script expects input on STDIN.  An example
text is found in `texts/`

`$cat texts/d48_clean.txt | ./autotagger.py 2>err 1>d48.xml`

This invocation should produce two files, a TEI compliant XML
file called `d48.xml` and a list of error/warning messages 
called `err`.
