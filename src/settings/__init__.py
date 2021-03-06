#!/usr/bin/env python
"""
Settings
The settings are global constants for a run
"""

# Access to other libraries
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

from src.lib import marginCalculator
from src.lib.goldenLibrary import PHI

### Global Settings ###

class GlobalSettings:
	"""Here global settings for the entire program can be placed"""
	relativeDatabaseLocation = "udvidet.db"
	absoluteDatabaseLocation = os.path.abspath(relativeDatabaseLocation)
	relativeCSVFileLocation = 'database/catalog.csv'
	absoluteCSVFileLocation = os.path.abspath(relativeCSVFileLocation)
	def getDatabaseLocation(self):
		return self.relativeDatabaseLocation
	def getCSVFileLocation(self):
		return self.absoluteCSVFileLocation


### Settings For an Analysis ###


class Settings:
	"""These are the default settings for the analysis.
	The standard margin is the difference between phi and
	2/3"""
	edgeThreshold1 = 78
	edgeThreshold2 = 2.5 * edgeThreshold1
	lo = 4
	up = 4
	cutRatios = None
	marginPercentage = (2.0/3) - PHI
	method = 'naive'

	def __init__(self, cutRatios):
		# This check should be moved to the set-method
		if cutRatios is None:
			raise StandardError()
		self.setCutRatios(cutRatios)

		# Get the marginPercentage
		marginPercentage = marginCalculator.getPercentage(self.cutRatios, self.marginPercentage)
		if not (marginPercentage is None):
			self.marginPercentage = marginPercentage

	def setThreshold1(self, trsh):
		"""Set threshold1
		Will auto-set threshold2 to 2.5 * trsh"""
		self.edgeThreshold1 = trsh
		self.edgeThreshold2 = trsh * 2.5

	def setThreshold2(self, trsh):
		"""Set threshold2"""
		self.edgeThreshold2 = trsh

	def setThresholds(self, trsh1, trsh2):
		"""Set thresholds"""
		self.edgeThreshold1 = trsh1
		self.edgeThreshold2 = trsh2

	def setLo(self, lo):
		"""Set the lower bound for flood fill"""
		self.lo = lo

	def setUp(self, up):
		"""Set the upper bound for flood fill"""
		self.up = up

	def setCutRatios(self, cutRatios):
		"""Set the list of ratios for cuts"""
		# TODO: Check if this is an array
		# Adjust the ratio according to specifications
		for i in range(len(cutRatios)):
			if cutRatios[i] < 0.5:
				cutRatios[i] = 1 - cutRatios[i]
			elif cutRatios[i] > 1.0:
				# Scary
				# Maybe raise an error
				cutRatios[i] = cutRatios[i] - 1
		self.cutRatios = cutRatios

	def setMarginPercentage(self, perc):
		"""Set the percent for margin"""
		self.marginPercentage = perc

	def setMethod(self, method):
		"""Set the method for analysis"""
		self.method = method

	def __repr__(self):
		str =  "Settings\n"
		str += "Margin ratios: \t\t%s\n" % self.cutRatios
		str += "Thresholds: \t\t%s, %s\n" % (self.edgeThreshold1, self.edgeThreshold2)
		str += "Bounds: \t\t%s, %s\n" % (self.lo, self.up)
		str += "Margin percentage: \t%s\n" % self.marginPercentage
		str += "Method: \t\t%s" % self.method
		return str


### Test ###

def main():
	# Studpid test for nothing
	print "Test"
	cutRatios = [0.618, 1.0/2, 2.0/3]
	cutRatios = [0.618034, 2.0/3]
	cutRatios = [1.0/2]
	test = Settings(cutRatios)
	print test.edgeThreshold1
	print test

	#globals = GlobalSettings()
	#print globals.absoluteDatabaseLocation

if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
