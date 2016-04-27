#!/usr/bin/env python3
import shlex,subprocess

def tei2html(infile,outfile,xsltfile):
  of = open(outfile,'w',encoding='utf-8')
  #if xsltfile == lb:
  args = shlex.split("xsltproc --nonet xslt/tei2html_"+xsltfile+".xslt %(infile)s" 
                      % {'infile': infile })
  p = subprocess.Popen(args, stdout=of)
  p.wait()
  return p.returncode

def tei2latex(infile,outfile):
  of = open(outfile,'w',encoding='utf-8')
  args = shlex.split("xsltproc --nonet xslt/tei2latex.xslt %(infile)s" 
                      % {'infile': infile })
  p = subprocess.Popen(args, stdout=of)
  p.wait()
  return p.returncode
