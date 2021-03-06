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
	lo = 4
	up = 4

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

threshold1 = 80;
threshold2 = 2.6 * 70;

# Set up the needed images
out = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
blur = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
edges = cv.cvCreateImage(cv.cvGetSize(image), 8, 1)

# Blur the image
cv.cvSmooth(image, blur, cv.CV_BLUR, 3, 3, 0)

# Find edges in the original image
edgeDetector.findBWEdges(image, edges, threshold1, threshold2)

# Superimpose the edges onto the blured image
cv.cvNot(edges, edges)
cv.cvCopy(blur, out, edges)

# Get the edges back to white
cv.cvNot(edges, edges)

print "Finding the golden means in the picture"

lines = lib.findGoldenMeans(cv.cvGetSize(image))

# Define cut
cut = lines[0]

# Set margin
margin = 15

components = featureDetector.ribbonFloodFill(image, edges, out, cut, margin, lo, up)

# Set up constraints
constraints = regionSelector.Constraints(cv.cvGetSize(image), cut, margin, 0.002, 0.25)

# Prune components
newComponents = regionSelector.pruneRegions(components, constraints)

# Draw boxes of selected components
lib.drawBoundingBoxes(out, newComponents)

# Draw margin
lib.drawMargin(out, cut, margin)

winname = "Find regions"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
