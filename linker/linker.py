#!/usr/bin/python

# @author Adam Croissant (adam.croissant@gmail.com)

# This script adds links to a JMS diary html file which link to the contentDM images of the diary
# pages. Requires html format to have page numbers surrdouned by spans with class='pb' and for the
# actual page numbers themselves to appear formatted as [pg: ##]. This script uses the BeautifulSoup4
# library to crawl, parse, and edit the HTML. Documentation can be found at
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/ . To install bs4 on UW servers use
# "easy_install --prefix=[your_local_python_library_directory]" beautifulsoup4. On the newbook account,
# local python library is $HOME/.local. On the ndthtech account, it is at $HOME/local.
# To create valid html5, BeautifulSoup also requires installation of a non-default html parser. To
# do this, use the command "easy_install --prefix=[your_local_python_library_directory]" html5lib. If
# you don't install html5lib, this script WILL NOT function.
import sys, getopt
import re
from bs4 import BeautifulSoup

base_link = 'http://digitalcollections.lib.washington.edu/cdm/ref/collection/iraqdiaries/id/'

# map of [diary_no]=>start page for url
start_nums = {47: 427, 48: 820, 49: 1223, 50:0, 51: 1658, 52: 3361, 53: 9201, 55: 2127, 56: 2521, 59: 2524, 60: 2915}

# function goes through all spans with class 'pb' and adds a tags with link
def add_links(soup, start_num):
    for page in soup.find_all('span', class_='pb'):
        tag_text = page.string
        m = re.search('\[pg: ([0-9]+)\]', tag_text)
        page_no = int(m.group(1))

        #reset page's enclosed string (will be held inside <a> tag)
        page.string = ''
        # build <a> tag & set enclosed text
        link = soup.new_tag("a", href=base_link + str(start_num + page_no), target='blank')
        link.string = tag_text.strip()
        print "Adding link: " + link['href'] + " for page no. " + str(page_no)

        #insert <a> tag to span
        page.append(link)
        

def main():
    diary_no = 0
    inputfile = ''
    outputfile = ''

    opts = []
    args = []
    
    # make sure that all required options are provided
    if "-d" not in sys.argv[1:] or "-i" not in sys.argv[1:] or "-o" not in sys.argv[1:]:
        print 'USAGE: linker.py -d <diary number> -i <input file> -o <output file>'
        sys.exit(2)
    
    # gathers arguments and ensures that required options have an accompanying argument
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:i:o:", ["diaryno=", "infile=", "outfile="])
    except getopt.GetoptError:
        print 'USAGE: linker.py -d <diary number> -i <input file> -o <output file>'
        sys.exit(2)

    
    # iterate through arguments and validate, set as appropriate variables
    for opt, arg in opts:
        if opt == '-d':
            diary_no = int(arg)

            if diary_no not in start_nums:
                print('ERROR: Diary ' + str(diary_no) + ' not supported')
                sys.exit(2)
        elif opt == '-i':
            inputfile = arg
        elif opt == '-o':
            outputfile = arg

    print('Attempting to add links to file ' + inputfile +  ' for diary ' + str(diary_no) + ', outputting to ' + outputfile)

    # open infile and construct BeautifulSoup object
    try:
        soup = BeautifulSoup(open(inputfile), "html5lib")
    except IOError:
        print("ERROR: Could not open file or read data from input file " + inputfile)
        sys.exit(2)

    # add links to file and output in utf-8 format to output file
    add_links(soup, start_nums[diary_no])
    out = soup.prettify('utf-8')

    try:
        outfile = open(outputfile, "w")
        outfile.write(out)
        outfile.close()
    except IOError:
        print("ERROR: Could not write data to output file " + outputfile)
        sys.exit(2)

main()
