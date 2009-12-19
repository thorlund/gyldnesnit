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
import lib.edgeDetector as edgeDetector

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui


print ""

if len(sys.argv) < 2:
	print "Input error!"
	print "Usage: ./edgeDetectorTest.py <filename> [threshold1] [threshold2]"
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

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

print "Finding edges using Canny"
bwe = cv.cvCreateImage(cv.cvGetSize(image), 8, 1)
out = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
#edgeDetector.findEdges(image, out, threshold1, threshold2)
edgeDetector.findBWEdges(image, bwe, threshold1, threshold2)

#set if you need the image and the Edges togeter
#cv.cvNot(bwe, bwe)

cv.cvCopy(image, out, bwe)

outname = "edgeDetectorTest"
orgname = "Original"
nystr = str(str(threshold1)+'-'+str(threshold2)+'.png')
print nystr
highgui.cvNamedWindow (outname, highgui.CV_WINDOW_AUTOSIZE)
highgui.cvNamedWindow (orgname, highgui.CV_WINDOW_AUTOSIZE)
highgui.cvSaveImage(nystr, out)

while True:
	
	highgui.cvShowImage (orgname, image)
	highgui.cvShowImage (outname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
