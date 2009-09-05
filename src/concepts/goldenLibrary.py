# Collection of methods for image manipulation 
#
# Ulrik Bonde

from math import sqrt

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui

# Define globals
global PHI
PHI = (sqrt(5) + 1)/2

"""
A container for a line segment.
Contains two cvPoints indicating the segment
"""
class line():
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

"""
Returns four line segments ((x, y), (u,v))
where the marking the golden mean
"""
def findMeans(size):
	lines = []
	# First vertical lines (along x-axis)
	dx = int(size.width/PHI)

	# The rightmost
	p1 = cv.cvPoint(dx, 0)
	p2 = cv.cvPoint(dx, size.height)
	lines.append(line(p1, p2))
	
	# The leftmost
	p1 = cv.cvPoint((size.width - dx), 0)
	p2 = cv.cvPoint((size.width - dx), size.height)
	lines.append(line(p1, p2))

	# Then the horizontal lines (along y-axis)
	dy = int(size.height/PHI)

	# The bottommost
	p1 = cv.cvPoint(0, dy)
	p2 = cv.cvPoint(size.width, dy)
	lines.append(line(p1, p2))

	# The topmost
	p1 = cv.cvPoint(0, (size.height - dy))
	p2 = cv.cvPoint(size.width, (size.height - dy))
	lines.append(line(p1, p2))
	return lines

"""
Draw a list of lines
"""
def drawLines(lines, outimage):
	col = cv.CV_RGB(255, 0, 0)
	for line in lines:
		cv.cvLine(outimage, line.p1, line.p2, col, 1, 8, 0)
