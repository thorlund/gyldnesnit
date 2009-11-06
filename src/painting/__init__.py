#!/usr/bin/env python
"""
A framework to interact with a painting, and handling the database interaction
"""
#imports
from opencv import cv
from opencv import highgui
import sys

class Painting:
	#All the values we sohuld fill.
	id = None
	image = None
	width = None
	height = None
	results = None

	def __init__(self, entry):
		self.id = entry.id
		filename = entry.location
		self.image = highgui.cvLoadImage(filename)
		if not self.image:
			raise SystemError('This picture is not parsable by opencv :'+filename)
		self.setSize(self.image.width,self.image.height)

	#setters and getters
	def setResults(self, results):
		self.results = results

	def getResults(self):
		return self.results

	def getId(self):
		return self.id

	def setImage(self, filename):
		self.image = highgui.cvLoadImage(filename)
		if not self.image:
			raise SystemError('This picture is not parsable by opencv :'+filename)

	def setSize(self,width,height):
		self.width = width
		self.height = height

	def getImage(self):
		if not self.image:
			raise SystemError('This picture is not a valid picture')
		else:
			return self.image

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getWidthHeight(self):
		return (self.width,self.height)

def main():
	if len(sys.argv)<2:
		print "throw a image my way"
		sys.exit(-1)
	
	print "Im testing"
	test = Painting(sys.argv[1])
	print test.getWidth()
	print test.getHeight()
	winname ="Test"
	highgui.cvNamedWindow(winname, highgui.CV_WINDOW_AUTOSIZE)
	while True:
		highgui.cvShowImage(winname,test.getImage())
		c = highgui.cvWaitKey(0)
		if c == 'q':
			sys.exit(0)

if __name__ == "__main__":
	main()
