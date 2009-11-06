#!/usr/bin/env python
"""
Model
Classes/tables for the database

Keys marked with underscores are primary keys
Keys marked with a ^ are foreign keys
"""

class Artist(object):
	"""
	_id_, the rest
	"""
	pass

class Painting(object):
	"""
	_id_, ^artistId, the rest
	"""
	pass

class Run(object):
	"""
	_id_, trsh1, trsh2, lo, up, marginPercentage
	"""

	def __init__(self, settings):
		self.trsh1 = settings.edgeThreshold1
		self.trsh2 = settings.edgeThreshold2
		self.lo = settings.lo
		self.up = settings.up
		self.marginPercentage = settings.marginPercentage

class Result(object):
	"""
	_id_, ^runId, ^paintingId, cutRatio, cutNo, numberOfRegions
	"""
	pass

class Region(object):
	"""
	_id_, ^resultId, x, y, height, width, blobArea
	"""
	pass


### Test ###

def main():
	# Stupid test for nothing
	print "Test"

if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
