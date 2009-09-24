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
import lib.featureDetector as featureDetector

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

print ""

if len(sys.argv) < 2:
	print "Input error!"
	print "Usage: ./featureDetectorTest.py <filename>"
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

winname = "featureDetectorTest"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

print "Attempt to find features"
points = featureDetector.getGoodFeatures(image)

print "Found %s features" % len(points)

for point in points:
	lib.plot(image, point)

while True:
	highgui.cvShowImage (winname, image)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
