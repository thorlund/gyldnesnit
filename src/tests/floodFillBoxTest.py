#!/usr/bin/env python
#
# Ulrik Bonde
# 
# Attention! No *real* checks on the argument vector!

print "" # Just for good meassure
# INIT THE TEST
# THIS SHOULD BE FIRST AS IT WILL MAKE THE LIBRARIES BELLOW AVAILABLE
import initTests
initTests.init()

import sys
import lib.goldenLibrary as lib
import lib.edgeDetector as edgeDetector
import lib.lineScanner as lineScanner
import lib.featureDetector as featureDetector
import lib.regionSelector as regionSelector

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

print "Testing library"
print "Press 'q' to exit"
print ""

filename = sys.argv[1]
if len(sys.argv) == 4:
	lo = int(sys.argv[2])
	up = int(sys.argv[3])
else:
	lo = 7
	up = 7

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

threshold1 = 70;
threshold2 = 70;
out = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
edgeDetector.findEdges(image, out, threshold1, threshold2)

print "Finding the golden means in the picture"

lines = lib.findGoldenMeans(cv.cvGetSize(image))

# Define cut
cut = lines[0]

print "Test plot and line scanner methods"
points = lineScanner.naiveLineScanner(out, image, cut)

out = highgui.cvLoadImage (filename)

(out, components) = featureDetector.floodFillLine(image, out, points, cut, lo, up)

# Set margin
margin = 4

# Draw margin
lib.drawMargin(out, cut, margin)

# Set up constraints
constraints = regionSelector.Constraints(cv.cvGetSize(image), cut, margin, 0.002, 0.25)

# Prune components
newComponents = regionSelector.pruneRegions(components, constraints)

# Draw boxes of selected components
lib.drawBoundingBoxes(out, newComponents)

#lib.drawLines(out)

winname = "Find regions"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
