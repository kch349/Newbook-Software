#!/usr/bin/env python3
# autotagger web interface
# 

import cgi
import autotagger
import codecs
import sys
import os
from random import randint

HTTP_HEADERS = "Content-type: text/html\n"

WELCOME_PAGE = """
<html>
<head><title>Newbook Autotagger Online</title>
</head>
<body>
<h3>Newbook Autotagger Online Interface</h3>
<p>Submit a SDTF file (svoboda diaries transcription format);
we'll run the autotagger and show you to the result.</p>
<form action="autotagger.cgi" method="post" 
      enctype="multipart/form-data">
 <input type="submit" name=""  value="Upload transcription file"/>
 <input type="file" name="sdtf" /></p>
 </form>
 </body>
</html>
"""

## be sure to use UTF buffer for stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

# Get the cookie.  If there's not one, make one.
http_cookie = os.getenv('HTTP_COOKIE')
browser_cookie = False
cookie = ''
if http_cookie:
  for c in http_cookie.split(';'):
    (name, value) = c.split('=', 1)
    if name == 'session' and len(value) == 4 and value.isdigit():
      browser_cookie = True
      cookie = value
      break

if not cookie:
  cookie = str(randint(1000,9999))
  while os.path.exists('sessions/' + cookie):
    cookie = str(randint(1000,9999))


print(HTTP_HEADERS) 
form_data = cgi.FieldStorage() 

if 'sdtf' in form_data:
  ## run autotagger on input

  # step 1, get the lines from the form
  infilelines = str(form_data['sdtf'].value, encoding="utf-8").split('\n')

  # step 2 make a TranscriptionFile from the lines
  tf = autotagger.TranscriptionFile(infilelines)
  # check for errors
  if len(tf.errors) > 0:
    print("<h3>errors in the input, they are listed below</h3>")
    print("<pre>")
    for e in tf.errors:
      print(e)
    print("</pre>")
  else:
   # no errors, run the tagger
   div2s, marginheaders, margins_dict = autotagger.create_dom_nodes(tf)
   autotagger.organize_nodes(tf, div2s, marginheaders, margins_dict)
   print(autotagger.newdoc.toprettyxml('  ', '\n', None))
    
else:
  print(WELCOME_PAGE)
