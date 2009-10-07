#!/usr/bin/python
import os # For opening files
import pysqlite3 # this is for python > 2.4
# from pysqlite2 import dbapi2 as sqlite # uncomment for python <= 2.4

#TODO:
#

##
# This will create a database given a location ad 
#
#
#
##

if len(sys.argv) < 2:
	print "Please atleast surply a location where to place the database"
	print "Do note that this has to be a location on the filesystem, since that is how sqlite operates"
	print "Proper Usage: ./init.py 

