"""
Provides methods for pruning a set of regions
"""

class Constraints:
	"""Holds a set of constraints for an image when finding regions at a cut"""
	rect = None
	size = None
	mass = None
	def __init__(imagesize, cut, margin, sizePercentage, massPercentage):
		"""Calculate all the constraints, i.e. the accepting
		rectangle (margin), the minimum size relative to the
		image and the minimum mass relative to the image.
		This class then functions as a quick lookup for those
		otherwise relatively demanding calulations.
		
		Arguments:
			imagesize = size of image as cvSize
			cut = the section we are inspecting as Line
			margin = Not yet defined :/
			sizePercentage = min % of pixels required for size of region
			massPercentage = min % of pixels required for mass of region
		"""
		# Insert tedious calculations
		raise NotImplementedError()


def checkPosition(component, constraints):
	"""Test if the component have a bounding box inside the accepting
	rectangle defined in the constraints."""
	raise NotImplementedError()

def checkSize(component, constraints):
	"""Test if the component have size greater than the minumum size
	defined by the constraints."""
	raise NotImplementedError()

def checkMass(component, constraints):
	"""Check if the component have mass greater than the minimum mass
	defined by the contraints."""
	raise NotImplementedError()

def pruneRegions(components, contraints):
	"""Run all required test on a set of regions with the given set
	of contraints."""
	raise NotImplementedError()
