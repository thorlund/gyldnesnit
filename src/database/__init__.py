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
	csvfile = os.getcwd() + "catalog.csv"
	databasename = "pictureresource.db"
	count = None
	def setCSVFile(self,csvfile):
		self.csvfile = csvfile
	def setDatabaseName(self,databasename):
		self.databasename = databasename
	def setCount(self,count):
		self.count = count
	def getCSVFile(self):
		return self.csvfile
	def getDatabaseName(self):
		return self.databasename
	def getCount(self):
		return self.count
	def constructDatabase(self):
		resdir = (os.getcwd()[:os.getcwd().find('src')+3]).replace('src','res') +'/'
		csvfile = open(self.csvfile,'r')
		#gettings the location of resdir for the database to be placed
		#default db starting crap
		connectionString = 'sqlite:%s/%s' % (os.getcwd(), self.databasename)
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
		count = self.count
		if not count == None:
			count = count
			onlyoil=True
		else:
			count = len(csvfilelines)
			onlyoil=False

		#iterate over the rest of the lines
		for line in csvfilelines:
			if count >= 0:
			filepath = None
			line = line.split(';')
			(paint,material,realHeight,realWidth) = parser.parseTechnique(line[4])
		#The artist has changed we need to make an artist in the database
			if not line[0]==currentArtist[0]:
				(born, died) = parser.bornDied(line[1])
				if len(m.Artist.select(m.Artist.q.name == line[0]))==0:
					artist = m.Artist(name=line[0], born=born, died=died ,school=line[9],timeline=line[10])
				currentArtist=(line[0],artist.id)
			url=line[6]
			url = url.replace('html','art',1)
			url = url.replace('html','jpg')
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
			if len(m.Painting.select(m.Painting.q.url==line[6])==0:
			painting = m.Painting(artist=currentArtist[1],title=line[2],date = parser.dateParser(line[3]), paint = paint, material = material, realHeight = realHeight, realWidth = realWidth, location=line[5],url=line[6],form=line[7],type=line[8], width=None, height=None, filepath=filepath)

# Tests
def main():
	print "beware of the test monster...output is gonna hit for you over 9000 damage"	
	init("",count=5)
	#check location of db

if __name__ = "__main__":
	main()
# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
