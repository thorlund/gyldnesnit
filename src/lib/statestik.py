# Import what we need from OpenCV
from opencv import cv

# import goldenLibrary
import lib.goldenLibrary as lib
	
def splitOpBlob(floodFillImage, copy, points, line):
"""
Flood fill on bots side of are line, and return the 2 areas
"""
	comp = cv.CvConnectedComp()
	# Get start and stop points
	sizeSplitBlobs = []
	(start_point, stop_point) = line.getPoints()
	for point in points:
		# Get new random color
		color = lib.getRandomColor()
		if (start_point.x == stop_point.x):
			slice1 = floodFillImage[:,0:start_point.x+1]
			cv.cvFloodFill(slice1, cv.cvPoint(start_point.x, start_point.y+1), color, cv.CV_RGB(2,2,2), cv.CV_RGB(2,2,2),comp)
			#removes blobs that have are area under 3
			if (comp.area > 2):
				sizeSplitBlobs.append(comp.area)
				slice2 = copy[:,start_point.x:]
				cv.cvFloodFill(slice2, cv.cvPoint(0, start_point.y+1), color, cv.CV_RGB(2,2,2), cv.CV_RGB(2,2,2),comp)
				sizeSplitBlobs.append(comp.area)
			start_point = point
	return sizeSplitBlobs
