#! /usr/bin/env python 

import initTests
initTests.init()

import os
import sys
import lib.goldenLibrary as lib
import lib.featureDetector as featureDetector
import lib.edgeDetector as edgeDetector
import lib.lineScanner as lineScanner
import lib.regionSelector as regionSelector

from opencv import cv
from opencv import highgui


if len(sys.argv) < 2:
	print "give a path and how many images to test on"
	exit(-1)


path = sys.argv[1]
count = sys.argv[2]

images = os.listdir(path)

if len(images) > count:
	print "There isnt enuff images in the dir"
	exit(-1)
images = images[0:int(count)-1]
sumpoints=0
lo = 7
up = 7
threshold1 = 70
threshold2 = 70
margin = 15

for image in images:
	try:
		filename = path+image
		print "working on " + filename
		image = highgui.cvLoadImage(filename)
		out = cv.cvCreateImage(cv.cvGetSize(image), 8, 3)
		edgeDetector.findEdges(image, out, threshold1, threshold2)
		lines = lib.findGoldenMeans(cv.cvGetSize(image))
		cut = lines[0]
		points = lineScanner.naiveLineScanner(out, cut)
		out = highgui.cvLoadImage (filename)
		comp_dict = {}
		featureDetector.floodFillLine(image, out, points, cut, lo, up, comp_dict)
		lib.drawMargin(out, cut, margin)
		constraints = regionSelector.Constraints(cv.cvGetSize(image), cut, margin, 0.002, 0.25)
		points = regionSelector.pruneRegions(comp_dict, constraints)
		print "in image:"+filename+" there was "+str(len(points))+" blobs, that had the potential to be a golden ratio"
		sumpoints = len(points) + sumpoints
print "found "
print sumpoints
print "points in "
print count
print "images"

