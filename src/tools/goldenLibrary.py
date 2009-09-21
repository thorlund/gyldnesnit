"""
Provides a collection of tools for image manipulation
"""

from math import sqrt
from opencv import cv
from opencv import highgui

# Define globals
global phi, PHI
phi = (sqrt(5) + 1)/2
PHI = phi - 1

# Define basic colors
COL_BLACK = cv.CV_RGB(0, 0, 0)
COL_WHITE = cv.CV_RGB(255, 255, 255)
COL_RED = cv.CV_RGB(255, 0, 0)
COL_GREEN = cv.CV_RGB(0, 255, 0)
COL_BLUE = cv.CV_RGB(0, 0, 255)

class OrientationException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)

def getIntersection(x1, x2, x3, x4, y1, y2, y3, y4):
	"""Helper method for calculating the intersection of two line segments"""
	px = (((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)))
	py = (((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)))

	return cv.cvPoint(px, py)

def getGoldenSection(length):
	"""Get the golden section for a line segment from 0 to the argument"""
	return int(length * PHI)
	
class line():
	"""A container for a line segment."""
	def __init__(self, p1, p2):
		"""Create a line segement of two cvPoint types"""
		self.p1 = p1
		self.p2 = p2

	def intersection(self, line):
		"""Returns the intersection of this line and another as a cvPoint"""
		return intersection(self, line)

	def getPoints(self):
		"""Returns a two-tuple with the end points of the line"""
		return (self.p1, self.p2)

def plot(image, point, radius=3, color=COL_GREEN):
	"""Plot a point on an image"""
	cv.cvCircle(image, point, radius, color, -1)

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

	return getIntersection(x1, x2, x3, x4, y1, y2, y3, y4)

def findMeans(size):
	"""Return (four) line segments marking the golden mean"""
	
	# Array holding the line segments
	lines = []

	# First vertical lines (along x-axis)
	dx = getGoldenSection(size.width)

	# The rightmost
	p1 = cv.cvPoint(dx, 0)
	p2 = cv.cvPoint(dx, size.height)
	lines.append(line(p1, p2))
	
	# The leftmost
	p1 = cv.cvPoint((size.width - dx), 0)
	p2 = cv.cvPoint((size.width - dx), size.height)
	lines.append(line(p1, p2))

	# Then the horizontal lines (along y-axis)
	dy = getGoldenSection(size.height)

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
	for line in lines:
		cv.cvLine(outimage, line.p1, line.p2, COL_RED)

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

def isSamePoint(p1, p2):
	"""Checks whether two points have the same coordinates"""
	return (p1.x == p2.x) and (p1.y == p2.y)

def isSameColor(c1, c2):
	"""Checks whether two colors are the same"""
	return (c1[0] == c2[0]) and (c1[1] == c2[1]) and (c1[2] == c2[2])

def scanLine(edgeImage, origImage, line, margin):
	"""Scan for edges along a line in a edge-detected image

This is _very_ naive
Traverse a line, put a dot if the pixel is white
The margin is a padding on each side of the input line

Example:
In an array [1 2 3 4 5]
            [1. ......]
	    ..........

we want the column at 3 with margin 1.
This will get the columns at 2 3 and 4.
"""
	# Get the points from the line
	(p1, p2) = line.getPoints()

	# We check the direction of the line and pull out
	# the appropriate row or column
	if p1.y == p2.y:
		# Get the row, defined by y
		# We then want y - margin and y + margin
		print "horizontal"
		if margin > 0:
			slice = edgeImage[p1.y - margin:p1.y + margin]
		else:
			slice = edgeImage[p1.y]
	elif p1.x == p2.x:
		# Get the column, defined by x
		# We want x - margin and x + margin
		print "vertical"
		if margin > 0:
			slice = edgeImage[:,p1.x - margin:p1.x + margin]
		else:
			slice = edgeImage[:,p1.x:p1.x]
	else:
		raise OrientationException("The orientation is fucked up")

	# Now we can traverse every point in the row/column
	# We have to check for the margin again
	if margin > 0:
		for x in range(slice.width + 1):		# adjust for something
			for y in range(slice.height + 1):	# adjust again
				# Do something
				print "%s, %s" % (x, y)
			
	else:
		for point in slice:
			thisColor = cv.CV_RGB(int(point[0]), int(point[1]), int(point[2])) 
			if not isSameColor(COL_BLACK, thisColor):
				# Do something a bit more sophisticated
				print point
