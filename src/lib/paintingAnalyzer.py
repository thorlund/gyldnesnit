#!/usr/bin/env python
"""
This collection of methods extract the interesting features from an image
according to different cuts.
"""

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

# Access to other libraries
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

from src.settings import Settings

import goldenLibrary as lib

# Import methods
import naiveMethod


def analyze(painting, settings):
	"""Given a picture, of class painting, commence the analysis"""
	original = painting.getImage()
	method = settings.method

	if method == "naive":
		return naiveMethod.analyzeImage(original, settings)
	else:
		raise StandardError("No method named %s" % method)


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

	filename = sys.argv[1]
	image = highgui.cvLoadImage (filename)

	print "DO NOT EXPECT THE RUNNING TIME OF THIS TEST TO BE REPRESENTATIVE!"
	print ""
	print "THRESHOLDS AND EVERYTHING ELSE ARE HARDCODED!"

	cutRatios = [0.6667, lib.PHI, 0.6]
	settings = Settings(cutRatios)

	# Run the analysis with the above settings
	comps = naiveMethod.analyzeImage(image, settings)

	# This is just for drawing the results
	# The below methods can probably be combined but don't bother
	# {{{
	# Get and draw the cuts
	cuts = {}
	for ratio in settings.cutRatios:
		cuts[str(ratio)] = lib.findMeans(cv.cvGetSize(image), ratio)

	for ratio in cuts:
		lib.drawLines(image, None, cuts[ratio], lib.getRandomColor())

	# Get and draw the components
	for ratio in comps:
		for cut in comps[ratio]:
			lib.drawBoundingBoxes(image, comps[ratio][cut])
	# }}}

	winname = "Failure"

	highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

	while True:
		highgui.cvShowImage (winname, image)

		c = highgui.cvWaitKey(0)

		if c == 'q':
			print "Exiting ..."
			print ""
			sys.exit(0)


if __name__ == '__main__':
	main()
