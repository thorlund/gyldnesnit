"""
Provides a method for finding features
"""

# Import what we need from OpenCV
from opencv import cv

# import goldenLibrary
import lib.goldenLibrary as lib



def floodFillLine(out, points, line, lo, up):
	"""take are golden ratio and make floot fill betvine alle of the points
points are the points on the given line"""
	# Get start and stop points
	(start_point, stop_point) = line.getPoints()
	
	# Set the end point at the end of the line
	points.append(stop_point)
	
	for point in points:
		out = floodFillBetweenPoints(out, lo, up, start_point, point, line)
		start_point = point
	
	return out

# Floodfill the image at point x,y whit are lower and upper thres hold namt lo and up
# Start and stop point is the point that the def runs from to
# golden_ratio is are indekater of whot of the 4 golden ratio we are working in
# 0 and 1 is from the top to the bottom.
# 2 and 3 is from the left to til rigth
def floodFillBetweenPoints(image, lo, up, start_point, stop_point, line):
	"""Floofill the image at point x,y whit are lower and upper thres hold namt lo and up
Start and stop point is the point that the def runs from to"""
	# Get new random color
	color = lib.getRandomColor()

	#Sets the flag
	flags = 4 + (255 << 8) + cv.CV_FLOODFILL_FIXED_RANGE

	#Sets are observer on the blob
	comp = cv.CvConnectedComp()
	
	(p1, p2) = line.getPoints()
	#print cv.cvPoint(p1.x,start_point.y+2)
	
	if p1.x == p2.x:
		# Initialize the seed and set deltas for increasing the seed
		dx = 0
		dy = 1
		seed = cv.cvPoint(start_point.x, start_point.y)
		
		#Color betwine start_point+1 and point-1
		for i in range(start_point.y+1, stop_point.y-1):
			if not(lib.isSameColor(image[i][start_point.x],color)):
				seed = cv.cvPoint(seed.x + dx, seed.y + dy)
				cv.cvFloodFill(image, seed, color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp)# ,flags, None);
			#else:
			#	print i
	else:
		print "Not implemented"
	
	#Diffrent forms of comp print
	if (comp.rect.height> 2000):
		print 'next blob'
		print type(comp.contour)
		print comp.rect.height
		print comp.rect.width
		print comp.rect.x
		print comp.rect.y
	#print "%rect" % comp.rect;
	return image 
	
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
