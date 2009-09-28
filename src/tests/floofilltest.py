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
import lib.floofill as floofill
import lib.edgeDetector as edgeDetector
import lib.lineScanner as lineScanner

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui



print "Testing library"
print "Press 'q' to exit"
print ""

filename = sys.argv[1]
if len(sys.argv) == 4:
	lowerThres = int(sys.argv[2])
	upperThres = int(sys.argv[3])
	x = 200
	y = 200
elif len(sys.argv) == 6:
	lowerThres = int(sys.argv[2])
	upperThres = int(sys.argv[3])
	x = int(sys.argv[4])
	y = int(sys.argv[5])
else:
	lowerThres = 8
	upperThres = 8
	x = 200
	y = 200

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)


threshold1 = 70;
threshold2 = 70;
out = edgeDetector.findEdges(image, threshold1, threshold2)


print "Finding the golden means in the picture"
lines = lib.findMeans(cv.cvGetSize(image))


print "Test plot and line scanner methods"
points = lineScanner.naiveLineScanner(out, image, lines[0])

out = highgui.cvLoadImage (filename)

print "Finding region using floofill"
#out = floofill.floofill(image,lowerThres, upperThres,x,y)

for point in points:
	out = floofill.floofill(out,lowerThres, upperThres,point)
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
