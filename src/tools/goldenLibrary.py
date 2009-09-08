"""
Provides a collection of tools for image manipulation
"""

from math import sqrt
from opencv import cv
from opencv import highgui

# Define globals
global PHI
PHI = (sqrt(5) + 1)/2

def __getintersection__(x1, x2, x3, x4, y1, y2, y3, y4):
	"""Helper method for calculating the intersection of two line segments"""
	px = (((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)))
	py = (((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)))

	return cv.cvPoint(px, py)
	
class line():
	"""A container for a line segment."""
	def __init__(self, p1, p2):
		"""Create a line segement.
		p1 and p1 must be of type cvPoint"""
		self.p1 = p1
		self.p2 = p2

	def intersection(self, line):
		"""Returns the intersection of this line and another"""
		return intersection(self, line)

def intersection(line1, line2):
	"""Get the intersection of two lines as a cvPoint"""
	x1 = line1.p1.x
	y1 = line1.p1.y

	x2 = line1.p2.x
	y2 = line1.p2.y

	x3 = line2.p1.x
	y3 = line2.p1.y

	x4 = line2.p2.x
	y4 = line2.p2.y

	return __getintersection__(x1, x2, x3, x4, y1, y2, y3, y4)

def findMeans(size):
	"""Return (four) line segments marking the golden mean"""
	
	# Array holding the line segments
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

def drawLines(lines, outimage):
	"""Draw a list of lines on an image"""
	col = cv.CV_RGB(255, 0, 0)
	for line in lines:
		cv.cvLine(outimage, line.p1, line.p2, col, 1, 8, 0)

def findEdges(original, threshold = 100):
	"""Return a new edge detected image with a specified threshold"""
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
	cv.cvCanny(gray, edge, threshold, threshold * 3, 3)

	# We initialize our out-image to black
	cv.cvSetZero(out)

	# Finally, we use the found edges, which are b/w, as
	# a mask for copying the colored edges from the original
	# to the out-image
	cv.cvCopy(original, out, edge)

	# Et voila! The skin comes right off!
	# http://www.youtube.com/watch?v=rUbWjIKxrrs
	return out

