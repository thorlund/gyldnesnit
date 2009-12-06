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

import lib.goldenLibrary as lib
from src.settings import Settings

# Import available methods
import src.lib.expandedMethod as expandedMethod
import src.lib.grid as grid
import src.lib.marginCalculator as marginCalculator

### Methods for showing images
COL_GREEN = cv.CV_RGB(0, 255, 0)
COL_RED = cv.CV_RGB(255, 0, 0)



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


def centerOfMass(gridPointsList):
	"""
	Canculate the center of mass of alle the regions
	"""
	centerOfMassList = []
	for ragions in gridPointsList:
		tmp = 0
		for points in ragions:
			tmp = tmp + points.x
		if (tmp == 0):
			centerOfMassList.append(0)
		else:
			centerOfMassList.append(tmp/len(ragions))
	return centerOfMassList
	
def pixelSideCounter(gridPointsList, cut):
	"""
	counts the difrens in pixels at both side og the cut in are blob
	"""
	counter = []
	for ragions in gridPointsList:
		tmp = 0
		left = 0
		right = 0
		for points in ragions:
			if cut > points.x:
				left = left + 1.0
			elif cut < points.x:
				right = right + 1.0
			tmp = tmp + 1.0;
		if (tmp == 0):
			counter.append(1)
		else:
			counter.append((right - left)/tmp)
	return counter		
	
def main():
	"""
	Just the test
	This method is a god resource on how to handle the results
	"""

	filename = sys.argv[1]
	image = highgui.cvLoadImage (filename)

	cutRatios = [0.61]
	settings = Settings(cutRatios)
	image = highgui.cvLoadImage (filename)
	thickness = 4
	settings.setMarginPercentage(0.05)
	cutNo = int(sys.argv[2])
	
	#udtrak af cut
	cut = lib.findMeans(cv.cvGetSize(image), settings.cutRatios[0])[cutNo]
	
	# cuttet verdi, dog skal det vi generaliseres lidt
	if cutNo < 3:
		cutPixel = int(0.61 * cv.cvGetSize(image).width)
	else:
		cutPixel = int(0.61 * cv.cvGetSize(image).higth)
	

	
	#Get the BW edge image
	edgeImage = expandedMethod.getEdgeImage(image, settings)

	(blobImg, comp) = expandedMethod.analyzeCut(image, edgeImage, cut, settings, 'True')
	#Liste af liste 
	
	# Find the margin
	margin = marginCalculator.getPixels(image, cut, settings.marginPercentage)

	lib.drawMargin(image, cut, margin)
	
	#Udregning af gridet
	gridPointsList = grid.gridIt(blobImg, comp)
	#hvor mange pixel der er pa den ende side i forhold til den anden, i procent
	
	pixelRatio = pixelSideCounter(gridPointsList, cutPixel)
	
	#Udregning af center og mass
	points = centerOfMass(gridPointsList)
	#Draw the cut
	cv.cvLine(image, cv.cvPoint(cutPixel, 0), cv.cvPoint(cutPixel,600), COL_RED)
	
	#Draw center of mass
	for point in points:
		cv.cvLine(image, cv.cvPoint(point, 0), cv.cvPoint(point,600), COL_GREEN)
	lib.drawBoundingBoxes(image, comp)
	#highgui.cvSaveImage('floodfillbilledet.png', blobImg)
	#highgui.cvSaveImage('boindingboxbilledet.png', boxxImg)
	
	showImage(image, 'name')
if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
