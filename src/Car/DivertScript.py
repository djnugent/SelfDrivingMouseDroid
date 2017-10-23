#!/usr/bin/python3.5

import sys, getopt

def main(argv):
     inputDistance = ''
	 try:
	      opts, args = getopt.getopt(argv, "l:r:",["lvalue", "rvalue"])
     except getopt.GetoptError:
	      print("DivertScript.py -v <divergeDistance>")
		  sys.exit(2)
	 for opt, arg in opts:
	      if opt in ("-l", "--lvalue"):
		       inputDistance = (-1) * arg
		  elif opt in ("-r", "--rvalue"):
		       inputDistance = arg
	 print("Diverging {} ft".format(inputDistance))