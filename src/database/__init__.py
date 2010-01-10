#!/usr/bin/python
"""
Database

"""

# Get basedir
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import re
import src.model as m
import sqlobject as s
import parser
import urllib
class Database:
	csvfile = ""
	location = "pictureresource.db"
	count = None
	def setCSVFile(self,csvfile):
		self.csvfile = csvfile
	def setLocation(self,location):
		self.location = location
	def setCount(self,count):
		self.count = count
	def getCSVFile(self):
		return self.csvfile
	def getLocation(self):
		return self.location
	def getCount(self):
		return self.count
	def exists(self):
		return os.path.isfile(self.location)
	def empty(self):
		value = m.Artist.select().count()==0
		value = value and  m.Painting.select().count()==0
		return value
	def __init__(self,settings):
		self.setLocation(settings.getDatabaseLocation())
		connectionString = 'sqlite:%s/%s' % (os.getcwd(), self.location)
		connection = s.connectionForURI(connectionString)
		s.sqlhub.processConnection = connection
		m.Artist.createTable(ifNotExists=True)
		m.Painting.createTable(ifNotExists=True)
		m.Run.createTable(ifNotExists=True)
		m.Result.createTable(ifNotExists=True)
		m.Region.createTable(ifNotExists=True)
		self.setCSVFile(settings.getCSVFileLocation())
		#print self.csvfile

	def constructDatabase(self):
		csvfile = open(self.csvfile,'r')
		#Parse the catelog.csv
		csvfilelines = csvfile.readlines()

		#The first line is the categories
		categories = csvfilelines[0] 
		csvfilelines = csvfilelines[1:]
		categories = categories.split(';')
		currentArtist = ("",)
		#get the count on how many pictures should be downloaded also make sure that only oil paintings are downloaded if a number is given
		count = self.count
		if not count == None:
			count = count
			onlyoil=True
		else:
			count = len(csvfilelines)
			onlyoil=False

		#iterate over the rest of the lines
		for line in csvfilelines:
			print 'database is now looking at %s' % line
			line = line.split(';')
			if count > 0 and len(line)==11:
				filepath = None
				(paint,material,realHeight,realWidth) = parser.parseTechnique(line[4])
			#The artist has changed we need to make an artist in the database
				if not line[0]==currentArtist[0]:
					(born, died) = parser.bornDied(line[1])
					if (m.Artist.select(m.Artist.q.name == line[0])).count()==0:
						artist = m.Artist(name=line[0], born=born, died=died ,school=line[9],timeline=line[10])
						currentArtist=(line[0],artist.id)
					else:
						currentArtist=(line[0],m.Artist.select(m.Artist.q.name ==line[0]).getOne())
#				print currentArtist
				url=line[6]
				url = url.replace('html','art',1)
				url = url.replace('html','jpg')
					#make dictionary
				dir = url[url.find('.')+1:url.rfind('/')+1]
				resdir = (os.getcwd()[:os.getcwd().find('src')+3]).replace('src','res') +'/'
				dir = resdir + dir
				if not os.path.isdir(dir):
					os.makedirs(dir)
				#get the file
				filepath = dir+url[url.rfind('/')+1:]
				#Only download a file if the restrictions is true, to ensure only oil is downloaded in a small database
				if (onlyoil and not paint == None and paint.find("oil")>0) or onlyoil ==False:
					if not os.path.isfile(filepath):
						print url + '\n'
						print filepath + '\n'
						print line[6] + '\n'
						print line
						urllib.urlretrieve(url,filepath)
					if m.Painting.select(m.Painting.q.url==line[6]).count()==0:
						count = count - 1
						painting = m.Painting(artist=currentArtist[1],title=line[2],date=parser.dateParser(line[3]), paint = paint, material = material, realHeight = realHeight, realWidth = realWidth, location=line[5],url=line[6],form=line[7],type=line[8], width=None, height=None, filepath=filepath)

# Tests
def main():
	print "beware of the test monster...output is gonna hit for you over 9000 damage"	
	db = Database()
	db.setCount(5)
	db.constructDatabase()
	#check location of db
	print 'The db is located at %s is that correct python? %s' % (db.getLocation(),db.exists())
	#check om vi har modtaget 5 billeder og om de er af oile"
	alle = m.Painting.select()
	print list(alle)
	db.setCount(4)
	db.constructDatabase()
	alle = m.Painting.select()
	print '9 pictures were added to the database how many is there now? :D'
	print alle.count()
	print "Warning will now try to get the entire database"
	db.setCount(None)
	db.constructDatabase()

if __name__ == "__main__":
	main()
# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
