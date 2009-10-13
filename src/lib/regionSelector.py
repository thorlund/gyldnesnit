"""
Provides methods for pruning a set of regions
"""

class Constraints:
	"""Holds a set of constraints for an image when finding regions at a cut"""
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
			margin = Not yet defined :/
			sizePercentage = min % of pixels required for size of region as decimal
			massPercentage = min % of pixels required for mass of region as decimal
		"""
		# Insert tedious calculations
		totalPixels = imagesize.height * imagesize.width
		self.size = sizePercentage * totalPixels


def checkPosition(component, constraints):
	"""Test if the component have a bounding box inside the accepting
	rectangle defined in the constraints."""
	raise NotImplementedError()

def checkSize(component, constraints):
	"""Test if the component have size greater than the minumum size
	defined by the constraints."""
	return component.area >= constraints.size

def checkMass(component, constraints):
	"""Check if the component have mass greater than the minimum mass
	defined by the contraints."""
	raise NotImplementedError()

def pruneRegions(components, contraints):
	"""Run all required test on a set of regions with the given set
	of contraints."""
	acceptedRegions = []
	for component in components:
		#if checkPosition(component, contraints) and checkSize(component, contraints) and checkMass(component, contraints):
		if checkSize(component, contraints):
			acceptedRegions.append(component)
	return acceptedRegions
