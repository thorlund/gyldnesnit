#!/usr/bin/env python
"""
This collection os methods (two, that is) extract the interesting
features from an image with respect to the golden section. It's
possible to specify other cuts that should be analyzed, although
a method for finding cuts other than the golden one, should first
be made in the goldenLibrary.
"""

import lib.goldenLibrary as lib
import lib.edgeDetector as edgeDetector
import lib.featureDetector as featureDetector
import lib.regionSelector as regionSelector
import lib.lineScanner as lineScanner

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui
import sys


## Behold! The Power of Thresholds ##

# Other edges
edgeThreshold1 = 78

# "Inner" edges
edgeThreshold2 = 2.5 * edgeThreshold1

# Agressiveness of flood fill
lo = 5
up = 5

# The margin
margin = 18

## End Thresholds ##

# All of this might even go in the feature detector...?
def analyzeCut(original, edgeImage, cut):
	"""Extract the interesting features respecting the cut"""

	# Set up constraints
	constraints = regionSelector.Constraints(cv.cvGetSize(original), cut, margin, 0.002, 0.25)

	# Create temporary images
	blurImage = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
	workImage = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)

	# Create a blurred copy of the original
	cv.cvSmooth(original, blurImage, cv.CV_BLUR, 3, 3, 0)

	# Superimpose the edges onto the blured image
	cv.cvNot(edgeImage, edgeImage)
	cv.cvCopy(blurImage, workImage, edgeImage)

	# Get the edges back to white
	cv.cvNot(edgeImage, edgeImage)

	# We're done with the blurred image now
	cv.cvReleaseImage(blurImage)

	# Retrive the regions touching the cut
	component_dictionary = featureDetector.ribbonFloodFill(original, edgeImage, workImage, cut, margin, lo, up)

	# Clean up
	cv.cvReleaseImage(workImage)

	# Prune components
	newComponents = regionSelector.pruneRegions(component_dictionary, constraints)

	# Return the dictionary of accepted components
	return newComponents


def analyzeImage(original):
	# Create 1-channel image for the egdes
	edgeImage = cv.cvCreateImage(cv.cvGetSize(image), 8, 1)

	# Retrieve edges
	edgeDetector.findBWEdges(original, edgeImage, edgeThreshold1, edgeThreshold2)

	# Get cuts
	cuts = lib.findGoldenMeans(cv.cvGetSize(original))

	# Run along
	allComponents = []
	for cut in cuts:
		cutComponents = analyzeCut(original, edgeImage, cut)
		allComponents.append(cutComponents)

	# Get the collected component_dictionaries
	for dict in allComponents:
		lib.drawBoundingBoxes(original, dict)

	# Draw the margins
	for cut in cuts:
		lib.drawMargin(original, cut, margin)

	return (original, allComponents)


if __name__ == '__main__':
	print "Hi"
	filename = sys.argv[1]
	image = highgui.cvLoadImage (filename)

	print "Analyze the image"
	analyzeImage(image)

	winname = "Failure"

	highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

	while True:
		highgui.cvShowImage (winname, image)

		c = highgui.cvWaitKey(0)

		if c == 'q':
			print "Exiting ..."
			print ""
			sys.exit(0)
