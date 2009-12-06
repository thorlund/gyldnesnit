#!/usr/bin/env python
"""
The algorithm for the naive method and some helper methods
"""

import sys

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

import goldenLibrary as lib
import edgeDetector
import featureDetector
import regionSelector
import lineScanner
import marginCalculator
import grid


def getEdgeImage(original, settings):
	"""Helper method for calculating the edge detected image"""
	# Get the thresholds
	edgeThreshold1 = settings.edgeThreshold1
	edgeThreshold2 = settings.edgeThreshold2

	# Create 1-channel image for the egdes
	edgeImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 1)

	# Retrieve BW edges from the original
	# Put the edges in edgeImage
	edgeDetector.findBWEdges(original, edgeImage, edgeThreshold1, edgeThreshold2)
	return edgeImage


def getBlobImage(original, settings, cutNo):
	"""Show the colored blobs in an image at the cut specified
	by cutNo as int. The cut ratio are placed in the settings and only
	the first cut in this ratio-list will be analyzed.
	original should be the image data
	settings should be of class Settings
	cutNo as int"""

	# Get the cut defined by cutNo from the cuts from the first cut ratio in settings
	cut = lib.findMeans(cv.cvGetSize(original), settings.cutRatios[0])[cutNo]

	# Get the BW edge image
	edgeImage = getEdgeImage(original, settings)

	# Find the margin
	margin = marginCalculator.getPixels(original, cut, settings.marginPercentage)

	# Clever hack for putting the cut in an array
	tmp = []
	tmp.append(cut)

	# Get results
	(blobImage, components) = analyzeCut(original, edgeImage, cut, settings, True)
	lib.drawLines(blobImage, blobImage, tmp)
	lib.drawMargin(blobImage, cut, margin)

	# Return result, what a surprise
	return blobImage


def getBoundingBoxImage(original, settings, cutNo, thickness=1, color=None):
	"""Same as above but will paint the bounding boxes
	original should be the image data
	settings should be of class Settings
	cutNo as int
	color as CV_RGB"""

	# Get the cut defined by cutNo from the cuts from the first cut ratio in settings
	cut = lib.findMeans(cv.cvGetSize(original), settings.cutRatios[0])[cutNo]

	# Get the BW edge image
	edgeImage = getEdgeImage(original, settings)

	# Find the margin
	margin = marginCalculator.getPixels(original, cut, settings.marginPercentage)

	tmp = []
	tmp.append(cut)
	components = analyzeCut(original, edgeImage, cut, settings)
	lib.drawMargin(original, cut, margin)

	# Draw the components
	lib.drawBoundingBoxes(original, components, thickness, color)

	return original


### Here begins the algoritms

def analyzeCut(original, edgeImage, cut, settings, showBlobs=False):
	"""Extract the interesting features in the vicinity of a given cut"""
	# Get all data from the settings
	lo = settings.lo
	up = settings.up

	# Set up the margin with respect to the cut
	margin = marginCalculator.getPixels(original, cut, settings.marginPercentage)
	superMargin = 0
	# ^^ We don't use superMargin

	# Set up constraints
	constraints = regionSelector.Constraints(cv.cvGetSize(original), cut, margin, superMargin, 0.002, 0.25)

	# Create temporary images
	blurImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)
	workImage = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)

	# Create a blurred copy of the original
	cv.cvSmooth(original, blurImage, cv.CV_BLUR, 3, 3, 0)

	# Superimpose the edges onto the blured image
	cv.cvNot(edgeImage, edgeImage)
	cv.cvCopy(blurImage, workImage, edgeImage)

	# We're done with the blurred image now
	cv.cvReleaseImage(blurImage)

	# Get the edges back to white
	cv.cvNot(edgeImage, edgeImage)

	# Retrive the regions touching the cut
	component_dictionary = featureDetector.ribbonFloodFill(original, edgeImage, workImage, cut, margin, lo, up)

	# Clean up only if we do not return the image
	if not showBlobs:
		cv.cvReleaseImage(workImage)
	
	#start expanded
	
	# Prune components
	tmpnewComponents = regionSelector.pruneExpandedRegions(component_dictionary, constraints)
	newComponents = regionSelector.pruneExpandedRagionsto(tmpnewComponents, constraints, cut, workImage)
	# Return the dictionary of accepted components or both
	if not showBlobs:
		return newComponents
	else:
		return (workImage, newComponents)


	
def pixelSideCounter(gridPointsList, cut):
	"""
	counts the difrens in pixels at both side og the cut in are blob
	"""
	counter = []
	for ragions in gridPointsList:
		tmp = 0
		left = 0
		right = 0
		for points in ragions:
			if cut > points.x:
				left = left + 1.0
			elif cut < points.x:
				right = right + 1.0
			tmp = tmp + 1.0;
		if (tmp == 0):
			counter.append(1)
		else:
			counter.append((right - left)/tmp)
	return counter		
	
def analyzeImage(original, settings):
	"""Runs the analysis on all cuts on an image"""
	# Get the BW edge image
	edgeImage = getEdgeImage(original, settings)

	# Get cuts and place then in a dictionary by cut ratio
	# XXX: Notice the ugly string conversion because python has an issue when
	# converting the ratio to a dictionary index
	cuts = {}
	for ratio in settings.cutRatios:
		cuts[str(ratio)] = lib.findMeans(cv.cvGetSize(original), ratio)

	# New dictionary for holding the resulting components
	# Hold on, now we're putting the result (which is a dictionary)
	# inside a new dict (cutDict). This holds the result for the four cuts
	# for a given ratio. We now put this dict inside the comps-dictionary
	# which then can be used for lookup by the cut-ratio
	comps = {}
	for ratio in cuts:
		cutDict = {}
		for cutNo in range(len(cuts[ratio])):
			cutComponents = analyzeCut(original, edgeImage, cuts[ratio][cutNo], settings)
			cutDict[cutNo] = cutComponents
		comps[ratio] = cutDict

	# Clean up
	cv.cvReleaseImage(edgeImage)

	# This is a dictionary in a dictionary in a dictionary
	return comps


def analyze(painting, settings):
	"""Given a picture, of class painting, commence the analysis"""
	original = painting.getImage()

	return analyzeImage(original, settings)

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
