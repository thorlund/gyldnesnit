#!/usr/bin/python

# Get basedir
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import re
import src.model as m
import sqlobject as s
import parser
import urllib

##Do some testing if the csvfile exsists:
if not os.path.isfile(sys.argv[1]):
	print "The csv file isn't located at the given location, please check:"
	print sys.argv[1]
	exit(-1)
csvfile = open(sys.argv[1],'r')
##Default databasename
databasename = "pictureresource.db"
connectionString = 'sqlite:%s/%s' % (os.getcwd(), databasename)
connection = s.connectionForURI(connectionString)
s.sqlhub.processConnection = connection
m.Artist.createTable()
m.Painting.createTable()
if len(sys.argv)==3:
	count = int(sys.argv[2])

#Parse the catelog.csv
csvfilelines = csvfile.readlines()

#The first line is the categories
categories = csvfilelines[0] #yes, there is prob a better way to do this.
csvfilelines = csvfilelines[1:]
categories = categories.split(';')
currentArtist = ("",)
for line in csvfilelines:
	filepath = None
	line = line.split(';')
#	#The artist has changed we need to make an artist in the database
	if not line[0]==currentArtist[0]:
		(born, died) = parser.bornDied(line[1])
		artist = m.Artist(name=line[0], born=born, died=died ,school=line[9],timeline=line[10])
		currentArtist=(line[0],artist.id)
	url=line[6]
	url = url.replace('html','art',1)
	url = url.replace('html','jpg')
	if count > 0:
		#lav biblotekerne
		dir = url[url.find('.')+1:url.rfind('/')+1]
		dir = (os.getcwd()[:os.getcwd().find('src')+3]).replace('src','res') +'/'+ dir
		print dir
		if not os.path.isdir(dir):
			os.makedirs(dir)
		#hent filen
		filepath = dir+url[url.rfind('/')+1:]
		urllib.urlretrieve(url,filepath)
		count = count - 1
	(paint,material,realHeight,realWidth) = parser.parseTechnique(line[4])
	painting = m.Painting(artist=currentArtist[1],title=line[2],date = parser.dateParser(line[3]), paint = paint, material = material, realHeight = realHeight, realWidth = realWidth, location=line[5],url=line[6],form=line[7],type=line[8], width=None, height=None, filepath=filepath)
# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
