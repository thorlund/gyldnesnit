#!/usr/bin/env python
"""
Provides methods for showing graphic results.
Functions as an abtraction layer for different methods.
"""

# Import what we need from OpenCV
from opencv import cv
from opencv import highgui

# Access to other libraries
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import goldenLibrary as lib
from src.settings import Settings

# Import available methods
import naiveMethod
import src.lib.marginCalculator as marginCalculator

### Methods for showing images

def showImage(image, name):
	"""Helper method for displaying an image"""
	# Do NOT save images to disk in this method
	winname = name

	highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

	while True:
		highgui.cvShowImage (winname, image)

		c = highgui.cvWaitKey(0)

		if c == 'q':
			print "Exiting ..."
			print ""
			sys.exit(0)


def compareImages(img1, img2, name1, name2):
	# Do NOT save images to disk in this method
	winname1 = name1
	winname2 = name2

	highgui.cvNamedWindow (winname1, highgui.CV_WINDOW_AUTOSIZE)
	highgui.cvNamedWindow (winname2, highgui.CV_WINDOW_AUTOSIZE)

	while True:
		highgui.cvShowImage (winname1, img1)
		highgui.cvShowImage (winname2, img2)

		c = highgui.cvWaitKey(0)

		if c == 'q':
			print "Exiting ..."
			print ""
			sys.exit(0)


### Methods for retreiving image results

def blobResult(original, settings, cutNo):
	"""Show the colored blobs in an image at the cut specified
	by cutNo as int. The cut ratio are placed in the settings and only
	the first cut in this ratio-list will be analyzed.
	original should be the image data
	settings should be of class Settings
	cutNo as int"""

	method = settings.method
	if method == 'naive':
		return naiveMethod.getBlobImage(original, settings, cutNo)
	else:
		raise StandardError("No method named %s" % method)


def boundingBoxResult(original, settings, cutNo, thickness=1, color=None):
	"""Same as above but will paint the bounding boxes
	original should be the image data
	settings should be of class Settings
	cutNo as int
	color as CV_RGB"""

	method = settings.method
	if method == 'naive':
		return naiveMethod.getBoundingBoxImage(original, settings, cutNo, thickness, color)
	else:
		raise StandardError("No method named %s" % method)


#########################################
# The code below are tests and ugly hacks


def main():
	"""
	Just the test
	This method is a good resource on how to handle the results.
	Save images in this method if you have to.
	"""

	filename = sys.argv[1]
	image = highgui.cvLoadImage (filename)

	cutRatios = [lib.PHI]
	settings = Settings(cutRatios)
	image = highgui.cvLoadImage (filename)
	thickness = 4
	settings.setMarginPercentage(0.025)
	cut = int(sys.argv[2])
	winname = sys.argv[3]+".png"
	#settings.setThresholds(100,150)
	# Set the color for the boxes
	#color = lib.COL_BLACK
	#color = lib.COL_WHITE
	#color = lib.COL_RED
	color = lib.COL_GREEN
	#color = lib.COL_BLUE

	blobImg = blobResult(image, settings, cut)
	boxxImg = boundingBoxResult(image, settings, cut, thickness, color)
	cutt = lib.findMeans(cv.cvGetSize(image), settings.cutRatios[0])[cut]
	# cuttet verdi, dog skal det vi generaliseres lidt
	oriantesen = cutt.getPoints()[0].x == cutt.getPoints()[1].x
	if oriantesen:
		cutPixel = cutt.getPoints()[1].x
	else:
		cutPixel = cutt.getPoints()[1].y
	
	if oriantesen:
	#	print 'hej'
		cv.cvLine(boxxImg, cv.cvPoint(cutPixel, cutt.getPoints()[0].y), cv.cvPoint(cutPixel, cutt.getPoints()[1].y), lib.COL_RED)
	else:
		cv.cvLine(boxxImg, cv.cvPoint(cutt.getPoints()[0].x, cutPixel), cv.cvPoint(cutt.getPoints()[1].x, cutPixel), lib.COL_RED)
	# Save images
	highgui.cvSaveImage('floodfillbilledet.png', blobImg)
	highgui.cvSaveImage(winname, boxxImg)

	# Show images
	compareImages(blobImg, boxxImg, "blob", winname)

if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
