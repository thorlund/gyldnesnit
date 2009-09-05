#!/usr/bin/env python
#
# Ulrik Bonde
# Most recent update: Fri 04 Sep 18:20:24 CEST 2009

print "Draw the golden mean on a picture"

import sys
from math import sqrt

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

# Define globals
global PHI
PHI = (sqrt(5) + 1)/2

"""
Returns four line segments ((x, y), (u,v))
where the marking the golden mean
"""
def findMeans(size):
	# First vertical lines (along x-axis)
	x = int(size.width/PHI)

	# The rightmost
	line1_p1 = cv.cvPoint(x, 0)
	line1_p2 = cv.cvPoint(x, size.height)
	
	# The leftmost
	line2_p1 = cv.cvPoint((size.width - x), 0)
	line2_p2 = cv.cvPoint((size.width - x), size.height)

	# Then the horizontal lines (along y-axis)
	y = int(size.height/PHI)

	# The bottommost
	line3_p1 = cv.cvPoint(0, y)
	line3_p2 = cv.cvPoint(size.width, y)

	# The topmost
	line4_p1 = cv.cvPoint(0, (size.height - y))
	line4_p2 = cv.cvPoint(size.width, (size.height - y))
	return [[line1_p1, line1_p2], [line2_p1, line2_p2], [line3_p1, line3_p2], [line4_p1, line4_p2]]

def drawLines(lines, outimage):
	col = cv.CV_RGB(255, 0, 0)
	for line in lines:
		cv.cvLine(outimage, line[0], line[1], col, 1, 8, 0)

if not (len(sys.argv) == 2):
	print "Input err!"
	print "Usage: drawGoldenMean filename"

filename = sys.argv[1]

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	sys.exit(-1)

winname = "Test golden mean"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

lines = findMeans(cv.cvSize(image.width, image.height))
drawLines(lines, image)

highgui.cvShowImage (winname, image)

highgui.cvWaitKey(0)
