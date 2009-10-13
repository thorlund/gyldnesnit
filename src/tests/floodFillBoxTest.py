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

def drawBoundingBoxes(components, threshold):
	for comp in components:
		if comp.area > threshold:
			rect = comp.rect
			p1 = cv.cvPoint(rect.x, rect.y)
			p2 = cv.cvPoint(rect.x + rect.width, rect.y + rect.height)
			cv.cvRectangle(out, p1, p2, lib.COL_RED)

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

print "Test plot and line scanner methods"
points = lineScanner.naiveLineScanner(out, image, lines[0])

out = highgui.cvLoadImage (filename)

(out, components) = featureDetector.floodFillLine(image, out, points, lines[0], lo, up)

drawBoundingBoxes(components, 600)

lib.drawLines(out)

winname = "Find regions"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
