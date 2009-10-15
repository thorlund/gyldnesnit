"""
Provides a method for finding features
"""

# Import what we need from OpenCV
from opencv import cv

# import goldenLibrary
import lib.goldenLibrary as lib

# Missing functions for differentiating grid points

def gridIt(image, component_dictionary, step=2):
	print len(component_dictionary)
	gridcordinates = []
	for entry in component_dictionary:
		color = component_dictionary[entry][0]
		print color
		print entry
		component = component_dictionary[entry][1]
		points = 0

		rect = component.rect
		lower_x = rect.x
		lower_y = rect.y
		upper_x = lower_x + rect.width
		upper_y = lower_y + rect.height

		for i in range(lower_x, upper_x, step):
			for j in range(lower_y, upper_y, step):
				if lib.isSameColor(color, image[j][i]):
					points = points + 1
					gridcordinates.append(cv.cvPoint(i, j))
		print points

	return gridcordinates
