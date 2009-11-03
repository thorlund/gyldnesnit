#!/usr/bin/env python
"""
This collection of methods extract the interesting features from an image
according to different cuts.
"""

import sys

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

import goldenLibrary as lib
import edgeDetector
import featureDetector
import regionSelector
import lineScanner
import marginCalculator
import transformations as transformer


def analyzeCut(original, edgeImage, cut, settings):
	"""Extract the interesting features in the vicinity of a given cut"""
	# Get all data from the settings
	lo = settings.lo
	up = settings.up

	# Set up the margin with respect to the cut
	margin = marginCalculator.getPixels(cv.cvGetSize(original), cut, settings.marginPercentage)
	superMargin = 0
	# ^^ We don't use superMargin

	# Set up constraints
	constraints = regionSelector.Constraints(cv.cvGetSize(original), cut, margin, superMargin, 0.002, 0.25)

	# Create temporary images
	blurImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)
	workImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)

	# Create a blurred copy of the original
	cv.cvSmooth(original, blurImage, cv.CV_BLUR, 3, 3, 0)

	# Superimpose the edges onto the blured image
	cv.cvNot(edgeImage, edgeImage)
	cv.cvCopy(blurImage, workImage, edgeImage)

	# We're done with the blurred image now
	cv.cvReleaseImage(blurImage)

	# Get the edges back to white
	cv.cvNot(edgeImage, edgeImage)

	# Retrive the regions touching the cut
	component_dictionary = featureDetector.ribbonFloodFill(original, edgeImage, workImage, cut, margin, lo, up)

	# Clean up
	cv.cvReleaseImage(workImage)

	# Prune components
	newComponents = regionSelector.pruneRegions(component_dictionary, constraints)

	# Return the dictionary of accepted components
	return newComponents


def analyzeImage(original, settings):
	"""Runs the analysis on all cuts on an image"""
	# Get the thresholds
	edgeThreshold1 = settings.edgeThreshold1
	edgeThreshold2 = settings.edgeThreshold2

	# Create 1-channel image for the egdes
	edgeImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 1)

	# Retrieve BW edges from the original
	# Put the edges in edgeImage
	edgeDetector.findBWEdges(original, edgeImage, edgeThreshold1, edgeThreshold2)

	# Get cuts and place then in a dictionary by cut ratio
	# XXX: Notice the ugly string conversion because python has an issue when
	# converting the ratio to a dictionary index
	cuts = {}
	for ratio in settings.cutRatios:
		cuts[str(ratio)] = lib.findMeans(cv.cvGetSize(original), ratio)

	# New dictionary for holding the resulting components
	# Hold on, now we're putting the result (which is a dictionary)
	# inside a new dict (cutDict). This holds the result for the four cuts
	# for a given ratio. We now put this dict inside the comps-dictionary
	# which then can be used for lookup by the cut-ratio
	comps = {}
	for ratio in cuts:
		cutDict = {}
		for cutNo in range(len(cuts)):
			cutComponents = analyzeCut(original, edgeImage, cuts[ratio][cutNo], settings)
			cutDict[cutNo] = cutComponents
		comps[ratio] = cutDict

	# Clean up
	cv.cvReleaseImage(edgeImage)

	# This is a dictionary in a dictionary in a dictionary
	return comps


def analyze(painting, settings):
	"""Given a picture, of class painting, commence the analysis"""
	original = painting.getImage()
	components = analyzeImage(original, settings)
	return components


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

	# XXX: King of hacks
	# We need a class for holding the settings
	# All of this should be in a separate settings class
	cutRatios = [0.6667, lib.PHI, 0.6]
	settings = Sets()
	setattr(settings, "lo", 5)
	setattr(settings, "up", 5)
	setattr(settings, "edgeThreshold1", 78)
	setattr(settings, "edgeThreshold2", 2.5 * 78)
	setattr(settings, "cutRatios", cutRatios)
	setattr(settings, "marginPercentage", 0.009)

	# Run the analysis with the above settings
	comps = analyzeImage(image, settings)

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
