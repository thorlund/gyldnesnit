#!/usr/bin/env python
#
# Ulrik Bonde

import sys
import goldenLibrary as lib

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

if len(sys.argv) < 2:
	print "Damn you"
	exit(-1)

filename = sys.argv[1]

image = highgui.cvLoadImage (filename)

if not image:
	print "Error loading image '%s'" % filename
	sys.exit(-1)

winname = "Test golden mean"

highgui.cvNamedWindow (winname, highgui.CV_WINDOW_AUTOSIZE)

lines = lib.findMeans(cv.cvSize(image.width, image.height))
lib.drawLines(lines, image)

highgui.cvShowImage (winname, image)

highgui.cvWaitKey(0)
