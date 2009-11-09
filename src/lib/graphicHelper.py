#!/usr/bin/env python
"""
Provides methods for showing graphic results
"""

# Import what we need from OpenCV
from opencv import cv
from opencv import highgui

import goldenLibrary as lib
import paintingAnalyzer
import marginCalculator

import sys


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

	highgui.cvSaveImage('floodfillbilledet.png',img1)
	highgui.cvSaveImage('boindingboxbilledet.png',img2)
	while True:
		highgui.cvShowImage (winname1, img1)
		highgui.cvShowImage (winname2, img2)

		c = highgui.cvWaitKey(0)

		if c == 'q':
			print "Exiting ..."
			print ""
			sys.exit(0)


def blobResult(original, settings, cutNo):
	"""Show the colored blobs in an image at the cut specified
	by cutNo as int. The cut ratio are placed in the settings and only
	the first cut in this ratio-list will be analyzed.
	painting should be of class Painting
	settings should be of class Settings
	cutNo as int"""
	# Get the cut defined by cutNo from the cuts from the first cut ratio in settings
	cut = lib.findMeans(cv.cvGetSize(original), settings.cutRatios[0])[cutNo]
	# Get the BW edge image
	edgeImage = paintingAnalyzer.getEdgeImage(original, settings)
	# Find the margin
	margin = marginCalculator.getPixels(original, cut, settings.marginPercentage)
	# Clever hack for putting the cut in an array
	tmp = []
	tmp.append(cut)
	# Get results
	(blobImage, components) = paintingAnalyzer.analyzeCut(original, edgeImage, cut, settings, True)
	lib.drawLines(blobImage, blobImage, tmp)
	lib.drawMargin(blobImage, cut, margin)
	# Return result, what a surprise
	return blobImage


def boundingBoxResult(original, settings, cutNo):
	"""Same as above but will paint the bounding boxes
	painting should be of class Painting
	settings should be of class Settings
	cutNo as int"""
	
	# Get the cut defined by cutNo from the cuts from the first cut ratio in settings
	cut = lib.findMeans(cv.cvGetSize(original), settings.cutRatios[0])[cutNo]

	# Get the BW edge image
	edgeImage = paintingAnalyzer.getEdgeImage(original, settings)

	# Find the margin
	margin = marginCalculator.getPixels(original, cut, settings.marginPercentage)

	tmp = []
	tmp.append(cut)
	components = paintingAnalyzer.analyzeCut(original, edgeImage, cut, settings)
	lib.drawMargin(original, cut, margin)

	# Draw the components
	lib.drawBoundingBoxes(original, components)

	return original


#########################################
# The code below are tests and ugly hacks

class Sets():
	"""Bogus settings class
	Use setattr for setting attributes at will"""
	pass


def main():
	"""
	Just the test
	This method is a god resource on how to handle the results
	"""

	filename = "../../res/local/nicolai.jpg"
	image = highgui.cvLoadImage (filename)

	# XXX: King of hacks
	# We need a class for holding the settings
	# All of this should be in a separate settings class
	cutRatios = [lib.PHI]
	settings = Sets()
	setattr(settings, "lo", 5)
	setattr(settings, "up", 5)
	setattr(settings, "edgeThreshold1", 78)
	setattr(settings, "edgeThreshold2", 2.5 * 78)
	setattr(settings, "cutRatios", cutRatios)
	setattr(settings, "marginPercentage", 0.010)
	image = highgui.cvLoadImage (filename)

	#showBoundingBoxResult(image, settings, 0)
	compareImages(blobResult(image, settings, 0), boundingBoxResult(image, settings, 0), "blob", "bounding box")

if __name__ == "__main__":
	main()
