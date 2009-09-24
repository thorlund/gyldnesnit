"""Provides functionality for running edge detection on images"""

# Import basic functionality
import goldenLibrary

# Import what we need from OpenCV
from opencv import cv

def findEdges(original, threshold1 = 100, threshold2 = None):
	"""Return a new edge detected image with a specified threshold"""

	#Define threshold2
	if threshold2 == None:
		threshold2 = threshold1 * 3

	# First create the out picture, the one the method will return
	out = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)

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
	# NOTE:	Both images are "not'ed" against each other
	#	meaning that the b/w copy will now be blurred!
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

	# Et voila! The skin comes right off!
	# http://www.youtube.com/watch?v=rUbWjIKxrrs
	return out
