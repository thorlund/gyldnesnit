"""
Provides a method for finding features
"""

# Import what we need from OpenCV
from opencv import cv
import lineScanner
import edgeDetector

# import goldenLibrary
import lib.goldenLibrary as lib

def colorString(color):
	return "%s%s%s" % (int(color[0]), int(color[1]), int(color[2]))

def floodFillLine(original, out, points, line, lo, up, component_dict):
	"""take are golden ratio and make floot fill betvine alle of the points
points are the points on the given line"""
	if not out:
		out = original
	# Get start and stop points
	(start_point, stop_point) = line.getPoints()
	
	# Set the end point at the end of the line
	points.append(stop_point)
	#components = []
	for point in points:
		line = lib.Line(start_point, point)
		floodFillBetweenPoints(out, lo, up, line, component_dict)
		# append in floodfill
		#components.append(component)
		start_point = point

# XXX: Description does not apply
# Floodfill the image at point x,y whit are lower and upper thres hold namt lo and up
# Start and stop point is the point that the def runs from to
# golden_ratio is are indekater of whot of the 4 golden ratio we are working in
# 0 and 1 is from the top to the bottom.
# 2 and 3 is from the left to til rigth
def floodFillBetweenPoints(out, lo, up, line, component_dict):
	"""Floofill the image at point x,y whit are lower and upper thres hold namt lo and up
Start and stop point is the point that the def runs from to"""
	# Get new random color
	#if not colors:
	#	color = lib.getRandomColor()
	#color = lib.getRandomColor()

	#Sets the flag
	flags = 4 + (255 << 8) + cv.CV_FLOODFILL_FIXED_RANGE

	#Sets are observer on the blob
	comp = cv.CvConnectedComp()
	
	(p1, p2) = line.getPoints()
	
	if p1.x == p2.x:
		# Initialize the seed and set deltas for increasing the seed
		dx = 0
		dy = 1
		min = p1.y
		max = p2.y - 1
	elif p1.y == p2.y:
		# Initialize the seed and set deltas for increasing the seed
		dx = 1
		dy = 0
		min = p1.x
		max = p2.x - 1
	else:
		raise lib.OrientationException("Unknown orientation")

	seed = p1

	# Get a new color that is not in the component dictionary
	color = lib.getRandomColor()
	inDict = colorString(color) in component_dict
	while inDict:
		color = lib.getRandomColor(color)
		inDict = colorString(color) in component_dict

	tmp = 0;
	#Color between start_point+1 and point-1
	for i in range(min, max):
		seed = cv.cvPoint(seed.x + dx, seed.y + dy)
		if not (lib.isSameColor(out[seed.y][seed.x], color)):
			tmp = tmp + 1;
			if not (colorString(out[seed.y][seed.x]) in component_dict):
				tmp = tmp - 1;
				cv.cvFloodFill(out, seed, color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp)# ,flags, None);
	
	#print if you need to se have meny pixels that are lept over
	#if not (tmp == 0):
	#	print tmp
	# Color the last pixel again to make sure that the returned component is the entire region
	cv.cvFloodFill(out, seed, color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp)# ,flags, None);

	# Put the results in the component dictionary
	component_dict[colorString(color)] = (color, comp)

def ribbonFloodFill(original, out, cut, margin, lo, up):
	threshold1 = 70;
	threshold2 = 70;
	edges = cv.cvCreateImage(cv.cvGetSize(original), 8, 3)
	edgeDetector.findEdges(original, edges, threshold1, threshold2)
	
	(p1, p2) = cut.getPoints()

	if p1.x == p2.x:
		# Initialize the seed and set deltas for increasing the seed
		dx = 0
		dy = 1
		min = p1.y - margin
		max = p2.y + margin
	elif p1.y == p2.y:
		# Initialize the seed and set deltas for increasing the seed
		dx = 1
		dy = 0
		min = p1.x - margin
		max = p2.x + margin
	else:
		raise lib.OrientationException("Unknown orientation")
	
	component_dict = {}

	for i in range(margin, margin - 1, -1):
		(lower_bound, upper_bound) = lib.getMargins(cut, i)
		lower_points = lineScanner.naiveLineScanner(edges, lower_bound)
		upper_points = lineScanner.naiveLineScanner(edges, upper_bound)

		floodFillLine(original, out, lower_points, lower_bound, lo, up, component_dict)
		floodFillLine(original, out, upper_points, upper_bound, lo, up, component_dict)
	
	points = lineScanner.naiveLineScanner(edges, cut)
	floodFillLine(original, out, points, cut, lo, up, component_dict)
	
	# Here's the result
	#print component_dict
	return component_dict

	
def getGoodFeatures(image):
	# XXX: BETA but working
	# TODO: Clean up!! Comments properly
	# This is mostly copy/paster from /usr/share/opencv/samples/python/lkdemo.py
	"""Find features using OpenCV's cvFindGoodFeatures"""
	win_size = 10 
	MAX_COUNT = 500

	# create the images we need
	grey = cv.cvCreateImage (cv.cvGetSize (image), 8, 1)
	eig = cv.cvCreateImage (cv.cvGetSize (grey), 32, 1)
	temp = cv.cvCreateImage (cv.cvGetSize (grey), 32, 1)

	# Make a b/w copy
	cv.cvCvtColor(image, grey, cv.CV_BGR2GRAY)

	# the default parameters
	quality = 0.01
	min_distance = 10

	# search the good points
	points = cv.cvGoodFeaturesToTrack (
			grey, eig, temp,
			MAX_COUNT,
			quality, min_distance, None, 3, 1, 0.04)

	# refine the corner locations
	cv.cvFindCornerSubPix (
			grey,
			points,
			cv.cvSize (win_size, win_size), cv.cvSize (-1, -1),
			cv.cvTermCriteria (cv.CV_TERMCRIT_ITER | cv.CV_TERMCRIT_EPS,
			20, 0.03))
 
	# release the temporary images for good meassure
	cv.cvReleaseImage (eig)
	cv.cvReleaseImage (temp)
	cv.cvReleaseImage (grey)

	return points
