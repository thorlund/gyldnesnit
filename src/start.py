#!/usr/bin/env python
"""
Quick n dirrrty test
"""

import sys
from lib import paintingAnalyzer
from lib import goldenLibrary
from settings import Settings
from painting import Painting

def main():
	try:
		filename = sys.argv[1]
	except IndexError:
		filename = "../res/local/small_seurat_bathers.png"

	painting = Painting(filename)
	cutRatios = [2.0/3, goldenLibrary.PHI]
	settings = Settings(cutRatios)
	res = paintingAnalyzer.analyze(painting, settings, "naive")
	#painting.setResults(result)

	#res = painting.getResults()

	for ratio in res:
		print ratio
		for cut in res[ratio]:
			print "\t%s objects in cut no. %s" % (len(res[ratio][cut]), cut)
			for result in res[ratio][cut]:
				print "\t\t%s" % res[ratio][cut][result][1].area

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
