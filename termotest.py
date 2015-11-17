#!/usr/bin/python

import sys
from daenetip import * 

if (len(sys.argv) != 2):
	print "termotest <ip>"
	sys.exit()

d = daenetip(sys.argv[1])
print "Temperature is:",d.gettemp(0),"C"
