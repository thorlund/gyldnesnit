#!/usr/bin/env python
#
# Ulrik Bonde

import sys
import goldenLibrary as lib

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

print "Testing library"
print "Press 'q' to exit"
print ""

if len(sys.argv) < 2:
	print "Damn you"
	exit(-1)

filename = sys.argv[1]

image = highgui.cvLoadImage (filename)
out = lib.findEdges(image)

if not image:
	print "Error loading image '%s'" % filename
	sys.exit(-1)

winname = "Test golden mean"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

print "Finding the golden means in the picture"
lines = lib.findMeans(cv.cvGetSize(image))

print "Drawing the means"
lib.drawLines(lines, out)

print lines[0].intersection(lines[2])

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		sys.exit(0)
