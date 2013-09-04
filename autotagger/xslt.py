#!/usr/bin/env python3
import shlex,subprocess

def tei2html(infile,outfile):
  of = open(outfile,'w',encoding='utf-8')
  args = shlex.split("xsltproc --nonet xslt/diary.xslt %(infile)s" 
                      % {'infile': infile })
  p = subprocess.Popen(args, stdout=of)
  p.wait()
  return p.returncode
