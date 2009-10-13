#!/usr/bin/env python
#
# Ulrik Bonde
# 
# Attention! No *real* checks on the argument vector!
#
#
# Purpose of test:
#	Does the region findind function do a lot of unescessary work?
#	It seems like floodfill will always color the same amount of pixels
#	no matter what.
#
#

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

cut = lines[0]

print "Test plot and line scanner methods"
points = lineScanner.naiveLineScanner(out, image, cut)

out = highgui.cvLoadImage (filename)

(out, components) = featureDetector.floodFillLine(image, out, points, cut, lo, up)

print components[0].area

# Test
comp = cv.CvConnectedComp()
seed = cv.cvPoint(200, 20)
cv.cvFloodFill(image, seed, lib.COL_RED, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp)# ,flags, None);
print comp.area

lib.drawBoundingBoxes(out, components, 600)

#lib.drawLines(out)

winname1 = "Find regions"
winname2 = "original"

highgui.cvNamedWindow (winname1, highgui.CV_WINDOW_AUTOSIZE)
highgui.cvNamedWindow (winname2, highgui.CV_WINDOW_AUTOSIZE)

while True:
	highgui.cvShowImage (winname1, out)
	highgui.cvShowImage (winname2, image)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
