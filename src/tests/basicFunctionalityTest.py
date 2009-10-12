#!/usr/bin/env python
#
# Ulrik Bonde

print "" # Just for good meassure
# INIT THE TEST
# THIS SHOULD BE FIRST AS IT WILL MAKE THE LIBRARIES BELLOW AVAILABLE
import initTests
initTests.init()

import sys
import lib.goldenLibrary as lib

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

print ""

if len(sys.argv) < 2:
	print "Input error!"
	print "Usage: ./basicFunctionalityTest.py <filename>"
	print "The above means that you have to supply a path to an image"
	print ""
	exit(-1)

print "Testing library"
print "Press 'q' to exit"
print ""

filename = sys.argv[1]

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

winname = "basicFunctionalityTest"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

print "Finding the golden means in the picture"
lines = lib.findGoldenMeans(cv.cvGetSize(image))

print "Drawing the means"
lib.drawLines(image)

print "Test plot function and intersection function"
lib.plot(image, lines[0].intersection(lines[2]))
lib.plot(image, lib.intersection(lines[1], lines[3]), color=lib.COL_BLUE)

while True:
	highgui.cvShowImage (winname, image)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
