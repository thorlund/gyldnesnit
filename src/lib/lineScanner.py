"""
Provides (a) method(s) for scanning a line for crossing edges
"""

# Import basic functionality
import goldenLibrary as lib

# Import what we need from OpenCV
from opencv import cv

def naiveLineScanner(edgeImage, line):
	"""Scan for edges along a line in a edge-detected image
	This is _very_ naive
	Traverse a line, put the coordinate in a list if the pixel is white
"""
	# Get the points from the line
	(p1, p2) = line.getPoints()

	# We check the direction of the line then
	# get the appropriate row or column.
	# XXX: Any smarter way around this problem??
	if p1.y == p2.y:
		# Get the row, defined by y
		dx = 1
		dy = 0
		slice = edgeImage[p1.y]
	elif p1.x == p2.x:
		# Get the column, defined by x
		dx = 0
		dy = 1
		slice = edgeImage[:,p1.x]
	else:
		raise lib.OrientationException("The orientation is fucked up")

	p = p1
	points = []
	# Now we can traverse every point in the row/column
	for point in slice:
		thisColor = cv.CV_RGB(int(point[0]), int(point[1]), int(point[2]))
		if not lib.isSameColor(lib.COL_BLACK, thisColor):
			# Save this point
			points.append(p)
		# Update the coordinate
		p = (cv.cvPoint(p.x + dx, p.y + dy))

	return points

def naiveBWLineScanner(edgeImageBW, line):
	"""B/W version of the naiveLineScanner"""
	# Get the points from the line
	(p1, p2) = line.getPoints()

	# We check the direction of the line then
	# get the appropriate row or column.
	# XXX: Any smarter way around this problem??
	if p1.y == p2.y:
		# Get the row, defined by y
		dx = 1
		dy = 0
		slice = edgeImageBW[p1.y]
	elif p1.x == p2.x:
		# Get the column, defined by x
		dx = 0
		dy = 1
		slice = edgeImageBW[:,p1.x]
	else:
		raise lib.OrientationException("The orientation is fucked up")

	p = p1
	points = []
	# Now we can traverse every point in the row/column
	for point in slice:
		if not int(point) == 0:
			# Save this point
			points.append(p)
		# Update the coordinate
		p = (cv.cvPoint(p.x + dx, p.y + dy))

	return points
