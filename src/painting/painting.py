"""
A framework to interact with a painting, and handling the database interaction
"""
#imports
from opencv import cv
from opencv import highgui

#All the values we sohuld fill.
image = None
width = None
height = None

#setters and getters
def setImage( filename):
	image = highgui.cvLoadImage(filename)
	if not image:
		raise SystemError('This picture is not parsable by opencv :'+filename)

def setSize(width,height):
	self.width = width
	self.height = height

def getImage():
	if not image:
		raise SystemError('This picture is not parsable by opencv :'+filename)
	else:
		return image

def getWidth():
	return width

def getHeight():
	return height

def getWidthHeight():
	return (width,height)
