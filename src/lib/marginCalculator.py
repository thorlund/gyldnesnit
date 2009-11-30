#!/usr/bin/env python

# Access to other libraries
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import math
from src.settings import Settings
import goldenLibrary as lib


def getPercentage(Rlist):
	"""Given a list of ratios return the minimum allowed percentage
	for the margin"""
	size = len(Rlist)
	#the max magin that the function can return
	tmp = 1
	if size == 1:
		return None

	for i in range(0, size):
		for j in range(0, size):
			if (abs(Rlist[i] - Rlist[j]) < tmp) and not (j == i):
				tmp = abs(Rlist[i] - Rlist[j])
	return (tmp)/2.0


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
