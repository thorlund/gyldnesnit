"""
Library for various transformations.
For recerence, see Foley et al, Gomputer Graphics p. 201 ->
Helps perfom matrix multiplications without too much hassle.
"""

from opencv import cv
import numpy

def translatePoint(point, scale):
	"""Translate a cvPoint according to scale"""
	return cv.cvPoint(int(point.x/scale), int(point.y/scale))

def pointToHomogeneousVector(point):
	"""cvPoint to vector representation"""
	a = numpy.array([point.x, point.y, 1])
	a = a.reshape(3, 1)
	return a


def homogeneousVectorToPoint(vector):
	"""Vector to cvPoint representation"""
	x = int(vector[0])
	y = int(vector[1])
	return cv.cvPoint(x, y)


def translateMatrix(p, dx, dy):
	"""Transpose a vector"""
	tM = numpy.zeros( (3, 3) )
	tM = ( [
		(1,  0, dx),
		(0,  1, dy),
		(0,  0,  1)
		] )
	p_pling = numpy.mat(tM)*numpy.mat(p)
	return p_pling


def scalingMatrix(p, sx, sy):
	"""Scale a vector"""
	sM = numpy.zeros( (3, 3) )
	sM = ( [
		(sx,  0,  0),
		(0,  sy,  0),
		(0,   0,  1)
		] )
	p_pling = numpy.mat(sM)*numpy.mat(p)
	return p_pling

def translateBoundingBoxes(component_dictionary, factor):
	"""Translate all bounding boxes in a components
	dictionary according to a factor > 0 and <= 1"""
	if not (0 < factor and factor <= 1):
		raise ValueError("factor must be a number between 0 and 1")
	for component in component_dictionary:
		rect = component.rect
		x = int(rect.x/factor)
		y = int(rect.y/factor)
		w = int(rect.width/factor)
		h = int(rect.height/factor)
		component.rect.x = x
		component.rect.y = y
		component.rect.width = w
		component.rect.height = h


if __name__ == "__main__":
	p1 = cv.cvPoint(2, 2)
	hp = pointToHomogeneousVector(p1)
	p_pling = transposeMatrix(hp, 2, 2)
	print homogeneousVectorToPoint(p_pling)

