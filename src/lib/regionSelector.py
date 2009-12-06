"""
Provides methods for pruning a set of regions
"""

import goldenLibrary as lib
import grid

class Constraints:
	"""Holds a set of constraints for an image when finding regions at a cut"""
	coordinate = None
	acceptRange = None
	superAcceptRange = None
	rect = None
	size = None
	mass = None
	def __init__(self, imagesize, cut, margin, supermargin, sizePercentage=0.002, massPercentage=0.15):
		"""Calculate all the constraints, i.e. the accepting
		rectangle (margin), the minimum size relative to the
		image and the minimum mass relative to the image.
		This class then functions as a quick lookup for those
		otherwise relatively demanding calulations.
		
		Arguments:
			imagesize = size of image as cvSize
			cut = the section we are inspecting as Line
			margin = floor(marginWidth/2) as int
			sizePercentage = min % of pixels required for size of region as decimal
			massPercentage = min % of pixels required for mass of region as decimal
		"""
		if not (0 <= sizePercentage and sizePercentage <= 1):
			raise ValueError("sizePercentage must be a number between 0 and 1")

		if not (0 <= massPercentage and massPercentage <= 1):
			raise ValueError("sizePercentage must be a number between 0 and 1")

		if not (0 < margin):
			raise ValueError("margin must be greater than 0")

		totalPixels = imagesize.height * imagesize.width
		self.size = sizePercentage * totalPixels
		self.mass = massPercentage

		if cut.p1.x == cut.p2.x:
			# Vertical
			self.coordinate = 0
			lower_bound = cut.p1.x - margin
			upper_bound = cut.p1.x + margin
			self.acceptRange = range(lower_bound, upper_bound + 1, 1)
			#superlower_bound = cut.p1.x - supermargin
			#superupper_bound = cut.p1.x + supermargin
			#self.superAcceptRange = range(superlower_bound, superupper_bound + 1, 1)
		elif cut.p1.y == cut.p2.y:
			# Horizontal
			self.coordinate = 1
			lower_bound = cut.p1.y - margin
			upper_bound = cut.p1.y + margin
			self.acceptRange = range(lower_bound, upper_bound + 1, 1)
			#superlower_bound = cut.p1.y - supermargin
			#superupper_bound = cut.p1.y + supermargin
			#self.superAcceptRange = range(superlower_bound, superupper_bound + 1, 1)
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
	
	return (p in constraints.acceptRange) or ( (p + d) in constraints.acceptRange)

def checkSuperPosition(component, constraints):
	"""Test if the component have a bounding box inside the SuperAccepting
	rectangle defined in the constraints. this def i mebnt to confine the box whit ind are
	large margin"""
	d = component.rect.width
	p = component.rect.x
	if constraints.coordinate:
		d = component.rect.height
		p = component.rect.y
	
	return (p in constraints.superAcceptRange) and ( (p + d) in constraints.superAcceptRange)

def checkSize(component, constraints):
	"""Test if the component have size greater than the minumum size
	defined by the constraints."""
	return component.area >= constraints.size

def checkCenterOfMass(constraints, grid):
	"""muhaaa
	"""
	p = centerOfMass(grid)
	return (p in constraints.acceptRange)
	
def pixelSideCounter(gridPointsList, cut):
	"""
	counts the difrens in pixels at both side og the cut in are blob
	"""
	counter = []
	for ragions in gridPointsList:
		tmp = 0
		left = 0
		right = 0
		for points in ragions:
			if cut > points.x:
				left = left + 1.0
			elif cut < points.x:
				right = right + 1.0
			tmp = tmp + 1.0;
		if (tmp == 0):
			counter.append(1)
		else:
			counter.append((right - left)/tmp)
	return counter
	
def centerOfMass(grid):
	"""
	Canculate the center of mass of alle the regions
	"""
	centerOfMassList = []
	tmp = 0
	for points in grid:
		tmp = tmp + points.x
	if (tmp == 0):
		return 0
	else:
		return(tmp/len(grid))
		
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

def pruneExpandedRegions(component_dictionary, contraints):
	"""Run all required test on a dictionary of regions with the given set
	of contraints. The output is a pruned components_dictionary."""
	acceptedRegions = {}
	for entry in component_dictionary:
		component = component_dictionary[entry][1]
		if checkSize(component, contraints) and checkMass(component, contraints):
			acceptedRegions[entry] = component_dictionary[entry]
	return acceptedRegions
	
def pruneExpandedRagionsto(component_dictionary, contraints, cut, workImage):
	"""
	run center of mass an prune the ragion
	"""
	#Get the count af pixels from left ore top
	if cut.getPoints()[0].x == cut.getPoints()[1]:
		pixels = cut.getPoints()[1].y
	else:
		pixels = cut.getPoints()[1].x
		
	#get are grid for alle the ragions
	grids = grid.gridIt(workImage, component_dictionary)

	#procent list over pixels on bots side 
	rigensPixelSidecount = pixelSideCounter(grids, pixels)
	
	#remove the raions thet i no good in the
	acceptedRegions = {}
	i = 0
	for entries in component_dictionary:
		if abs(rigensPixelSidecount[i]) < 0.75 and checkCenterOfMass(contraints, grids[i]):
			acceptedRegions[entries] = component_dictionary[entries]
		i = i + 1
	return acceptedRegions
