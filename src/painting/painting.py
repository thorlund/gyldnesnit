"""
A framework to interact with a painting, and handling the database interaction
"""
#imports
from opencv import cv
from opencv import highgui

<<<<<<< HEAD
class Painting:
	#All the values we sohuld fill.
	image = None
	width = None
	height = None

	def __init__(self, filename):
		image = highgui.cvLoadImage(filename)
		if not image:
			raise SystemError('This picture is not parsable by opencv :'+filename)

	#setters and getters
	def setImage(self, filename):
		image = highgui.cvLoadImage(filename)
		if not image:
			raise SystemError('This picture is not parsable by opencv :'+filename)

	def setSize(self,width,height):
		self.width = width
		self.height = height

	def getImage(self):
		if not image:
			raise SystemError('This picture is not parsable by opencv :'+filename)
		else:
			return image

	def getWidth(self):
		return width

	def getHeight(self):
		return height

	def getWidthHeight(self):
		return (width,height)
