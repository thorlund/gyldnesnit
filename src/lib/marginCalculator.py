#!/usr/bin/env python

# Access to other libraries
import sys, os

import math
import goldenLibrary as lib


def getPercentage(cutRatios, min=1):
	"""Given a list of ratios return the minimum allowed percentage
	for the margin. An optional argument for the minimum value can
	be supplied."""

	size = len(cutRatios)

	for i in range(0, size):
		for j in range(0, size):
			if (abs(cutRatios[i] - cutRatios[j]) < min) and not (j == i):
				min = abs(cutRatios[i] - cutRatios[j])
	return (min)/2.0


def getPixels(image, line, marginPercentage):
	(p1, p2) = line.getPoints()
	if p1.x == p2.x:
		# Initialize the seed and set deltas for increasing the seed
		tmp = int(image.width * marginPercentage)
	elif p1.y == p2.y:
		tmp = int(image.height * marginPercentage)
	else:
		raise lib.OrientationException("Unknown orientation")
	return tmp

## Tests


def main():
	# Test
	cuts1 = [2.0/3, 1.0/2, 0.618]
	cuts2 = [2.0/3, 0.618, 1.0/2]
	cuts3 = [1.0/2, 2.0/3, 0.618]
	cuts4 = [1.0/2, 0.618, 2.0/3]
	cuts5 = [0.618, 1.0/2, 2.0/3]
	cuts6 = [0.618, 2.0/3, 1.0/2]

	print getPercentage(cuts1)
	print getPercentage(cuts2)
	print getPercentage(cuts3)
	print getPercentage(cuts4)
	print getPercentage(cuts5)
	print getPercentage(cuts6)


if __name__ == "__main__":
	main()
