"""
Provides functionality for running edge detection on images
"""

# Import basic functionality
import goldenLibrary
import warnings

# Import what we need from OpenCV
from opencv import cv

def findBWEdges(original, out, threshold1, threshold2):
	"""Identical with findEdges except that this returns white edges
	on a black background. We really don't need colored edges any longer.
	This also makes it easy to to a manual merge of edge and blur picture."""
	if threshold2 == None:
		threshold2 = threshold1 * 3

	gray = cv.cvCreateImage(cv.cvGetSize(original), 8, 1)

	cv.cvCvtColor(original, gray, cv.CV_BGR2GRAY)

	cv.cvSmooth(gray, out, cv.CV_BLUR, 3, 3, 0)

	cv.cvNot(gray, out)

	cv.cvCanny(gray, out, threshold1, threshold2)

	return out

def findEdges(original, out, threshold1 = 100, threshold2 = None):
	"""Return a new edge detected image with a specified threshold"""
	warnings.warn("Use findBWEdges instead unless you really need colored edges.", DeprecationWarning)

	#Define threshold2
	if threshold2 == None:
		threshold2 = threshold1 * 3

	# Create two pictures with only one channel for a b/w copy
	# and one for storring the edges found in the b/w picture
	gray = cv.cvCreateImage(cv.cvGetSize(original), 8, 1)
	edge = cv.cvCreateImage(cv.cvGetSize(original), 8, 1)

	# Create the b/w copy of the original
	cv.cvCvtColor(original, gray, cv.CV_BGR2GRAY)

	# Blur the b/w copy, but put the result into edge pic
	cv.cvSmooth(gray, edge, cv.CV_BLUR, 3, 3, 0)

	# Negate the b/w copy of original with newly blurred
	# b/w copy. This will make egdes stand out
	cv.cvNot(gray, edge)

	# Run an edge-finding algorithm called 'Canny'
	# It will analyse the first argument and store the
	# resulting picture in the second argument
	cv.cvCanny(gray, edge, threshold1, threshold2)

	# We initialize our out-image to black
	cv.cvSetZero(out)

	# Finally, we use the found edges, which are b/w, as
	# a mask for copying the colored edges from the original
	# to the out-image
	cv.cvCopy(original, out, edge)

	# The edge-detected image is now in out
