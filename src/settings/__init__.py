"""
Settings
The settings are global constants for a run
"""

class Settings:
	edgeThreshold1 = None
	edgeThreshold2 = None
	lo = None
	up = None
	cutRatios = None

	def __init__(self, cutRatios):
		self.edgeThreshold1 = 78
		self.edgeThreshold2 = 2.5 * self.edgeThreshold1

		self.lo = 5
		self.up = 5

		if cutRatios is None:
			raise StandardError()
		self.cutRatios = cutRatios
