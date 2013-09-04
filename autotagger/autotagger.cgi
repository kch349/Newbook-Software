#!/usr/bin/env python3
# autotagger web interface
# 

import cgi
import cgitb; cgitb.enable()
import autotagger
import codecs
import sys
import os
import time
import glob
from random import randint
from distutils.dir_util import remove_tree



HTTP_HEADERS = "Content-type: text/html\nSet-cookie: session=%(cookie)s"
SUCCESS_PAGE = """
<html>
<head><title>Autotagger Success!</title></head>
<body>
<h3>Your %(filetype)s is ready!</h3>

<p>Find the result <a href="%(outfile)s">here</a> 
(right click the link to save the file to your computer).</p>

<h4>other options (coming soon):</h4>
<ul>
  <li>Validate: check that you're TEI-XML output is valid</li>
  <li>Apply diary.xslt and get an html output</li>
  <li>Try again with another transcription format file 
   <form action="autotagger.cgi" method="post" enctype="multipart/form-data">
   <input type="file" name="sdtf" /><br />
   <input type="submit" value="Upload transcription file"/>
   </form>
  </li>
  <li>
  <form action="autotagger.cgi" method="post" enctype=multipart/form-data">
  <input type="hidden" name="tei" value="on"/>
  Process your TEI-XML to generate an HTML file: <input type="submit" value="Go!"/></form></li>
</ul>
</body>
</html>"""

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
Our code is open-source access our repository <a href="https://github.com/kch349/Newbook-Software">here</a>.
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

# make the sessions directory if necessary
if not os.path.exists('sessions'):
  os.mkdir('sessions')

# look for any sessions older than 24 hours and delete them
now = time.time()
sessions = glob.glob('sessions/*')
for s in sessions:
  if now - os.path.getmtime(s) > 86400:
    remove_tree(s)

# figure out the path to the current session's directory, creating it
# if necessary
session_path = 'sessions/' + cookie
if cookie and not os.path.exists(session_path):
  os.mkdir(session_path)
  # create a blank output file
  open(os.path.join(session_path, 'output.xml'), 'w').close()

print(HTTP_HEADERS % {'cookie':cookie }) 
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
    print("""
<form action="autotagger.cgi" method="post" 
      enctype="multipart/form-data">
 <input type="submit" name=""  value="Upload another transcription file"/>
 <input type="file" name="sdtf" /></p>
</form>""")
         
    
    print("<pre>")
    for e in tf.errors:
      print(e)
    print("</pre>")
  else:
   # no errors, run the tagger
    document = autotagger.setup_DOM()
    div2s, marginheaders, margins_dict = autotagger.create_dom_nodes(document, tf)
    autotagger.organize_nodes(document, tf, div2s, marginheaders, margins_dict)
    try:
      outfile = open(session_path+"/output.xml", "w",encoding="utf-8")
    except:
      print("error getting the outfile for writing")

    document.writexml(outfile, addindent="  ",newl="\n")
    print(SUCCESS_PAGE % {'filetype': "TEI-XML", 'outfile': session_path+"/output.xml"})

elif 'tei' in form_data: 
  import xslt
  r = xslt.tei2html(session_path+"/output.xml",session_path+"/output.html")
  if r != 0:
    print("<p>xsltproc returned nonzero</p>")
  else:
    print(SUCCESS_PAGE % {'filetype': "HTML", 'outfile': session_path+"/output.html"})

else:
  print(WELCOME_PAGE)
