#!/usr/bin/env python3
#
# python version of
# svoboda autotagger program 
# 
# authors:
## joshua crowgey
## rachel elle brown
## victoria wellington
## kelsie haakenson
## justin yoon
## ... (add your names as you edit this file)

import sys
import re
from xml.dom.minidom import *

## some regexes that we need
PAGE_RE = re.compile('^Page\s+(\d+)')
DIVLINE_RE = re.compile('\s*DivLine:?\s*(.*)$', re.IGNORECASE)
MARGINLINE_RE = re.compile('\s*Line\s+(\d+):?\s*(.*)$')
PARA_RE = re.compile('^\s+(\S+)')
STAR_RE = re.compile('^\s*\*(.*)$')
MARGINS_RE = re.compile('\s*Margins?:?', re.IGNORECASE)
#new regexes looking for "Text:" or the "Line #:" indicating trip headings in body text
TEXT_RE = re.compile('\s*Text:?') #\s*\n^\s*Line\s+(\d+):?\s*(.*)$')
TEXTLINE_RE = re.compile('\s*Line\s+(\d+):?\s*(.*)$')

AMP_RE = re.compile('\&')

#regexes for incorrect formatting (e.g. Line #, #, #:)
MARGINLINELIST_RE = re.compile('\s*Line\s+(\d+),')
MARGINLINERANGE_RE = re.compile('\s*Line\s+(\d+)-') 
PAGENOTES_RE = re.compile('^Pages?\s+(\d+)\s*-')
PAGETABBED_RE = re.compile('^\s+Page\s+(\d+)')


impl = getDOMImplementation()
#doctype = <!DOCTYPE TEI PUBLIC "-//OTAP//DTD TEI Transitional//EN" "http://www.tei-c.org/release/xml/tei/custom/schema/dtd/teilite.dtd">

doctype = impl.createDocumentType('TEI',None,'http://www.tei-c.org/release/xml/tei/custom/schema/dtd/teilite.dtd')

# def createDocument(self, namespaceURI, qualifiedName, doctype):
newdoc = impl.createDocument(None, "TEI", doctype)
document = newdoc.documentElement
newdoc.appendChild(document)
header = newdoc.createElement('teiHeader')
header.appendChild(newdoc.createComment('put real TEI header here'))
document.appendChild(header)
text = newdoc.createElement('text')
document.appendChild(text)

#front = newdoc.createElement('front')
#text.appendChild(front)
#back = newdoc.createElement('back')
#text.appendChild(back)
body = newdoc.createElement('body')
text.appendChild(body)
errors_found = False
	
class TranscriptionFile:
  """class to parse and hold a series of TranscriptionPage objects"""

  pages = []

  def __init__(self, lines):
    self.parse_lines(lines)

  def parse_lines(self, lines):
    """method to parse the lines from the transcription file into
       a series of Transcription Page objects"""
    p = [] 
    n = -1
    while len(lines) > 0:
      m1 = PAGE_RE.match(lines[0])
     # m2 = PAGENOTES_RE.match(lines[0])
     # m3 = PAGETABBED_RE.match(lines[0])
      if m1:
        # m.group(0) should be the entire matching string
        # m.group(1) should be the page number
      #  if m2:
       #   error_protocol(m2.group(1), -1, lines[0], 5)
        # if n==-1, we're on the first page, so keep going
        # if n is already defined, we've found a new page, so
        #    process the old one
        if n > -1:
          self.pages.append(TranscriptionPage(str(n),p))
          p = []
          lines.pop(0)
          n = int(m1.group(1))
        else:
          n = int(m1.group(1))
          lines.pop(0)
     # elif m3:
      #  error_protocol(m3.group(1), -1, lines[0], 5)
       # self.pages.append(TranscriptionPage(str(n), p))
       # p = []
       # n = int(m3.group(1))
       # lines.pop(0)
      else:
        p.append(lines[0])
        lines.pop(0)
    

 
class TranscriptionPage:
  """class to hold a transcription page in a nice object
     it has a 'number', a 'header', and a 'body'

     the number should be a positive integer (or zero?, maybe?)
     the header and body are just lists of lines"""

  num = -1
  head = [] 
  body = []

  def __init__(self, num, lines):

    # sys.stderr.write("process transcription page ... ")
    self.num = num
    self.parse_lines(lines)

    # check

    # print("[done]\npage info:",file=sys.stderr)
    # print("number: "+self.num,file=sys.stderr)
    # print("header: \n"+str(self.head),file=sys.stderr)
    # print("body: \n"+str(self.body)+"\n", file=sys.stderr)
  

  def parse_lines(self, lines):
    """header is all lines up to the first empty one, rest is body"""
    h = []
    b = []
    switch = False #false means we're still in head
	               #true means we've switched to body
					  
    length = len(lines)
    text = False #true if previous line was Text:
    multi_headers = False #true if multiple "Lines" are allowed	
    for i in range(0, length): 
      m1 = MARGINS_RE.match(lines[i])
      m2 = DIVLINE_RE.match(lines[i])
      m3 = MARGINLINE_RE.match(lines[i])
      m5 = MARGINLINELIST_RE.match(lines[i])
      m6 = MARGINLINERANGE_RE.match(lines[i])
      if m5 or m6:
        error_protocol(self.num, i, lines[i], 4)
      elif not switch:
        if m1 or m2 or m3:
          h.append(lines[i])
        elif lines[i].strip() == "":
          switch = True		
        else:	
          error_protocol(self.num, i, lines[i], 1)
      else:
        if text:
          if m3:
            b.append(lines[i])
            multi_headers = True
          else:
            error_protocol(self.num, i, lines[i], 3)
          text = False
        else:
          m4 = TEXT_RE.match(lines[i])
          if m4:
            text = True
            b.append(lines[i])
          elif multi_headers and m3:
            b.append(lines[i])
          elif m1 or m2 or m3:
            error_protocol(self.num, i, lines[i], 2)
          else:		  
            b.append(lines[i])
            multi_headers = False
    self.head = h
    self.body = b	

def error_protocol(page_num, line_num, line, error_code):
  """sets errors_found variable to True and prints an error message."""
	
  global errors_found
  errors_found = True
  print_errors(page_num, line_num, line, error_code)
	
def print_errors(page_num, line_num, line, error_code):
  """prints an error message. Contains the line and page number, the faulty line,
  and what the error is."""
	
  print("An error was found on page " + str(page_num) +
	", line " +  str(line_num + 1) + ":", 
	file=sys.stderr)
  print("	" + line.strip(), file=sys.stderr)
  if error_code == 1:
    print("Error with head section. Please add either \"Line #\" or \"DivLine\"" +
     	 " to the indicated line.\nPlease make sure to format these exactly as shown.\n" +
		 "If this line belongs in the body, please remember to put a space before it.\n",
		 file=sys.stderr) 
  elif error_code == 2:
    print("This line belongs in the head. If you meant for this to be in the head," +
         " there may be an issue with the spacing.\nMake sure there are no spaces between" +
		  " the lines \"Page #:\" and \"Margin:\" and that you don't use double spacing.\n" + 
		  "If this is a diary entry header, make sure to use \"*\" " +
		  "rather than \"DivLine\".\nIf this is a journey header, add the line \"Text:\" before it.\n"
		  , file=sys.stderr)
  elif error_code == 3:
    print("This line should be a journey header. If it is, please make sure to begin " +
         "it with \"Line #\". If not, please put in a journey header before this line.",
    	 file=sys.stderr)
  elif error_code == 4:
    print("Lines cannot be formatted like \"Line #, #, #:\" or \"Lines #-#\" or any similar " +
         "format.\nEach part of the line must get its own line and must begin with \"Line #:\".\n",
         file=sys.stderr)	
  elif error_code == 5:
    print("This line must be formatted \"Page #\". No additional formatting is allowed.\n", file=sys.stderr)  
		 
def create_div2(n,part,content):
  div2 = newdoc.createElement('div2')
  div2.setAttribute('type','diaryentry')
  div2.setAttribute('n',n)
  div2.setAttribute('part', part)
  
  head = newdoc.createElement('head')
  div2.appendChild(head)
  head.setAttribute('type','diaryentry')

  text = newdoc.createTextNode(content)
  head.appendChild(text)
  return div2

def create_p(current_prose, first_line=None, fresh=False):
  '''method to create a paragraph, needs the list of paragraphs
     possibly also receive a first line (and it's linenum in a list of len 2).
     fresh tells us whether to empty the list before we start'''
  if fresh: current_prose = []
  current_prose.append(newdoc.createElement('p')) 
  if first_line != None:
    lb = newdoc.createElement('lb')
    lb.setAttribute('n',str(first_line[1]))
    current_prose[-1].appendChild(newdoc.createTextNode(first_line[0])) 
    current_prose[-1].appendChild(lb) 
  return current_prose 

       
def create_dom_nodes(tf):
  """function that sets up in a DOM form with the nodes: Document, header and body, 
  header type divlines and trip titles, margin notes and text"""

  div1s = [] # contains all trip div headers
  div2s = [] # contains all diary div headers
  marginheaders = []# triples: [content,pagenum,linenum]
  #div1 = newdoc.createElement('div1')
  #div1s.append(div1)
  
  div_count = 0
  marginline_count = 0
  for page in tf.pages:	
    for l in page.head:
       # divLine: "..." are 'diaryentry' headers
       # Line: "..." are 'margin_note' headers
      m = MARGINS_RE.match(l)
      if m:
        continue 
      
      part="N" # what's part="N"? I though these values were "I" and "F"
      if len(div2s)==0:
        ## create first div2
        div2s.append(create_div2(str(div_count),part,"First diary entry, no title given in text."))
        div_count += 1

      m = DIVLINE_RE.match(l)
      if m:
        # matched a Divline, create a new div2
        part="N" # what's part="N"? I though these values were "I" and "F"
        div2s.append(create_div2(str(div_count),part,m.group(1)))
        print("created Div2, page " + str(page.num), file=sys.stderr)
        div_count += 1
        		
      else:
        m = MARGINLINE_RE.match(l)
        if m:
            head = newdoc.createElement('head')
            marginheaders.append([head, page.num, m.group(1)])
            head.setAttribute('type','marginnote')

            xml_id = newdoc.createAttribute("xml:id")
            xml_id.nodeValue = "p" + page.num + '-' + m.group(1)
            head.setAttributeNode(xml_id)
            text = newdoc.createTextNode(m.group(2))
            head.appendChild(text)

    # now looping through page body to find div1s, which we may want to figure out how to 
    # do in the organize_nodes method later so as not to loop through the file as much.                
    div1_count = 0
    previous_text = False
    current_head = None
    text_found = False
    for l in page.body:
    # need line number stored in an attribute??
      #previous_text = False
      #current_head = None
      #text_found = False
      #div1_exists = False
      #untitled_div1 = False
      
      #if "Text:" matched and if "Line #:" is found right after "Text:", or it  
      #is the first line of the entire file, create a div 1 and add it to the list div1s 
      m = TEXT_RE.match(l)
      if m:
        text_found = True
        continue
      m = TEXTLINE_RE.match(l) 
      if (m and text_found) or len(div1s) == 0:
        #print("text line found" + page.num,file=sys.stderr)
        if not previous_text: #and div1_exists:
          div1_count += 1 
          #div1_exists = True
          div1 = newdoc.createElement('div1')
          div1s.append(div1)
          #print("created div1 and appended to the list", file=sys.stderr)
          div1.setAttribute('type','journey')
          div1.setAttribute('n',str(div1_count))
          head = newdoc.createElement('head')
          div1.appendChild(head)
          head.setAttribute('type','journey')
          current_head = head
          previous_text = True
          div1_count += 1 
          
          if len(div2s) >= 2:
            next_div2 = div2s[div_count - 1].cloneNode(True)
            print("created final node, page " + str(page.num), file=sys.stderr)
            next_div2.setAttribute('n', str(div_count))
            div2s.append(next_div2)
            div_count += 1
        #if it is the first line in the file, just create a generic and arbitrary div1
        #to hold diary entries until the first real div1 trip heading is found.  
        if not text_found:
          #print("initial trip",file=sys.stderr)
          text = newdoc.createTextNode("First Journey in Diary; No Journey Title")
        #if it actually is a trip heading, print the text as the header (and added in the
        #line number here just in case, since I don't know if that is important or not
        else:
          text = newdoc.createTextNode("Line " + m.group(1) + ': ' + m.group(2))
        current_head.appendChild(text)
        
        #if div1text_count > 0:
         # lb = newdoc.createElement('lb')
         # current_head.appendChild(lb)
        #text = newdoc.createTextNode(m.group(2))
        #current_head.appendChild(text)
        #div1text_count += 1
    
      else:
        #text line for trip header isn't matched, variables set accordingly.
        previous_text = False
        div1text_count = 0 
        div1_exists = False 
        text_found = False
      
  #print(div2headers, marginheaders)
  return div1s, div2s, marginheaders
   
def organize_nodes(tf, div1s, div2s, marginheaders):
  
  # this will be a list of paragraph nodes
  current_prose = []
  current_prose = create_p(current_prose) 

  new_trip = False
  current_div1 = 0
  for page in tf.pages:
    linecount = -1  
    for l in page.body:
      linecount += 1
      if linecount == 0:
        div1s[0].appendChild(div2s[0])
        
      if len(marginheaders) > 0:
        current_lineheader = marginheaders[0]
        if linecount <= int(current_lineheader[2]) and page.num == current_lineheader[1]:
          div2s[0].appendChild(current_lineheader[0])
          #marginheaders.pop(0)
          marginheaders.remove(current_lineheader)
      #else:
        #print("ran out of marginheaders",file=sys.stderr)
      
      #organizing div1s
      m = TEXT_RE.match(l)
      if m:
        #print("Next trip heading", file=sys.stderr)
        div2s[0].childNodes.extend(current_prose)
        # create a new next paragaraph
        current_prose = create_p(current_prose, fresh=True) 
        div1s[0].appendChild(div2s[0])
        #div1s[current_div1].appendChild(div2s[0])
        #if current_div1 < (len(div1s) - 1):
          #current_div1 += 1
        body.appendChild(div1s[0])
        #print("appended div1", file=sys.stderr)
        if len(div1s) > 1:
          div1s.pop(0)  
        new_trip = True
       
        #div2s[0].setAttribute('part', 'I')
        
        #creates a cloned div2 without all its nodes to serve as the medial or final part 
        #that div2 if need be. It is inserted into the list. 
        #next_div2 = div2s[0].cloneNode(False)
        #print("created final node, page " + str(page.num) + "line " + str(linecount), file=sys.stderr)
        #next_div2.setAttribute('part', 'M')
        #removes last div, and puts the new medial/final div2 in the list
        if len(div2s) > 1:
          headCheck = div2s[0].getElementsByTagName('head')
          #print("popped div2 #" + div2s[0].getAttribute('n'), file=sys.stderr)
          div2s.pop(0)
        #div2s.insert(0, next_div2)
        continue
      m = TEXTLINE_RE.match(l)
      if m:
        new_trip = True
        continue
       
      new_trip = False
      
      #organizes div2s. This section is the one with the most bugs I think, mainly the part
      #attribute issue
      m = STAR_RE.match(l) 
      if m: 
        print("asterisk, page " + str(page.num) + "line " + str(linecount), file=sys.stderr)
        #try: 
         # if linecount < int(current_lineheader[2]):
          #  continue
        #except: 
    	 #   """problem in screening each line for margin headers"""

        #####if div2 is empty (no content), strip it. 
        
        
        #tries to delete the extra medial/final node created if it isn't necessary, as is true if the 
        #new diary entry occurs at the beginning of a new journey.
       # if new_trip:
    	   # print("deleted extra final node, page " + str(page.num) + "line " + str(linecount), file=sys.stderr)
    	  #  div2s.pop(0)  
        
        #appends children to div2 and that div2 to div1, then moves to the next div2
        div2s[0].childNodes.extend(current_prose)
        div1s[0].appendChild(div2s[0])
        #div1s[current_div1].appendChild(div2s[0])

        # delete the star and add this line to the current paragraph of current prose
        current_prose = create_p(current_prose,[re.sub('\s+\*','',l),linecount],fresh=True)
        if len(div2s) > 1:
          headCheck = div2s[0].getElementsByTagName('head')
          #print("popped div2 #" + div2s[0].getAttribute('n'), file=sys.stderr)
          #for h in headCheck:
           # print(h.toxml(None), file=sys.stderr)
          div2s.pop(0)
          #print("moved to next div2, page " + str(page.num) + "line " + str(linecount), file=sys.stderr)
        
        #if len(div2headers) > 0:
          #current_div2 = div2s[0]
        #put in stuff for trip headings
      else:
        m = PARA_RE.match(l)
        if m:
          ## found a paragraph starting line of text
          # start a new paragraph
          current_prose = create_p(current_prose,[l,linecount])
        else:
          ## found a vanilla line of text
          lb = newdoc.createElement('lb')
          lb.setAttribute('n',str(linecount))
          current_prose[-1].appendChild(newdoc.createTextNode(l))
          current_prose[-1].appendChild(lb)
    #maybe add in something that says to delete the last line break before creating 
    #the next page to fix that bug?
    pb = newdoc.createElement('pb')
    pb.setAttribute('n',str(page.num))
    current_prose[-1].appendChild(pb)
      # print([c.toxml() for c in current_prose],file=sys.stderr)
  # done looping, everything organized so stick the nodes onto the document
  div2s[0].childNodes.extend(current_prose)
  #div1s[0].childNodes.extend(div2s) 
  body.childNodes.extend(div1s)

if __name__ in "__main__":
  # accept svoboda transcription format file
  # on stdin

  try:
    filename = sys.argv[1]
    infilelines = open(filename, 'r').readlines()
  except:
    infilelines = sys.stdin.readlines()
  
  # to keep things clean, and check for errors in
  # the input,
  # before we start, parse these lines
  # into a series of 'page objects'  
 
  tf = TranscriptionFile(infilelines)

  print("found "+str(len(tf.pages))+" transcription pages", file=sys.stderr)
  #for p in tf.pages:
  #   print(p.num,p.head,[l for l in p.body], file=sys.stderr)
  # print("---------", file=sys.stderr)
 
  #to_xml_dom(tf)
  div1s, div2s, marginheaders = create_dom_nodes(tf)

  ## okay, this is too verbose for now :)
  #for d in div1s:
   # print(d.toxml(),file=sys.stderr)
    #print("\n\n",file=sys.stderr)
   
  #for d in div2s:
    #print(d.toxml(),file=sys.stderr)
    #print("\n\n",file=sys.stderr)
  # 
  # for d in marginheaders:
  #   print(d[0].toxml(),file=sys.stderr)
  #   print("\n\n",file=sys.stderr)
  
  if errors_found:
    print("Errors found. Please check error log and try again later.")
  else:	
    #to_xml_dom(tf)
    div1s, div2s, marginheaders = create_dom_nodes(tf)

    ## okay, this is too verbose for now :)
    #for d in div1s:
      #print(d.toxml(),file=sys.stderr)
      #print("\n\n",file=sys.stderr)
    # 
    # for d in div2s:
    #   print(d.toxml(),file=sys.stderr)
    #   print("\n\n",file=sys.stderr)
    # 
    # for d in marginheaders:
    #   print(d[0].toxml(),file=sys.stderr)
    #   print("\n\n",file=sys.stderr)
  
    organize_nodes(tf, div1s, div2s, marginheaders)
    print(document.toprettyxml('\t', '\n', None))

