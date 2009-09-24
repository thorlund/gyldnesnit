"""
Provides a method for scanning a line for crossing edges
"""

from math import sqrt
from opencv import cv
from opencv import highgui
def naiveLineScanner(edgeImage, origImage, line):
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
		print "horizontal"
		dx = 1
		dy = 0
		slice = edgeImage[p1.y]
	elif p1.x == p2.x:
		# Get the column, defined by x
		print "vertical"
		dx = 0
		dy = 1
		slice = edgeImage[:,p1.x]
	else:
		raise OrientationException("The orientation is fucked up")

	p = p1
	points = []
	# Now we can traverse every point in the row/column
	for point in slice:
		thisColor = cv.CV_RGB(int(point[0]), int(point[1]), int(point[2]))
		if not isSameColor(COL_BLACK, thisColor):
			# Save this point
			points.append(p)
		# Update the coordinate
		p = (cv.cvPoint(p.x + dx, p.y + dy))

	return points

