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
	print "Usage: csvfile [count]"
	print "The csvfile is surplied from wga.hu and count is the amount of pictures being downloaded"
	print "The csv file isn't located at the given location, please check:"
	print sys.argv[1]
	exit(-1)
csvfile = open(sys.argv[1],'r')
#gettings the location of resdir for the database to be placed
resdir = (os.getcwd()[:os.getcwd().find('src')+3]).replace('src','res') +'/'
##Default databasename
databasename = "pictureresource.db"
#default db starting crap
connectionString = 'sqlite:%s/%s' % (os.getcwd(), databasename)
connection = s.connectionForURI(connectionString)
s.sqlhub.processConnection = connection
#Creating the tables needed, if they exsists...That hack is kind of neat
m.Artist.createTable(ifNotExists=True)
m.Painting.createTable(ifNotExists=True)

#Parse the catelog.csv
csvfilelines = csvfile.readlines()

#The first line is the categories
categories = csvfilelines[0] 
csvfilelines = csvfilelines[1:]
categories = categories.split(';')
currentArtist = ("",)
#get the count on how many pictures should be downloaded
if len(sys.argv)==3:
	count = int(sys.argv[2])
	onlyoil=True
else:
	count = len(csvfilelines)
	onlyoil=False

#iterate over the rest of the lines
for line in csvfilelines:
	filepath = None
	line = line.split(';')
	(paint,material,realHeight,realWidth) = parser.parseTechnique(line[4])
#	#The artist has changed we need to make an artist in the database
	if not line[0]==currentArtist[0]:
		(born, died) = parser.bornDied(line[1])
		artist = m.Artist(name=line[0], born=born, died=died ,school=line[9],timeline=line[10])
		currentArtist=(line[0],artist.id)
	url=line[6]
	url = url.replace('html','art',1)
	url = url.replace('html','jpg')
	if count >= 0:
		#make dictionary
		dir = url[url.find('.')+1:url.rfind('/')+1]
		dir = resdir + dir
		if not os.path.isdir(dir):
			os.makedirs(dir)
		#get the file
		filepath = dir+url[url.rfind('/')+1:]
		#Only download a file if the restrictions is true, to ensure only oil is downloaded in a small database
		if (onlyoil and find(lower(paint),"oil")>0) or onlyoil ==False:
			count = count - 1
			if not os.path.isfile(filepath):
				urllib.urlretrieve(url,filepath)
	painting = m.Painting(artist=currentArtist[1],title=line[2],date = parser.dateParser(line[3]), paint = paint, material = material, realHeight = realHeight, realWidth = realWidth, location=line[5],url=line[6],form=line[7],type=line[8], width=None, height=None, filepath=filepath)
# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
