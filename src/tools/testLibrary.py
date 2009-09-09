#!/usr/bin/env python
#
# Ulrik Bonde

import sys
import goldenLibrary as lib

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

print ""

if len(sys.argv) < 2:
	print "Input error!"
	print "Usage: ./testLibrary.py <filename> [threshold]"
	print "The above means that you have to supply a path to an image"
	print ""
	exit(-1)

print "Testing library"
print "Press 'q' to exit"
print ""

filename = sys.argv[1]

if len(sys.argv) == 3:
	threshold = int(sys.argv[2])
else:
	threshold = 100

image = highgui.cvLoadImage (filename)
out = lib.findEdges(image, threshold)

if not image:
	print "Error loading image '%s'" % filename
	print ""
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
		print ""
		sys.exit(0)