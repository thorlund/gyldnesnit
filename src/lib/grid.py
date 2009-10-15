"""
Provides a method for finding features
"""

# Import what we need from OpenCV
from opencv import cv

# import goldenLibrary
import lib.goldenLibrary as lib

def gridIt(image,blobs,distance=2):
	for blob in blobs:
		color = blob[1]
		blob = blob[0]
		points=0
		gridcordinates = []
		mostx = blob.rect.x
		x = mostx
		leastx = mostx-blob.rect.height
		mosty = blob.rect.y
		y = mosty
		leasty = mosty - blob.rect.height
		while(x >= leastx):
			while(y >= leasty):
				if color == image[x][y]:
					points = points +1
					gridcordinates.add((x,y))
				y = y-distance
			x = x-distance

		print points
