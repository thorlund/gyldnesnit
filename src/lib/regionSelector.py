"""
Provides methods for pruning a set of regions
"""

import goldenLibrary as lib

class Constraints:
	"""Holds a set of constraints for an image when finding regions at a cut"""
	coordinate = None
	lower_bound = None
	upper_bound = None
	rect = None
	size = None
	mass = None
	def __init__(self, imagesize, cut, margin, sizePercentage=0.002, massPercentage=0.15):
		"""Calculate all the constraints, i.e. the accepting
		rectangle (margin), the minimum size relative to the
		image and the minimum mass relative to the image.
		This class then functions as a quick lookup for those
		otherwise relatively demanding calulations.
		
		Arguments:
			imagesize = size of image as cvSize
			cut = the section we are inspecting as Line
			margin = floor(width of margin/2) as int
			sizePercentage = min % of pixels required for size of region as decimal
			massPercentage = min % of pixels required for mass of region as decimal
		"""
		if not (0 <= sizePercentage and sizePercentage <= 1):
			raise ValueError("sizePercentage must be a number between 0 and 1")

		if not (0 <= massPercentage and massPercentage <= 1):
			raise ValueError("sizePercentage must be a number between 0 and 1")

		if not margin >= 0:
			raise ValueError("margin must be >= 0")

		totalPixels = imagesize.height * imagesize.width
		self.size = sizePercentage * totalPixels
		self.mass = massPercentage

		if cut.p1.x == cut.p2.x:
			self.coordinate = 0
			self.lower_bound = cut.p1.x - margin
			self.upper_bound = cut.p1.x + margin
		elif cut.p1.y == cut.p2.y:
			self.coordinate = 1
			self.lower_bound = cut.p1.y - margin
			self.upper_bound = cut.p1.y + margin
		else:
			raise lib.OrientationException("The cut is not straight")


def checkPosition(component, constraints):
	"""Test if the component have a bounding box inside the accepting
	rectangle defined in the constraints."""
	d = component.rect.width
	p = component.rect.x
	if constraints.coordinate:
		d = component.rect.height
		p = component.rect.y

	return (constraints.lower_bound <= p) or (p + d <= constraints.upper_bound)

def checkSize(component, constraints):
	"""Test if the component have size greater than the minumum size
	defined by the constraints."""
	return component.area >= constraints.size

def checkMass(component, constraints):
	"""Check if the component have mass greater than the minimum mass
	defined by the contraints."""
	rect = component.rect
	mass = component.area/(rect.width * rect.height)
	return mass >= constraints.mass

def pruneRegions(component_dictionary, contraints):
	"""Run all required test on a dictionary of regions with the given set
	of contraints. The output is a pruned components_dictionary."""
	acceptedRegions = {}
	for entry in component_dictionary:
		component = component_dictionary[entry][1]
		if checkSize(component, contraints) and checkPosition(component, contraints) and checkMass(component, contraints):
			acceptedRegions[entry] = component_dictionary[entry]
	return acceptedRegions
