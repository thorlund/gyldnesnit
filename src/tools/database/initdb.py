#!/usr/bin/python

# Get basedir
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import os # For opening files
import sqlite3 # this is for python > 2.4
import re
# from pysqlite2 import dbapi2 as sqlite # uncomment for python <= 2.4
import src.model as m
import sqlobject as s


#TODO:
#
##
# This will create a database given a location 
#
# 
# if in doubt check http://docs.python.org/library/sqlite3.html
# Remeber to check if python has been compiled with sqlite
##

#if len(sys.argv) < 2:
#	print "Please atleast surply a location where to place the database"
#	print "Do note that this has to be a location on the filesystem, since that is how sqlite operates"
#	print "Proper Usage: ./init.py <filename of csv file> [location of database]"
#	print "It is taken for a given that the file given is a correctly formated file"
#	print "The definition of correctly formatted is a comma seperated file from wga.hu"
#	print "Default location will be the current directory if nothing else is surplied"
#	print "WARNING: Will flush the current database"
#	exit(-1)
#
##Do some testing if the csvfile exsists:
if not os.path.isfile(sys.argv[1]):
	print "The csv file isn't located at the given location, please check:"
	print sys.argv[1]
csvfile = open(sys.argv[1],'r')
##Default databasename if no other is given 
databasename = "pictureresource.db"
if len(sys.argv) ==3:
	databasename = sys.argv[2]

connectionString = 'sqlite:%s/%s' % (os.getcwd(), databasename)
connection = s.connectionForURI(connectionString)
s.sqlhub.processConnection = connection
m.Artist.createTable()
m.Painting.createTable()

#connection = sqlite3.connect(databasename)
##A cursor is how you send commands to the database
#cursor = connection.cursor()
#
##flush the current database
#if os.path.isfile(databasename):
#	cursor.execute('SELECT name FROM sqlite_master WHERE type = "table";')
#	i = 0
#	for row in cursor:
#		i = i+1
#		if not row[0] == 'sqlite_sequence':
#			row = 'DROP TABLE '+row[0]
#			cursor.execute(row)
#			connection.commit()
#print "Database now purged"
#
#Parse the catelog.csv
csvfilelines = csvfile.readlines()

#The first line is the categories
categories = csvfilelines[0] #yes, there is prob a better way to do this.
csvfilelines = csvfilelines[1:]
categories = categories.split(';')
# This is how it look...yes, im gonna do some horrible static crap now ^_^ brace yourself
# ARTIST;BORN-DIED;TITLE;DATE;TECHNIQUE;LOCATION;URL;FORM;TYPE;SCHOOL;TIMELINE
# artist table = id & 1,2,10,11
# art piece = id & artist & 3,4,5,6,7,8,9
##Removing anything that shouldnt be included in the SQL
#It is very convient that wga.hu is writing in all caps. It is a bit static tho
#for i in range(len(categories)):
#	categories[i] = re.sub("[^A-Z]","",categories[i])
##Making the artist SQL table
#artist = (categories[0],categories[1],categories[9],categories[10])
#artisttable = 'CREATE TABLE artist(id INTEGER PRIMARY KEY ASC AUTOINCREMENT'
#for artistcategory in artist:
#	artisttable += ' ,'+artistcategory +' TEXT'
#artisttable += ');'
#cursor.execute(artisttable)
#connection.commit()
#print "artist table created"
##Making the art SQL table
#artpiece = ('FILELOC',categories[2],categories[3],categories[4],categories[5],categories[6],categories[7],categories[8])
#artpiecetable = 'CREATE TABLE artpiece (id INTEGER PRIMARY KEY ASC AUTOINCREMENT, artist INTEGER'
#for artpiececategory in artpiece:
#	artpiecetable += ' ,'+artpiececategory+' TEXT'
#artpiecetable += ', FOREIGN KEY (artist) REFERENCES artist(id));'
#cursor.execute(artpiecetable)
#connection.commit()
#print "artpiece table created"
#
#Now the database is ready to recieve the data
#Again we utilize the data we get from wga.hu is very well formated
#Remeber to split the statement first! ^^
currentArtist = ("",)
##csvfilelines = encode(csvfilelines,'uft-16')
for line in csvfilelines:
#	line = unicode(line,errors='replace')
	line = line.split(';')
#	#The artist has changed we need to make an artist in the database
	if not line[0]==currentArtist[0]:
		artist = m.Artist(name=line[0], born=line[1],school=line[9],timeline=line[10])
		currentArtist=(line[0],artist.id)
	painting = m.Painting(artist=currentArtist[1],title=line[2],date=line[3], technique=line[4],location=line[5],url=line[6],form=line[7],type=line[8], width=None, height=None)
#		cursor.execute('INSERT INTO artist VALUES (null,?,?,?,?);',(line[0],line[1],line[9],line[10]))
#		connection.commit()
#		artistSearchString = 'SELECT id FROM artist WHERE '+categories[0]+'=?'
#		cursor.execute(artistSearchString,(line[0],))
#		currentArtist = (line[0],cursor.fetchone()[0])
#	cursor.execute('INSERT INTO artpiece VALUES (null,?,?,?,?,?,?,?,?,?);',(currentArtist[1],"",line[2],line[3],line[4],line[5],line[6],line[7],line[8]))
#cursor.execute('SELECT * FROM artpiece')
#print "The dokument is now ported into the database"
#
##Send a close flag to the database
#connection.commit()
##closing the cursor again
#cursor.close()
