#!/usr/bin/python
import os # For opening files
#import pysqlite # Google python db api 2.0, this is the sqlite 
from pysqlite2 import dbapi2 as sqlite3#This is rather blackmagic atm, research for the report ^^

##
# This should init the database with the connection string given below
#
#
#
##
#TODO:
# Make a good database design
# Understand that import
if len(sys.argv) < 2:
	print "Missing arguments"
	print "Please suply atleast the location for the database"
	print "Usage ./init.py <location> [location of csv file]"
	print "The csv file should, for now, be from wga.hu"
	exit(-1)
location = sys.argv[1]
csvfile = ""
if len(sys.argv) == 3:
	csvfile = sys.argv[2]

#Making the database with tables and such


