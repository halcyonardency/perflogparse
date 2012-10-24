#!/usr/bin/python2.6

import re, sys, pprint

def openLogFile(path):
   args = ()

   if path.find(':') >= 0:
      host, path = path.split(':')
      if path.endswith('.gz'):
         exe = 'zcat'
      else:
         exe = 'cat'
   
      args = ('ssh', host, exe, path)
   elif path.endswith('.gz'):
      args = ('zcat', path)
  
   if args:
      p = subprocess.Popen(shell=False, args=args, stdout=subprocess.PIPE)
      return p.stdout
   else:
      return open(path, 'r')



def loadlog (file):
   fp = openLogFile(file)
   pp = pprint.PrettyPrinter(indent=4)
   for line in fp.xreadlines():
      sys.stdout.write("\n")
      log = parseLine(line)
      pp.pprint(log)

def parseLine (line):
   match = PATTERN.match(line)
   if not match:
      sys.stdout.write("FAIL: "+line+"\n")
   else:
      sys.stdout.write("PASS: "+line+"\n")
   return match.groups()


PATTERN = re.compile(
   r"""
     ^([0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3})\s
      ([^ ]{1,})\s
      ([^ ]{1,}|\-)\s
      \[([0-9]{2}\/[A-Za-z]{3}\/[0-9]{1,4}:[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}\s[+\-][0-9]{4})\]
      \s"
	(\S+)\s
	(.*)\s
	(\S+)(?<!\\)"\s+
      ([0-9]{3})\s
      ([0-9]{1,}|\-)\s
      "(.*)(?<!\\\\)"\s+
      "(.*)(?<!\\\\)"+
      	(?:
		\s([0-9]{1,}|\-)\s
      	)+
	(?:
      		"(.*)(?<!\\)"\s+
	)+
      	(?:
		"(.*)(?<!\\)"\s+
	)+
      	(?:
      		([0-9]{1,}|\-)
	)+
   """, re.VERBOSE)


p = loadlog('all.log')
