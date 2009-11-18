#!/usr/bin/env python
#
# Kasper steenstrup

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
#from opencv.cv import *

print "Testing library"
print "Press 'q' to exit"
print ""

filename = sys.argv[1]
if len(sys.argv) == 4:
	lo = int(sys.argv[2])
	up = int(sys.argv[3])
	x = 200
	y = 200
elif len(sys.argv) == 6:
	lo = int(sys.argv[2])
	up = int(sys.argv[3])
	x = int(sys.argv[4])
	y = int(sys.argv[5])
else:
	lo = 6
	up = 6
	x = 200
	y = 200

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

threshold1 = 75;
threshold2 = 2.5 * threshold1;
out = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
edges = cv.cvCreateImage(cv.cvGetSize(image), 8, 1)
#blurImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)
edgeDetector.findBWEdges(image, edges, threshold1, threshold2)

print "Finding the golden means in the picture"

lines = lib.findGoldenMeans(cv.cvGetSize(image))

print "Test plot and line scanner methods"
points = lineScanner.naiveBWLineScanner(edges, lines[0])

out = highgui.cvLoadImage (filename)
#cv.cvSmooth(out, out, cv.CV_BLUR, 3, 3, 0)

print points[:0]
featureDetector.floodFillLine(image, out, points[:0], lines[0], lo, up, {})

#startpoint = lines[0].getPoints()[0]
#points.append(lines[0].getPoints()[1])
#for point in points:
#	out = floofill.floofill(out, lowerThres, upperThres, startpoint, point, 1)
#	startpoint = point
#for point in points:
#	lib.plot(out, point, 2)
#out = edgeDetector.findEdges(out, 70, 70)

winname = "floot"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
