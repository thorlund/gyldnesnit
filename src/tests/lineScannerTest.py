#!/usr/bin/env python
#
# Ulrik Bonde

import sys
import lib.goldenLibrary as lib
import lib.edgeDetector as edgeDetector
import lib.lineScanner as lineScanner
import initTests

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

# INIT THE TEST
initTests.init()

print ""

if len(sys.argv) < 2:
	print "Input error!"
	print "Usage: ./testLibrary.py <filename> [threshold1] [threshold2]"
	print "The above means that you have to supply a path to an image"
	print ""
	exit(-1)

print "Testing library"
print "Press 'q' to exit"
print ""

filename = sys.argv[1]

threshold2 = None

if len(sys.argv) == 3:
	threshold1 = int(sys.argv[2])
elif len(sys.argv) == 4:
	threshold1 = int(sys.argv[2])
	threshold2 = int(sys.argv[3])
else:
	threshold1 = 100

image = highgui.cvLoadImage (filename)
out = edgeDetector.findEdges(image, threshold1, threshold2)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

winname = "Test golden mean"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

print "Finding the golden means in the picture"
lines = lib.findMeans(cv.cvGetSize(image))


print "Drawing the means"
#lib.drawLines(lines, out)

print "Test plot function and intersection function"
#lib.plot(out, lines[0].intersection(lines[2]))
points = lineScanner.naiveLineScanner(out, image, lines[0])

for point in points:
	lib.plot(out, point, 2)
#lib.plot(out, lib.intersection(lines[1], lines[3]), color=lib.COL_BLUE)

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
