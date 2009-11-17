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


### Methods for showing images

def showImage(image, name):
	"""Helper method for displaying an image"""
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


def boundingBoxResult(original, settings, cutNo, color=None):
	"""Same as above but will paint the bounding boxes
	original should be the image data
	settings should be of class Settings
	cutNo as int
	color as CV_RGB"""

	method = settings.method
	if method == 'naive':
		return naiveMethod.getBoundingBoxImage(original, settings, cutNo, color)
	else:
		raise StandardError("No method named %s" % method)


#########################################
# The code below are tests and ugly hacks


def main():
	"""
	Just the test
	This method is a god resource on how to handle the results
	"""

	filename = sys.argv[1]
	image = highgui.cvLoadImage (filename)

	cutRatios = [lib.PHI]
	settings = Settings(cutRatios)
	image = highgui.cvLoadImage (filename)

	# Set the color for the boxes
	color = lib.COL_BLACK
	#color = lib.COL_WHITE
	#color = lib.COL_RED
	#color = lib.COL_GREEN
	#color = lib.COL_BLUE

	blobImg = blobResult(image, settings, 0)
	boxxImg = boundingBoxResult(image, settings, 0, color)
	compareImages(blobImg, boxxImg, "blob", "bounding box")
	#highgui.cvSaveImage('floodfillbilledet.png', blobImg)
	#highgui.cvSaveImage('boindingboxbilledet.png', boxxImg)

if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
