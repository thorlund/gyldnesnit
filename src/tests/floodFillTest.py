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
import lib.marginCalculator as marginCalculator

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
	lo = 4
	up = 4
	x = 353
	y = 148

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	print ""
	sys.exit(-1)

threshold1 = 75;
threshold2 = 2.5 * threshold1;
out = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
edges = cv.cvCreateImage(cv.cvGetSize(image), 8, 1)
blurImage = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)

edgeDetector.findBWEdges(image, edges, 72, 2.5*72)

#out = cv.cvCreateImage(cv.cvGetSize(image), 8, 1)

#cv.cvCvtColor(image, out, cv.CV_BGR2GRAY)

print "Finding the golden means in the picture"

lines = lib.findGoldenMeans(cv.cvGetSize(image))
#lines = lib.findMeans(cv.cvGetSize(image), lib.PHI)

print "Test plot and line scanner methods"
points = lineScanner.naiveBWLineScanner(edges, lines[0])

#cv.cvSmooth(out, out, cv.CV_MEDIAN, 7, 7, 0)
cv.cvSmooth(image, blurImage, cv.CV_BLUR, 3, 3, 0)
#cv.cvSmooth(out, out, cv.CV_GAUSSIAN, 7, 7, 0)
#out = blurImage

# Superimpose the edges onto the blured image
cv.cvNot(edges, edges)
cv.cvCopy(blurImage, out, edges)

# We're done with the blurred image now
#cv.cvReleaseImage(blurImage)

#print points[:0]
cut = lines[0]
margin = marginCalculator.getPixels(image, cut, 0.024)
component_dictionary = featureDetector.ribbonFloodFill(image, edges, out, cut, margin, lo, up)
#featureDetector.floodFillLine(image, out, points, cut, lo, up, {})
#flags = cv.CV_FLOODFILL_FIXED_RANGE
#flags = 4
color = lib.getRandomColor()
comp = cv.CvConnectedComp()
#cv.cvFloodFill(out, cv.cvPoint(x,y), color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp ,flags)#, None);
#lib.plot(out, cv.cvPoint(x,y), 3, lib.COL_RED)

cv.cvLine(out, cut.p1, cut.p2, lib.COL_RED)
lib.drawMargin(out, cut, margin)

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
highgui.cvSaveImage('out.png', out)

while True:
	highgui.cvShowImage (winname, out)

	c = highgui.cvWaitKey(0)
	
	if c == 'q':
		print "Exiting ..."
		print ""
		sys.exit(0)
