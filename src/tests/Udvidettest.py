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
import src.lib.naiveMethod as naiveMethod
import src.lib.grid as grid

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
	settings.setMarginPercentage(0.025)
	cutNo = int(sys.argv[2])
	
	cut = lib.findMeans(cv.cvGetSize(image), settings.cutRatios[0])[cutNo]
	# Get the BW edge image
	edgeImage = naiveMethod.getEdgeImage(image, settings)

	(blobImg, comp) = naiveMethod.analyzeCut(image, edgeImage, cut, settings, 'True')
	gridcordinats = grid.gridIt(blobImg, comp)

	#highgui.cvSaveImage('floodfillbilledet.png', blobImg)
	#highgui.cvSaveImage('boindingboxbilledet.png', boxxImg)
	
	showImage(blobImg, 'name')
if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
