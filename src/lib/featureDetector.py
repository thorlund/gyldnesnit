"""
Provides a method for finding features
"""

# Import what we need from OpenCV
from opencv import cv

# import random
import random

# import goldenLibrary
import lib.goldenLibrary as lib



def floodFillLine(out, points, line, lo, up):
	"""take are golden ratio and make floot fill betvine alle of the points
points are the points on the given line"""
	#Set the starting point at the start of the line
	startpoint = line.getPoints()[0]
	
	#Set the ending point at the ending af the line
	points.append(line.getPoints()[1])
	
	for point in points:
		out = floodFillBetweenPoints(out, lo, up, startpoint, point, line)
		startpoint = point
		
	for point in points:
		lib.plot(out, point, 2)
	
	return out

# Floofill the image at point x,y whit are lower and upper thres hold namt lo and up
# Start and stop point is the point that the def runs from to
# golden_ratio is are indekater of whot of the 4 golden ratio we are working in
# 0 and 1 is from the top to the bottom.
# 2 and 3 is from the left to til rigth
def floodFillBetweenPoints(image, lo, up, start_point, stop_point, line):
	"""Floofill the image at point x,y whit are lower and upper thres hold namt lo and up
Start and stop point is the point that the def runs from to"""		
	# the color of the blob
	b = random.randint(0,255)
	g = random.randint(0,255)
	r = random.randint(0,255)
	color = cv.CV_RGB(r,g,b);
	
	#Sets the flag
	flags = 4 + (255 << 8) + cv.CV_FLOODFILL_FIXED_RANGE

	#Sets are observer on the blob
	comp = cv.CvConnectedComp()
	
	(p1, p2) = line.getPoints()
	if p1.x == p2.x:
		#Set the seed to the start of the golden ratio 
		seed = cv.cvPoint(start_point.x,start_point.y+1)
		
		#Color betwine start_point+1 and point-1  
		for i in range(start_point.y+1, stop_point.y-1):
			cv.cvFloodFill(image, seed, color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp)# ,flags, None);
			seed = cv.cvPoint(seed.x,seed.y+1)
	else:
		#Set the seed to the start of the golden ratio 
		seed = cv.cvPoint(start_point.x+1,start_point.y)
		
		#Color betwine start_point+1 and point-1  
		for i in range(start_point.x+1, stop_point.x-1):
			cv.cvFloodFill(image, seed, color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up),comp)# ,flags, None);
			seed = cv.cvPoint(seed.x+1,seed.y)
	
	#Diffrent forms of comp print
	#print "%g pixels were repainted" % comp.area;
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
