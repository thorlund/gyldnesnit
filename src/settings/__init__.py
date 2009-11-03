#!/usr/bin/env python
"""
Settings
The settings are global constants for a run
"""

class Settings:
	"""These are the default settings for the analysis"""
	edgeThreshold1 = 78
	edgeThreshold2 = 2.5 * edgeThreshold1
	lo = 5
	up = 5
	cutRatios = None
	marginPercentage = 0.009

	def __init__(self, cutRatios):
		# This check should be moved to the set-method
		if cutRatios is None:
			raise StandardError()
		self.setCutRatios(cutRatios)

	def setThreshold1(self, trsh):
		"""Set threshold1
		Will auto-set threshold2 to 2.5 * trsh"""
		self.edgeThreshold1 = trsh
		self.edgeThreshold2 = thrsh * 2.5

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
		self.cutRatios = cutRatios

	def setMarginPercentage(self, perc):
		"""Set the percent for margin"""
		self.marginPercentage = perc


### Test ###

def main():
	# Studpid test for nothing
	print "Test"
	cutRatios = [0.618]
	test = Settings(cutRatios)
	print test.edgeThreshold1

if __name__ == "__main__":
	main()
