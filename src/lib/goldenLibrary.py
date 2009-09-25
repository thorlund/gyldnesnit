"""
Provides basic operations for image manipulation
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

# TODO: Check if there are any methods in OpenCV the two following
def isSamePoint(p1, p2):
	"""Checks whether two points have the same coordinates"""
	return (p1.x == p2.x) and (p1.y == p2.y)

def isSameColor(c1, c2):
	"""Checks whether two colors are the same"""
	return (c1[0] == c2[0]) and (c1[1] == c2[1]) and (c1[2] == c2[2])