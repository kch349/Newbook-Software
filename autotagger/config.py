#!/usr/bin/env python3
import json
import io
import sys

# CONFIG_INFO = json.load('file name here?')

class AutotaggerConfiguration:
  """This class contains and updates a config object for the
     Autotagger ...."""
  CONFIG_INFO = {'SECTION_IN_TEXT' : True, #True if title in body text
                 'SUBSECTION_IN_TEXT' : False, #False if title in margin or elsewhere
                 'NUMBER_OF_DIVS' : 2, # Number of divisions present
                 'TITLE' : 'Insert Document Title Here', #Beginning OF TEI header info
                 'AUTHOR' : 'Insert Author Name Here',
                 'RESP_PROJECT' : 'Insert Name of Project Responsible for Transcription',
                 'PROJECT_LEAD' : 'Insert Name of Project Lead',
                 'DISTRIBUTOR' : 'Insert Distributor Name Here',
                 'ID_TYPE' : 'Insert Your Type Here',
                 'ID_VALUE' : 'Insert ID Number Here',
                 'COPYRIGHT' : 'Insert Copyright Data Here',
                 'DATE' : 'Insert Date Here',
                 'DATE_LAST_UPDATED' : 'Insert Date of Last Edit', # will slightly change output of generics
                 'BIBL_INFO' : 'Enter Bibliographical Information Here',
                 'PROJECT_DESC' : 'Insert Project Here',
                 'LINE_BREAKS':True}
  
  def __init__(self,options_dict=None, filepath=None):
    if options_dict != None:
      try: 
        for o in options_dict.keys():
          self.CONFIG_INFO[o]=options_dict[o]
      except KeyError as e: 
        print(e,file=sys.stderr) 
    elif filepath != None:
      self.read_from_file(filepath)
        
  def write_to_file(self, path):
    """save config info to file"""
    #save json file as output_file
    with open(path, 'w') as output_file:
      json.dump(data, output_file)

  def read_from_file(self, path):
    """read config info from file"""
     #Inserted way to read from json file similar to what was in the autotagger before
    config_file = open(path, encoding ="utf-8") #not sure if this is the proper way to open here
    json_data = json.load(config_file)
    config_upload = json_data['config_options']
    for key in config_upload:
      if key in self.CONFIG_INFO:
  	    self.CONFIG_INFO[key] = config_upload[key]

  def get(self,name):
    try:
      return self.CONFIG_INFO[name]
    except KeyError as e:
      print(e,file=sys.stderr)
  
