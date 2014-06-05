#!/usr/bin/env python3

import unittest
import autotagger
import sys
from lxml import etree

class Test(unittest.TestCase):

  def test_d48(self):
    # tests output of diary 48 of svoboda diaries

    self.run_Test("texts\d48_clean.txt", "outputs\d48_out.xml")
  
  def test_double_space(self):
    # tests output of double space test

    self.run_Test("texts\double_space_test.txt", "outputs\double_out.xml")

  def test_emma(self):
    # tests output of emma b. andrews file

    self.run_Test("texts\emma-vol-1-autotagger-test-fixed.txt", "outputs\emma_out.xml")

  def test_generic_divs(self):
    # tests output of generic div test file

    self.run_Test("texts\generic_test.txt", "outputs\generic_out.xml")

  def test_sultan_1(self):
    # tests output of first sultan's dream file

    self.run_Test("texts\KM_test_Justin_1.txt", "outputs\sultan_1_out.xml")

  def test_sultan_2(self):
    # tests output of second sultan' dream file

    self.run_Test("texts\KM_test_Justin_2.txt", "outputs\sultan_2_out.xml")

  def run_Test(self, input, output):
    # runs test for each input file
 
    file = open(input, encoding="utf-8")
    lines = file.readlines()
    file.close()
    # lines is a big (collection of) string(s)
    tf = autotagger.TranscriptionFile(lines)
    document = autotagger.setup_DOM()
    div2s, marginheaders, margins_dict = autotagger.create_dom_nodes(document, tf)
    autotagger.organize_nodes(document, tf, div2s, marginheaders, margins_dict)
    # document is an XML object
    # don't reprint the document as a string, just 
    # use the document

    if input == "texts\d48_clean.txt":
      print(document.toprettyxml('\t', '\n', None))
    # note that text nodes should only be 
    # in p, l, note, etc (and the values of attributes).
    # all other text is ignorable.

    parser = etree.XMLParser(remove_blank_text=True)
    correct_document = etree.parse(output, parser)
    correct_doc_element = correct_document.getroot()
    isEqual = self.compare(document.documentElement, correct_doc_element)
    self.assertTrue(isEqual)

  def compare(self, test_element, correct_element):
    # compares the two documents 
  
    if test_element is None and correct_element is None:
      return True
    elif test_element is None or correct_element is None:
      return False
    else:
      test_is_text = test_element.nodeType == test_element.TEXT_NODE
      correct_is_text = correct_element.text != ""
      if test_is_text and correct_is_text:
        if test_element.data == correct_element.text:
          return True
        else:
          return False
      elif test_is_text or correct_is_text:
        return False
      else:
        test_attr = test_element.attributes
        correct_attr = correct_element.attrib
        tag_name_equal = test_element.tagName == correct_element.tag
        attr_length_equal = test_attr.length == len(correct_attr)

        if not tag_name_equal or not attr_length_equal:
          return False
        else:
          for i in range (0, test_attr.length):
            same_name = correct_attr.get(test_attr.item(i).name) != None
            same_value = correct_attr.get(test_attr.item(i).name) == test_attr.item(i).value
            if not same_name or not same_value:
              return False
          test_children = test_element.childNodes
          correct_children = len(correct_element)
          if test_children.length != correct_children:
            return False
          else:
            for i in range (0, test_children.length):
              test_child = test_children.item(i)
              correct_child = correct_element[i]
              match = self.compare(test_child, correct_child)
              if match == False:
                return False
            return True

if __name__ == '__main__':
  unittest.main()
