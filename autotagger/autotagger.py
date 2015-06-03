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

# Currently supported transcription formats:
# Version 0.0
# Version 1.0

# The autotagger converts plain text documents written the Svoboda Diaries Transcription
# Format (STDF) into valid TEI-XML documents by completing rudimentary structural
# tagging. XML tagging supports the following structural elements:
#			- Sections
#			- Subsections
# 		- Pages
# 		- Marginal notes
#			- Line breaks

# Is backwards compatible with earlier versions of the STDF format (listed above). 
# Encoding is in UTF-8. Any text in non-latin alphabets (such as Arabic) is left untouched
# by this program, and is only placed in its proper location within the text.

# To run this program in the command line from the same directory as the autotagger, enter:
#    cat <transcriptionFile.txt> | ./autotagger.py 1>err.txt 0>out.xml

#### ADD INFO ON CONFIGURATION USAGE ###
# TEI Header information either is filled with default placeholders, or with custom 
# metadata provided through a separate config.json file supplied by the user.


# The autotagger can also be accessed online at ________. This interface further includes
# conversions to HTML and LaTeX.


import sys
import re
import logging
import argparse
from config import AutotaggerConfiguration
from xml.dom.minidom import *


## input document and transcription format data
CURRENT_VERSION = 1
version = -1
original_version = -1

## overall regexes
PAGE_RE = re.compile('^Page\s+(\d+)')
PARA_RE = re.compile('^\s+(\S+)')
EMPTYLINE_RE = re.compile('^\s*$')
AMP_RE = re.compile('\&')
VERSION_RE = re.compile('^Version\s*(\d+.*)')

## regexes for incorrect formatting (e.g. Line #, #, #:)
LINELIST_RE = re.compile('\s*Line\s+(\d+),') ##change to line list (for journeys too)
LINERANGE_RE = re.compile('\s*Line\s+(\d+)-')
PAGENOTES_RE = re.compile('^Pages?\s+(\d+)\s*-')
PAGETABBED_RE = re.compile('^\s+Page\s+(\d+)')
DIVLINENUMBER_RE = re.compile('\s*DivLine\s+(\d+):?\s*(.*)$', re.IGNORECASE)

PAGECOLON_RE = re.compile('^Page:\s+(\d+)')
PAGESPLURAL_RE = re.compile('^Pages\s+(\d+)')


## version 0 regexes
DIVLINE_RE = re.compile('\s*DivLine:?\s*(.*)$', re.IGNORECASE)
STAR_RE = re.compile('^\s*\*(.*)$')
MARGINS_RE = re.compile('\s*Margins?:?', re.IGNORECASE)
TEXT_RE = re.compile('\s*Text:?')
LINE_RE = re.compile('\s*Line\s+(\d+):?\s*(.*)$')


## version 1 regexes
V1_MARGINLINELIST_RE = re.compile('^\s*Margin\s+Line\s+(\d+),')
V1_MARGINLINERANGE_RE = re.compile('^\s*Margin\s+Line\s+(\d+)-')
##include divline number##
NOTES_RE = re.compile('^\s*Notes:?', re.IGNORECASE)
MARGINNOTE_RE = re.compile('^\s*Margin\s+Line\s+(\d+):?\s*(.*)$')
FOOTNOTE_RE = re.compile('^\s*Footnote:?\s*(.*)$')
SECTION_RE = re.compile('^\s*Section:?\s*(.*)$')
SUBSECTION_RE = re.compile('^\s*Subsection:?\s*(.*)$')
SUBSECTIONNUMBER_RE = re.compile('^\s*Subsection:?\s*\d+:(.*)$') #take out once problem is fixed? 


 
#Sets version for document so it is accessible throughout program. If specified,
#will also set the original version as passed in (only done once at the beginning)
def set_version(value, original=False):
  if original:
    global original_version
    original_version = value
  global version
  version = value

#Creates responsibility statement in TEI Header
#(To Configure)
def create_respSt(document, cfg):
  resp_statement = document.createElement('respStmt')
  resp = document.createElement('resp')
  resp_statement.appendChild(resp)
  resp.appendChild(document.createTextNode(cfg.get('RESP_PROJECT')))
  name = document.createElement('name')
  resp_statement.appendChild(name)
  name.appendChild(document.createTextNode(cfg.get('PROJECT_LEAD')))
  return resp_statement

#Creates generic TEI Header. Will allow for configuration later.
#(To Configure)
def create_teiHeader(document,cfg):
  header = document.createElement('teiHeader')
  fileDesc = document.createElement('fileDesc')
  header.appendChild(fileDesc)
  title_statement = document.createElement('titleStmt')
  fileDesc.appendChild(title_statement)

  title = document.createElement('title')
  title_statement.appendChild(title)
  title.appendChild(document.createTextNode(cfg.get('TITLE')))

  author =  document.createElement('author')
  title_statement.appendChild(author)
  author.appendChild(document.createTextNode(cfg.get('AUTHOR')))

  title_statement.appendChild(create_respSt(document,cfg))

  pubSt = document.createElement('publicationStmt')
  fileDesc.appendChild(pubSt)
  distributor = document.createElement('distributor')
  pubSt.appendChild(distributor)
  distributor.appendChild(document.createTextNode(cfg.get('DISTRIBUTOR')))

  address = document.createElement('address')
  pubSt.appendChild(address)
  addrLine = document.createElement('addrLine')
  address.appendChild(addrLine)

  idno = document.createElement('idno')
  pubSt.appendChild(idno)
  idno.setAttribute('type', cfg.get('ID_TYPE'))
  idno.appendChild(document.createTextNode(cfg.get('ID_VALUE')))

  availability = document.createElement('availability')
  pubSt.appendChild(availability)
  p = document.createElement('p')
  availability.appendChild(p)
  p.appendChild(document.createTextNode(cfg.get('COPYRIGHT')))

  date = document.createElement('date')
  pubSt.appendChild(date)
  #why do we have a "when type" when there is already a text node containing that information?
  date.setAttribute('when', 'Insert Date Here')
  date.appendChild(document.createTextNode(cfg.get('DATE')))

  sourceDesc = document.createElement('sourceDesc')
  fileDesc.appendChild(sourceDesc)
  bibl = document.createElement('bibl')
  sourceDesc.appendChild(bibl)
  bibl.appendChild(document.createTextNode(cfg.get('BIBL_INFO')))

  encodingDesc = document.createElement('encodingDesc')
  header.appendChild(encodingDesc)
  projectDesc = document.createElement('projectDesc')
  encodingDesc.appendChild(projectDesc)
  p2 = document.createElement('p')
  projectDesc.appendChild(p2)
  p2.appendChild(document.createTextNode(cfg.get('PROJECT_DESC')))

  revisionDesc = document.createElement('revisionDesc')
  header.appendChild(revisionDesc)

  listNode = document.createElement('list')
  revisionDesc.appendChild(listNode)

  item = document.createElement('item')
  listNode.appendChild(item)

  date = document.createElement('date')
  item.appendChild(date)
  #Same question about "when" attribute as above.
  date.setAttribute('when', cfg.get('DATE_LAST_UPDATED'))     #Will be slightly different from existing copy
  date.appendChild(document.createTextNode(cfg.get('DATE_LAST_UPDATED')))
  item.appendChild(document.createTextNode('Last checked'))
  return header

#Sets up xml_minidom document with (front), body, and (back) material
def setup_DOM(cfg):
  impl = getDOMImplementation()
  doctype = impl.createDocumentType('TEI',None,'http://www.tei-c.org/release/xml/tei/custom/schema/dtd/tei_all.dtd')

  newdoc = impl.createDocument(None, "TEI", doctype)
  document = newdoc.documentElement
  newdoc.appendChild(document)
  teiHeader = create_teiHeader(newdoc,cfg)
  document.appendChild(teiHeader)

  text = newdoc.createElement('text')
  document.appendChild(text)

  #Commented out code for processing front and back material if ever necessary
  #front = newdoc.createElement('front')
  #text.appendChild(front)
  
  body = newdoc.createElement('body')
  text.appendChild(body)
  
  #back = newdoc.createElement('back')
  #text.appendChild(back)
  return newdoc

class TranscriptionFile:
  """class to parse and hold a series of TranscriptionPage objects"""

  pages = []
  errors = []

  #Constructs a TranscriptionFile. Determines document version and updates it to the
  #current version. Processes document into TranscriptionFile
  def __init__(self, lines):
    m4 = VERSION_RE.match(lines[0])
    if m4:
      set_version(int(m4.group(1)), True)
      
      if version > CURRENT_VERSION:
        set_version(CURRENT_VERSION) #should avoid passing constant?
        logging.warning("""Specified version is greater than the current version. Possibly
                           typo or an update to the autotagger is necessary before usage""")
    elif (version == -1):
      set_version(0, True)  
    
    
    #check for errors in lines, to ensure proper format.
    #
    
    while version < CURRENT_VERSION:
      lines, new_errors = self.uprev(lines)
      if len(new_errors) > 0:
        self.errors.append(new_errors)
        #print("Errors found. Please check error log and try again later.")
        #for e in self.errors:
         # print(e,file=sys.stderr)
     # else:
    #if len(self.errors) == 0:
    self.parse_lines(lines)
     
  def parse_lines(self, lines):
    """method to parse the lines from the transcription file into
       a series of Transcription Page objects"""
    p = []
    n = -1
    while len(lines) > 0:
      m1 = PAGE_RE.match(lines[0])
      m2 = PAGENOTES_RE.match(lines[0])
      m3 = PAGETABBED_RE.match(lines[0])
      
      #if m2:
        #self.errors.append(errors(m2.group(1), -1, lines[0], CURRENT_VERSION, 5))
      if m1:
        # m.group(0) should be the entire matching string
        # m.group(1) should be the page number
        # if n==-1, we're on the first page, so keep going
        # if n is already defined, we've found a new page, so
        #    process the old one
        if n > -1:
          self.pages.append(TranscriptionPage(str(n), p))
          p = []
          lines.pop(0)
          n = int(m1.group(1))
        else:
          n = int(m1.group(1))
          lines.pop(0)
      elif m3:
        #self.errors.append(errors(m3.group(1), -1, lines[0], CURRENT_VERSION, 5))
        self.pages.append(TranscriptionPage(str(n), p))
        p = []
        n = int(m3.group(1))
        lines.pop(0)
      else:
        p.append(lines[0])
        lines.pop(0)
        

   # try:
    tp = TranscriptionPage(str(n), p)
    if len(tp.errors) > 0:
      self.errors.extend(tp.errors)
    self.pages.append(tp)
    #except:
     # """Error with page creation. There is not another page to append."""
  
  #Controls the update of document to current version.   
  def uprev(self, lines):
    uprev_lines = []
    uprev_errors = []
    logging.debug("Entered uprev.")
    if version == 0:
      uprev_lines, uprev_errors = self.version0to1(lines)
      set_version(1)
      
    #Uncomment line below to print out the file in the most current transcription format
    #to stderr
    #self.print(uprev_lines)
    return uprev_lines, uprev_errors #or should this be a different return statement each time?

  #Updates version 0 documents to version 1
  def version0to1(self, lines):
    logging.debug("entered version0to1")
    version1_lines = []
    v1_errors = []
    
    current_page = -1  
    temp_div_headers = [] 
    length = len(lines)
    text = False #true if previous line was Text:
    divlines = 0
    empty = False #true if previous line in body was empty
    double_spacing = 0 #number of double spaced lines found in body
    double_spacing_found = False #true if double spacing found

    for i in range(0, length):
       #Handle Text and DivLine elements only present in version 0 transcription files
      m1 = TEXT_RE.match(lines[i])
      m2 = DIVLINE_RE.match(lines[i])
      m3 = DIVLINENUMBER_RE.match(lines[i])
      
      if m1 or m2 or m3:
        if m2 or m3:
          if m3:
            #self.errors.append(errors(str(current_page), i, lines[i], original_version, 6))
            logging.warning(" There may be an incorrectly formatted DivLine on page " +
                            str(current_page) + ". Make sure the line number is not included.")
            
          temp_div_headers.append(m2.group(1))
          divlines += 1
        else:
          text = True
      
      #Process rest, updating tf syntax where necessary and recording any errors.    
      else:
        m4 = PAGE_RE.match(lines[i])
        m5 = PAGENOTES_RE.match(lines[i])
        m6 = PAGETABBED_RE.match(lines[i])
        m7 = MARGINS_RE.match(lines[i])
        m8 = STAR_RE.match(lines[i])
        m9 = LINE_RE.match(lines[i])
        
        #Keep track of pages so as to allow for error reporting
        if m4 or m5 or m6:
          if current_page == -1:
            current_page = 1
          else:
            current_page += 1
          logging.debug("Page number " + str(current_page))  
      
        elif m7:
          lines[i] = '\tNotes:'
        elif m8:
          divlines -= 1
          #print(temp_div_headers[0], file=sys.stderr)
          if len(temp_div_headers) >= 1:
            version1_lines.append('\tSubsection: ' + temp_div_headers[0].rstrip())
            temp_div_headers.pop(0)
          else: 
            v1_errors.append(incorrect_stars_error(str(current_page))) 
          lines[i] = re.sub('\*', '', lines[i]) #removes *, need to remove that later in code since not here
          #appending at end could pose a problem adding multiple lines.
        elif text and m9:
          lines[i] = '\tSection: ' + re.sub('\s*Line:?\s+(\d+):?\s*', '', lines[i].rstrip())
          #multi_headers = True   
        else:
          text = False
          if m9:
            lines[i] = re.sub('^\s*', '\tMargin ', lines[i])
        version1_lines.append(lines[i].rstrip())          
    if divlines != 0:
      v1_errors.append(incorrect_stars_error(str(current_page)))  
    return version1_lines, v1_errors

  #Prints TranscriptionFile in current transcription file format, noting the version number
  def print(self, lines):
    print('Version ' + str(CURRENT_VERSION), file=sys.stderr)
    for l in lines:
      print(l, file=sys.stderr)
  
  #Prints a page after processing for debugging purposes, including Version number at
  #first page, Page and number, and lines in head and body.
  def printAfter(self):
    if self.num == '1': # what if different starting number? Account for that with a variable? 
      print('Version ' + str(CURRENT_VERSION), file=sys.stderr)
    print('Page ' + self.num + ':', file=sys.stderr)
    for l in self.head:
      print(l, file=sys.stderr)
    print('', file=sys.stderr)
    for l in self.body:
      print(l, file=sys.stderr)            
          

class TranscriptionPage:
  """class to hold a transcription page in a nice object
     it has a 'number', a 'header', and a 'body'

     the number should be a positive integer (or zero?, maybe?)
     the header and body are just lists of lines"""

  num = -1
  head = []
  body = []
  errors = []

  #Constructs a new TranscriptionPage
  def __init__(self, num, lines):
    self.num = num
    self.parse_lines(lines)
    logging.debug("[done]\npage info:")
    logging.debug("number: " + self.num)
    logging.debug("header: \n" + str(self.head))
    logging.debug("body: \n" + str(self.body) + "\n")

  #Processes lines of input into a TranscriptionPage in proper format 
  def parse_lines(self, lines):
    """header is all lines up to the first empty one, rest is body"""
    
    h = []
    b = []
    in_body = False #false if still in head
    length = len(lines)
    empty = False #true if previous line in body was empty
    double_spacing = 0 #number of double spaced lines found in body
    double_spacing_found = False #true if double spacing found
    linecount = 0
    for i in range(0, length):
      #Check for initial errors
      m1 = V1_MARGINLINELIST_RE.match(lines[i])
      m2 = V1_MARGINLINERANGE_RE.match(lines[i])
      m3 = VERSION_RE.match(lines[i])
      m4 = NOTES_RE.match(lines[i])
      m5 = MARGINNOTE_RE.match(lines[i])
      m6 = FOOTNOTE_RE.match(lines[i])  
      #if m1 or m2:
        #self.errors.append(errors(self.num, i, lines[i], original_version, 4))
      #process header
      if not in_body:
        logging.debug("IN HEAD") 
        if m3: #How do we make sure it is at the beginning of first page?
          continue
        elif m4 or m5 or m6:
          h.append(lines[i].rstrip())
        elif lines[i].strip() == "":
          in_body = True
        #else:
         # self.errors.append(errors(self.num, i, lines[i], original_version, 1))
      #process body
      else:
        logging.debug("IN BODY")
        #Handle double spacing
       # if double_spacing == 3 and double_spacing_found == False:
        #  logging.warning(" There may be unintentional double spacing on page " + self.num + ".") 
         # double_spacing_found = True
        #elif double_spacing < 3:
         # if lines[i].strip() == "":
          #  empty = True
          #elif empty == True:
           # double_spacing += 1
            #empty = False
          #elif empty == False:
           # double_spacing = 0    
        #if not m4:
          #self.errors.append(errors(self.num, i, lines[i], 3))
          
        #Translate main structural 
        m7 = SECTION_RE.match(lines[i])
        m8 = SUBSECTION_RE.match(lines[i])
        m9 = SUBSECTIONNUMBER_RE.match(lines[i])
        if m7 or m8 or m9:      
          #if m9:
          logging.warning(" There may be an incorrectly formatted DivLine on page " +
                             self.num + ". Make sure the line number is not included.")
          b.append(lines[i].rstrip()) #could pose a problem adding multiple lines.
        #elif m4 or m5 or m6:
          #self.errors.append(errors(self.num, i, lines[i], original_version, 2))
        else:
          b.append(lines[i].rstrip())# combine with one up 4 lines for less redundancy?
            
    self.head = h
    self.body = b
    #self.printAfter()




#Processes error with incorrect number of stars
def incorrect_stars_error(page_num):
  """Produces an error message saying there are too many or too few
  asterisks. Contains the page number."""

  return "The number of asterisks in the body does not match the number "+\
         "of DivLines in the header on page "+ page_num +"."

#Processes all other errors
def log_error(page_num, line_num, line, error_code, general=False):
  """Produces an error message. Contains the line and page number, the
  faulty line, and what the error is."""
  logging.debug("IN LOG_ERROR")
  general_errors = {1 : "Page notation error. Please be sure to indicate a new"+\
                    " page using the tag \"Page #:\". Do not add other notes to "+\
                    "to this line, give a page range, refer to more than one page, "+\
                    " or misplace the colon.\n",
                    2 : "Text included prior to the first page. Be sure to mark a "+\
                    "beginning page for your document before proceeding with the "+\
                    "transcription.\n"}
                    
  v0_errors = {1 : "Error with head section. Please add either \"Line #\" "+\
               "or \"DivLine\" to the indicated line.\n" +\
               "If this line belongs in the body, please remember to put"+\
               " an empty line before it.\n",
             2 : "Based on its formatting, this line belongs in the head. " +\
               "\t-If you meant for this to be in the head," +\
               " there may be an issue with the spacing. \n\t Make sure there "+\
               "are no spaces between the lines \"Page #:\" and \"Margin:\""+\
               " and that you don't use double spacing.\n"+\
               "\t-If this is a diary entry header, make sure to use \"*\" " +\
               "rather than \"DivLine\".\n " +\
               "\t-If this is a journey header, add the line \"Text:\" before it.\n",
             3 : "This line should be a journey header. If it is, please make "+\
               "sure to begin it with \"Line #\". If not, please put in a "+\
               "journey header before this line.",
             4 : "Lines cannot be formatted like \"Line #, #, #:\" or "+\
               "\"Lines #-#\" or any similar format.\nEach part of the"+\
               " line must get its own line and must begin with \"Line #:\".\n",
             5 : "This line must be formatted \"Page #\". No additional "+\
               "formatting is allowed.\n",
             6 : "DivLines cannot be formatted like \"Divline #: or in any similar format.\n" +\
               "This should be formatted without a line number, simply as \"Divline: <text>\"\n",
             7 : "A line marking was found out of place.\n" +\
               "\t-If this line indicates a marginal note, be sure to include this in the" +\
               " head as opposed to the body.\n" +\
               "\t-If this line indicates a section header, be sure to include the line \"Text:\"" +\
               " prior to it or prior to the list of \"Line #: \" markings of the section" +\
               " header title.\n"}
               
  v1_errors = {1 : "Error with head section. Please add \"Margin Line #\" "+\
               "to the indicated line.\n" +\
               "If this line belongs in the body, please remember to put"+\
               " a space before it.\n",
             2 : "Based on its formatting, this line belongs in the head. \n" +\
               "\t-If you meant for this to be in the head," +\
               " there may be an issue with the spacing. \n\t Make sure there "+\
               "are no spaces between the lines \"Page #:\" and \"Notes:\""+\
               " and that you don't use double spacing.\n"+\
               "\t-If this is a diary entry header, make sure to use \"Subsection:\". \n" +\
               "\t-If this is a journey header, add \"Section:\" before it.\n",
             3 : "This line should be a journey header. If it is, please make "+\
               "sure to begin it with \"Section:\". If not, please put in a "+\
               "journey header before this line.",
             4 : "Lines cannot be formatted like \"Margin Line #, #, #:\" or "+\
               "\"Margin Lines #-#\" or any similar format.\nEach part of the"+\
               " line must get its own line and must begin with \"Margin Line #:\".\n",
             5 : "This line must be formatted \"Page #\" with no additional "+\
               "formatting. \n"}


  err_str = "An error was found on page " + str(page_num) +\
            ", line " +  str(line_num + 1) + ", displayed below: \n\t\t" + line.strip() + "\n"
  if general:
    err_str += general_errors[error_code]
  elif version == 0: #version is a global variable
    err_str += v0_errors[error_code]
  elif version == 1:
    err_str += v1_errors[error_code]
  #logging.debug(err_str)
  return err_str



def verify_format(line, in_body, page_num, line_num): #, general=False):
  if version == 0: 
     return verify_v1(line, in_body, page_num, line_num) #, general)
  elif version == 1:
    return verify_v1(line, in_body, page_num, line_num) #general)
  #if result != None:
   # errors.append([result])
  
#Determine if a specified line marks a new div header or its position.
#Returns 1 if there is a new div header, -1 if a star marking 
#a div's position is found, and 0 otherwise 
#Note: used for version 0 documents only
def count_divlines(line, in_body):
  result = 0
  m1 = DIVLINE_RE.match(line)
  m2 = DIVLINENUMBER_RE.match(line)
  m3 = STAR_RE.match(line)
  if not in_body:
    if m1 or m2:
      result = 1
  else:
    if m3:
      result = -1   
  return result

def find_section_header(line, in_body):
  m1 = TEXT_RE.match(line)
  if m1 and in_body:
    return True
  return False

def verify_v0(line, in_body, page_num, line_num, text_header): #, general=False):
####################
  result = ""

  m1 = LINE_RE.match(line)
  m2 = LINELIST_RE.match(line)
  m3 = LINERANGE_RE.match(line)
  m4 = MARGINS_RE.match(line)
  
  m5 = TEXT_RE.match(line)
  m6 = DIVLINE_RE.match(line)
  m7 = DIVLINENUMBER_RE.match(line)
  m8 = STAR_RE.match(line)

##########

  m1 = MARGINLINELIST_RE.match(line)
  m2 = MARGINLINERANGE_RE.match(line)
  m3 = MARGINS_RE.match(line)
  m4 = LINE_RE.match(line)
  
  m5 = TEXT_RE.match(line)
  m6 = DIVLINE_RE.match(line)
  m7 = DIVLINENUMBER_RE.match(line)
  m8 = STAR_RE.match(line)
  m9 = LINE_RE.match(line)
  
  if m2 or m3:
    result = log_error(page_num, line_num, line, 4)
  if not in_body:
    logging.debug("IN V1 HEAD")
    
    #if m2 or m3:
      #result = log_error(page_num, line_num, line, 4)
    #if m4 or m1 or m6 or m2 or m3: #m6 = divline
     # x = 3 #remove later
    if m7:
      #result = log_error(errors(str(page_num), line_num, line, 6))
      
      
      
      
      
      
      #logging.warning(" There may be an incorrectly formatted DivLine on page " +
                      #str(current_page) + ". Make sure the line number is not included.")
    #else: #not a line from the head
    elif not (m1 or m2 or m3 or m4 or m6): # if not a line that should be in the head
      logging.debug("ERROR IN HEAD")
      result = log_error(page_num, line_num, line, 1)
      logging.debug("RESULT AFTER HEAD ERROR: " + result)
    
  else:
    logging.debug("IN V1 BODY")
    #if m5 or m8:
     # x = 5 #remove later
    #elif text_header and (m1 or m2 or m3):
     # x = 2 # remove later
    
      #multi_headers = True   
    if (m1 or m2 or m3) and not text_header:  #(all) and not text_header
      result = log_error(page_num, line_num, line, 7)
    elif m4 or m6 or m7:
      result = log_error(page_num, line_num, line, 2)
    
    #else, (if not (m5, m8, or (m1 m2 m3 with textheader) no error)
  logging.debug("VERIFY_V0 RESULT: " + result)
  return result
  #to complete

###################


  
def verify_v1(line, in_body, page_num, line_num): #, general=False): # version global, do we need general?
  result = ""
  
  m1 = V1_MARGINLINELIST_RE.match(line)
  m2 = V1_MARGINLINERANGE_RE.match(line)
  m3 = NOTES_RE.match(line)
  m4 = MARGINNOTE_RE.match(line)
  m5 = FOOTNOTE_RE.match(line)
    
  m7 = SECTION_RE.match(line)
  m8 = SUBSECTION_RE.match(line)
  m9 = SUBSECTIONNUMBER_RE.match(line)  #shouldn't need this, vestige of old format
  if not in_body: # in head
    logging.debug("IN V1 HEAD")
    if m1 or m2:
      result = log_error(page_num, line_num, line, 4)
    elif m3 or m4 or m5:
      x = 3 # REMOVE LATER
    else:
      logging.debug("ERROR IN HEAD")
      result = log_error(page_num, line_num, line, 1)
      logging.debug("RESULT AFTER HEAD ERROR: " + result)
  else: # in body
    logging.debug("IN V1 BODY") 
    #Check for other structural errors      
    if m7 or m8 or m9:      
       if m9:
         logging.warning(" There may be an incorrectly formatted DivLine on page " +
                          str(page_num) + ". Make sure the line number is not included.")
    elif m3 or m4 or m5:
      result = log_error(page_num, line_num, line, 2)
  logging.debug("VERIFY_V1 RESULT: " + result)
  return result
    #formerly else statement and continue
    
    
    
    
    
#Checks for transcription format errors in a given transcription file. Returns errors if 
#there are any, or returns null if the transcription file is well formatted.
def check_errors(lines):
  """header is all lines up to the first empty one, rest is body"""
  errors = []
  in_body = False #false if still in head
  length = len(lines)
  empty = False #true if previous line in body was empty
  double_spacing = 0 #number of double spaced lines found in body
  double_spacing_found = False #true if double spacing found
  linecount = 0
  pagecount = -1
  
  divlines = 0
  text_header = False
    
  # Check for common errors. e# indicates the match for an error.
  for i in range(0, length):
    linecount+=1
    #set version once
    if version == -1:
      version_found = VERSION_RE.match(lines[i])
      if version_found:
        set_version(int(version_found.group(1)), True)
    
      if version > CURRENT_VERSION:
        set_version(CURRENT_VERSION) #should avoid passing constant?
        logging.warning("""Specified version is greater than the current version. Possibly
                            typo or an update to the autotagger is necessary before usage""")
      elif (version == -1):
        set_version(0, True)  
      
      
      
    #check page
    version_found = VERSION_RE.match(lines[i]) # is this necessary when above? limit of scope?
    new_page = PAGE_RE.match(lines[i])
    m1 = PAGENOTES_RE.match(lines[i])
    m2 = PAGETABBED_RE.match(lines[i])
    m3 = PAGECOLON_RE.match(lines[i])
    m4 = PAGESPLURAL_RE.match(lines[i])
    if version_found:
      continue
    elif new_page or m1 or m2 or m3 or m4:
      in_body = False 
      linecount = 0 #reset linecount to start of that transcription page 
      if new_page:
        pagecount = int(new_page.group(1)) #page count issue?? see transcriptionfile
      elif m1 or m2 or m3 or m4: 
        if m1:
          pagecount = int(m1.group(1))
        elif m2:
          pagecount = int(m2.group(1))
        elif m3:
          pagecount = int(m3.group(1))
        elif m4:
          pagecount = int(m4.group(1))
        errors.append(log_error(pagecount, linecount, lines[i], 1, general=True))
    elif pagecount == -1:
      errors.append(log_error(pagecount, linecount, lines[i], 2, general=True)) #text prior error
      
      
    elif not in_body: #scan for errors in the head 
      logging.debug("IN HEAD - ERROR CHECKING") 
      if lines[i].strip() == "":
        in_body = True
      else:
        if version == 0:
          divlines += count_divlines(lines[i], in_body)
          text_header = find_section_header(lines[i], in_body)
        error_report = verify_format(lines[i], in_body, pagecount, linecount, text_header)
        if error_report != "":
          errors.append(error_report)
    else: #scan for errors in body text 
      logging.debug("IN BODY - ERROR CHECKING") 
      
      if double_spacing == 3 and double_spacing_found == False:
        logging.warning(" There may be unintentional double spacing on page " + str(pagecount) + ".") 
        double_spacing_found = True
      elif double_spacing < 3:
        if lines[i].strip() == "":
          empty = True
        elif empty == True:
          double_spacing += 1
          empty = False
        elif empty == False:
          double_spacing = 0    
          #if not m4:
            #self.errors.append(errors(self.num, i, lines[i], 3))
          
      if version == 0:
        divlines += count_divlines(lines[i], in_body)
        text_header = find_section_header(lines[i], in_body)
      error_report = verify_format(lines[i], in_body, pagecount, linecount, text_header)
      if error_report != "":
        errors.append(error_report)
    if len(errors) > 0:
      logging.debug(errors[0])
      
  if divlines != 0:
    errors.append(incorrect_stars_error(str(pagecount))) 
  logging.debug("LOOP FINISHED")
  return errors




#WHEN IS THE RETURN HEAD EVER USED?	
#Creates a div of a specified number, type (1 or 2), and if applicable, part (I, M, or F)
def create_div(document, n, div_type, part):
  """Creates div element of specified type and returns that div and its head node"""
  div = document.createElement(div_type)
  div.setAttribute('n', n)
  if part is not None:
    div.setAttribute('part', part)
  head = document.createElement('head')
  div.appendChild(head)
  return head, div

#Creates first div of given type if necessary
#def create_generic_div(document, div_count, type):
 # part = None
  #if type == 'div2':
   # part = "N"
  #div_head, div = create_div(document, str(div_count), type, part)
  #div_count +=1
  #return div, div_count

#Creates a new paragraph
def create_p(document,current_prose, cfg,first_line=None, fresh=False):
  '''method to create a paragraph, needs the list of paragraphs
     possibly also receive a first line (and it's linenum in a list of len 2).
     fresh tells us whether to empty the list before we start'''
  if fresh: current_prose = []
  current_prose.append(document.createElement('p'))
  if first_line != None:
    current_prose[-1].appendChild(document.createTextNode(first_line[0]))
    if cfg.get('LINE_BREAKS'):
      current_prose[-1].appendChild(create_line_break(document, str(first_line[1])))
      #logging.debug("called line break from create_p at page " + str(page.num) + " and line " + linecount)
  return current_prose

#Creates a line break of the given number
def create_line_break(document, linecount):
  #logging.debug("ENTERED line break at page " + str(page.num) + " and line " + linecount)
  lb = document.createElement("lb")
  lb.setAttribute("n", str(linecount))
  return lb
  
#Processes xml-ids for notes
def process_id(dict, id):
  """Makes sure every assigned xml-id is valid by checking for duplicates. Adds "i" 
  characters where necessary"""     
  if id in dict:
    duplicates = dict[id]
    dict[id] = dict[id] + 1
    logging.warning(" Duplicate marginnote id found: " + id + ". There may be duplicate pages in the Transcription File.")
    for i in range(0, duplicates):
      id += 'i'
  else:
    dict[id] = 1
  return id
    
def process_header(doc,tf):
  """Translates information contained in the header of the transcription file into XML."""

  marginheaders = [] # contains each note, its page number, and line
  footnotes = [] # doubles: [content, pagenum]
  xml_ids_dict = {}

  marginline_count = 1
  for page in tf.pages:
    for l in page.head:
      m = NOTES_RE.match(l)
      if m:
        continue

      m = MARGINNOTE_RE.match(l)
      if m:
        head = doc.createElement('head')
        marginheaders.append({'note' : head, 'page' : page.num, 'line' : m.group(1)})
        #check if page.num and m.group(1) are strings... should change them here?
        head.setAttribute('type','marginnote')
        marginnote_id = "p" + page.num + '-' + m.group(1)
        marginnote_id = process_id(xml_ids_dict, marginnote_id)
        head.setAttribute('xml:id', marginnote_id) 
        head.appendChild(doc.createTextNode(m.group(2)))
      
      m = FOOTNOTE_RE.match(l)
      if m:
        head = doc.createElement('head')
        footnotes.append([head, page.num])
        head.setAttribute('type', 'footnote')
        head.appendChild(doc.createTextNode(m.group(1)))
  return marginheaders, footnotes, xml_ids_dict

  
def process_body(document, tf, marginheaders, footnotes, xml_ids_dict, cfg):
  """Translates data contained in the body text of the transcription file into XML,
  combining the structure indicated in the body text with the given notes from the
  header."""
  current_prose = [] #list of paragraph nodes
  current_prose = create_p(document,current_prose,cfg)
  
  # get document body to appending below
  body = document.getElementsByTagName('body')[0]

  empty_lines = 0
  last_empty = False

  just_divided = False
  current_div1 = None
  current_div2 = None
  div1_head = None
  div2_head = None
  section_found = False
  subsection_found = False
  div1_count = 1
  div2_count = 1
  margin_queue = []
  
  for page in tf.pages:
    linecount = 0
    for l in page.body:
      linecount += 1
      
      #Insert margin notes when appropriate. Store early notes to add once first
      #section and subsection have been created.
      if len(marginheaders) > 0:
        current_marginnote = marginheaders[0]
        if linecount <= int(current_marginnote['line']) and page.num == current_marginnote['page']:
          if current_div2 == None:
            margin_queue.append(current_marginnote['note'])
          else:
            current_div2.appendChild(current_marginnote['note'])
          marginheaders.remove(current_marginnote)
      else:
        logging.debug("Ran out of marginheaders.")

      #Account for empty lines or double spacing
      if cfg.get('LINE_BREAKS'):
        m = EMPTYLINE_RE.match(l)
        if m:
          #found empty line
          last_empty = True
          empty_lines += 1
          continue
        elif last_empty:
          for i in range(1, empty_lines + 1):
            current_prose[-1].appendChild(create_line_break(document, str((linecount - empty_lines + (i - 1)))))
            #logging.debug("called line break from empty line handler line 710 at page " + str(page.num) + " and line " + linecount)
          last_empty = False
          empty_lines = 0
        
      # Creates section if found, or a generic section if one has not yet been created.
      # If new section occurs in the middle of a subsection, this subsection is divided
      # into two parts, labeled 'I' for initial, 'M' for medial, or 'F' for final as
      # corresponding to each case.
      m = SECTION_RE.match(l)
      if m:
        if not section_found:
          if current_div1 is not None:
            body.appendChild(current_div1)
          #Tab this current_div2 moves in?  
          if current_div2 is not None:
            next_div2 = current_div2.cloneNode(False)
            next_div2.setAttribute('part', 'F')
            atr = current_div2.getAttributeNode('part')
            x = atr.nodeValue
            if x == 'F':
              current_div2.setAttribute('part', 'M')
            else:
              current_div2.setAttribute('part', 'I')
            current_div2.childNodes.extend(current_prose)
            current_prose = create_p(document,current_prose,cfg, fresh=True)
            current_div1.appendChild(current_div2)
            current_div2 = next_div2

            # update div2s to get rid of original one 
          div1_head, div1 = create_div(document, str(div1_count), 'div1', None)
          current_div1 = div1
          div1_count += 1
            

        div1_head.appendChild(document.createTextNode(m.group(1)))
        if cfg.get('SECTION_IN_TEXT') and cfg.get('LINE_BREAKS'):
          div1_head.appendChild(create_line_break(document, linecount))
          #logging.debug("called line break from Section in Text line 756 at page " + str(page.num) + " and line " + linecount)
        else:
          linecount -= 1
        section_found = True
        continue
      else:
        if current_div1 == None:
          current_div1_head, current_div1 = create_div(document, str(div1_count), 'div1', None)
          div1_count += 1
          #current_div1, div1_count = create_generic_div(document, div1_count, 'div1')
          body.appendChild(current_div1)
        section_found = False
   
      # Creates a subsection, or a generic subsection if one has not yet been created.
      m = SUBSECTION_RE.match(l)  
      if m:
        if not subsection_found:
          just_divided = True
          if current_div2 is not None:
            #attach previous div2 and prose, clear already attached prose
            current_div2.childNodes.extend(current_prose)
            current_div1.appendChild(current_div2)
          current_prose = create_p(document,current_prose,cfg, fresh=True)
            
          #create new div2
          part = "N"
          div2_head, div2 = create_div(document, str(div2_count), 'div2', part)
          div2_count += 1
          if current_div2 == None:
            div2.childNodes.extend(margin_queue)
          current_div2 = div2
          
        div2_head.appendChild(document.createTextNode(m.group(1)))
        if cfg.get('SUBSECTION_IN_TEXT') and cfg.get('LINE_BREAKS'):
          div2_head.appendChild(create_line_break(document, linecount))
          #logging.debug("called line break from Subsection in Text line 788 at page " + str(page.num) + " and line " + linecount)
        else:
          linecount -= 1
        subsection_found = True 
        continue
      else: 
        if current_div2 == None:
          current_div2_head, current_div2 = create_div(document, str(div2_count), 'div2',
          part = "N")
          div2_count += 1
          #current_div2, div2_count = create_generic_div(document, div2_count, 'div2')
          current_div2.childNodes.extend(margin_queue)
          current_div1.appendChild(current_div2)
        subsection_found = False
        
      # Creates a paragraph if found a tab in the text.  
      m = PARA_RE.match(l)
      if m: 
        if just_divided:
          current_prose = create_p(document, current_prose, cfg, [l, linecount], fresh=True)
          just_divided = False
          #will this pose a problem if for some reason there isn't a paragraph right afterwards?
        else:
          current_prose = create_p(document, current_prose, cfg, [l,linecount])
      # Processes plain lines of body text
      else:
        just_divided = False
        current_prose[-1].appendChild(document.createTextNode(l))
        if cfg.get('LINE_BREAKS'):
          current_prose[-1].appendChild(create_line_break(document, str(linecount)))
          #logging.debug("called line break from else after paragraph creation (regular prose) line 817 at page " + str(page.num) + " and line " + linecount)
    # maybe add in something that says to delete the last line break 
    # before creating the next page to fix that bug?
      
    last_empty = False
    empty_lines = 0
    pb = document.createElement('pb')
    pb.setAttribute('n',str(page.num))
    current_prose[-1].appendChild(pb)
      # print([c.toxml() for c in current_prose],file=sys.stderr)
  # done looping, everything organized so stick the nodes onto the document
  current_div2.childNodes.extend(current_prose)
  current_div1.appendChild(current_div2)
  body.appendChild(current_div1)

def setup_argparse():
  ap = argparse.ArgumentParser()
  ap.add_argument('--file', '-f', help='choose a file for the autotagger')
  ap.add_argument('--verbose', '-v', action='count', dest='verbosity', 
      default=1, help='increase the verbosity (can be repeated: -vvv)') 
  ap.add_argument('--config', '-c', help = 'choose a configuration file (JSON) for specific document')
  return ap

def run(tf,cfg):
  """Translates transcription file into XML. Returns the complete XML document"""
  document = setup_DOM(cfg)
  marginheaders, footnotes, xml_ids_dict = process_header(document, tf)
  process_body(document, tf, marginheaders, footnotes, xml_ids_dict, cfg)
  return document
  
if __name__ in "__main__":

  # Accept a Svoboda Transcription Format file of given version on stdin
  ap = setup_argparse()
  args = ap.parse_args()
  if args.file:
    infile = open(args.file, encoding="utf-8")
    infilelines = infile.readlines()
  else:
    infilelines = sys.stdin.readlines()
  
  # if we got a user config file on the path, use that, otherwise
  # create a default config object
  if args.config:
    cfg = AutotaggerConfiguration(filepath=args.config)
  else:
    cfg = AutotaggerConfiguration()

  logging.basicConfig(format='%(levelname)s:%(message)s',
                          level=50-(args.verbosity*10)) 

  # Determine version and ensure transcription file is well formatted. If errors are found, 
  # reports these to the user. Any errors found must first be resolved by the user before 
  # process can continue.
  errors = [] 
  errors = check_errors(infilelines)
  if len(errors) > 0:
    logging.debug("ERRORS FOUND")
    print("Errors found. Please check error log and try again later.")
    #print('\n'.join(errors), file=sys.stderr)
    for e in errors:
      print(e,file=sys.stderr)
      
  # If transcription is properly formatted, compile a TranscriptionFile out 
  # of the inputed text. Convert TranscriptionFile to XML and print output
  else:
    logging.debug("NO ERRORS FOUND")
    tf = TranscriptionFile(infilelines)
    logging.info(" found "+str(len(tf.pages))+" transcription pages")
    document = run(tf, cfg)
    print(document.toprettyxml('\t', '\n', None))
  



  # Any errors found must first be resolved by the user before process can continue. 
  # If the TranscriptionFile properly follows the format, inputed text is converted
  # to XML and printed.
  #if len(tf.errors) > 0:
   # print("Errors found. Please check error log and try again later.")
    #for e in tf.errors:
     # print(e,file=sys.stderr)
  #else:
   # document = run(tf, cfg)
    #print(document.toprettyxml('\t', '\n', None))
