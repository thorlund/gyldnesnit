"""
Provides basic operations for image manipulation
"""

from math import sqrt
from opencv import cv
from opencv import highgui
import transformations as transformer
import random

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
	"""This exception is thrown if we do not have a straight line"""
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

class Line():
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
	
	def getLength(self):
		return getDistance(self.p1, self.p2)


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

def findMeans(size, ratio):
	"""Return four cuts with respect to the ratio."""

	if ratio < 0.5:
		ratio = 1 - ratio
		print "Ratio was %s, now its %s" % (1 - ratio, ratio)

	# Check if the 0 < ratio < 1
	# TODO: Find a minimum size for ratio
	# XXX: Obsolete check
	if not (0.5 <= ratio and ratio < 1.0):
		raise ValueError("ratio must be a number between 0.5 and 1.0")

	# Array holding the line segments
	lines = []

	# First vertical lines (along x-axis)
	dx = int(ratio * size.width)

	# The rightmost
	p1 = cv.cvPoint(dx, 0)
	p2 = cv.cvPoint(dx, size.height)
	lines.append(Line(p1, p2))
	
	# The leftmost
	if not ratio == 0.5:
		p1 = cv.cvPoint((size.width - dx), 0)
		p2 = cv.cvPoint((size.width - dx), size.height)
		lines.append(Line(p1, p2))

	# Then the horizontal lines (along y-axis)
	dy = getGoldenSection(size.height)
	dy = int(ratio * size.height)

	# The bottommost
	p1 = cv.cvPoint(0, dy)
	p2 = cv.cvPoint(size.width, dy)
	lines.append(Line(p1, p2))

	# The topmost
	if not ratio == 0.5:
		p1 = cv.cvPoint(0, (size.height - dy))
		p2 = cv.cvPoint(size.width, (size.height - dy))
		lines.append(Line(p1, p2))

	return lines

def findGoldenMeans(size):
	"""Return (four) line segments marking the golden mean"""
	return findMeans(size, PHI)

def getMargins(cut, margin, factor=1):
	lines = []
	if cut.p1.x == cut.p2.x:
		dx = margin
		dy = 0
	elif cut.p1.y == cut.p2.y:
		dx = 0
		dy = margin
	else:
		raise OrientationException("The cut is not straight")
	
	lower_p1 = cv.cvPoint(cut.p1.x - dx, cut.p1.y - dy)
	lower_p2 = cv.cvPoint(cut.p2.x - dx, cut.p2.y - dy)
	lower_p1 = transformer.translatePoint(lower_p1, factor)
	lower_p2 = transformer.translatePoint(lower_p2, factor)
	
	upper_p1 = cv.cvPoint(cut.p1.x + dx, cut.p1.y + dy)
	upper_p2 = cv.cvPoint(cut.p2.x + dx, cut.p2.y + dy)
	upper_p1 = transformer.translatePoint(upper_p1, factor)
	upper_p2 = transformer.translatePoint(upper_p2, factor)

	lines.append(Line(lower_p1, lower_p2))
	lines.append(Line(upper_p1, upper_p2))

	return lines

## Various drawing functions

def plot(image, point, radius=3, color=COL_GREEN):
	"""Plot a point on an image"""
	cv.cvCircle(image, point, radius, color, -1)

def drawLines(original, outimage=None, lines=None, color=COL_RED):
	"""Draw a list of lines on an image.
	If no outimage is supplied, the original is used.
	If no lines are supplied, dafault to drawing the golden section.
	If no color is supplied, use red"""
	if not outimage:
		outimage = original

	if not lines:
		lines = findGoldenMeans(cv.cvGetSize(original))

	for line in lines:
		cv.cvLine(outimage, line.p1, line.p2, color)
	
def drawBoundingBoxes(out, component_dictionary, thickness=1, color=None, factor=1):
	"""Given a dictionary of components, draw its bounding box on the outimage.
	If no color is supplied, the box will be the same color at the blob."""

	# This is a bit hacky, but we need to keep track of the original argument
	inColor = color

	for entry in component_dictionary:
		component = component_dictionary[entry][1]
		rect = component.rect

		if inColor == None:
			color = component_dictionary[entry][0]

		p1 = cv.cvPoint(rect.x, rect.y)
		p2 = cv.cvPoint(rect.x + rect.width, rect.y + rect.height)
		p1 = transformer.translatePoint(p1, factor)
		p2 = transformer.translatePoint(p2, factor)
		cv.cvRectangle(out, p1, p2, color, thickness)

def drawMargin(out, cut, margin, factor=1):
	lines = getMargins(cut, margin, factor)
	drawLines(out, None, lines, COL_BLUE)


## Various common checks

def getRandomColor(color=None):
	"""Get a random color. Is a color is supplied,
	the returned color will be different from that"""
	b = random.randint(0,255)
	g = random.randint(0,255)
	r = random.randint(0,255)

	newColor = cv.CV_RGB(r, g, b)
	
	if color:
		print "Get different color"
		flag = isSameColor(newColor, color)
		while flag:
			b = random.randint(0,255)
			g = random.randint(0,255)
			r = random.randint(0,255)
			newColor = cv.CV_RGB(r, g, b)
			flag = isSameColor(newColor, color)
	return newColor

def getDistance(p1, p2):
	return sqrt(pow((p2.x - p1.x), 2) + pow((p2.y - p1.y), 2))

# TODO: Check if there are any methods in OpenCV the two following
def isSamePoint(p1, p2):
	"""Checks whether two points have the same coordinates"""
	return (p1.x == p2.x) and (p1.y == p2.y)

def isSameColor(c1, c2):
	"""Checks whether two colors are the same"""
	return (c1[0] == c2[0]) and (c1[1] == c2[1]) and (c1[2] == c2[2])

