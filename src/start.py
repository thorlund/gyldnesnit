#!/usr/bin/env python
"""
Quick n dirrrty test
"""

import sys
from lib import paintingAnalyzer
from lib import goldenLibrary
from settings import Settings
from painting import Painting
import model as m

def main():
	try:
		filename = sys.argv[1]
	except IndexError:
		filename = "../res/local/small_seurat_bathers.png"

	# Setup test database
	connection_string = 'sqlite:/:memory:'
	connection = m.s.connectionForURI(connection_string)
	m.s.sqlhub.processConnection = connection

	m.Artist.createTable()
	m.Painting.createTable()
	m.Run.createTable()
	m.Result.createTable()
	m.Region.createTable()

	vangogh = m.Artist(name="Van Gogh",born="1234-4321",school="klatmalerier",timeline="1600ish")
	solsikker = m.Painting(artist=m.Artist.selectBy(name="Van Gogh")[0].id,title="Solsikker",date="24 dec",technique="Fingermaling", location=filename,url="www.bogus.com/help",form="pas",type="klatmaling")

	# Initialize settings and a new run
	cutRatios = [2.0/3, goldenLibrary.PHI]
	settings = Settings(cutRatios)
	run = m.createNewRun(settings)
	runId = run.id
	print "RunId %s" % runId

	for entry in list(m.Painting.select()):
		painting = Painting(entry)
		result = paintingAnalyzer.analyze(painting, settings, "naive")
		painting.setResults(result)
		m.saveResults(runId, painting)

	results = list(m.Result.select())

	for result in results:
		res = list(m.Region.select(m.Region.q.result==result.id))
		print result
		for r in res:
			print "\t%s" % r

	settings = m.getSettingsForRunId(1)

	#painting = Painting(filename)
	#cutRatios = [2.0/3, goldenLibrary.PHI]
	#settings = Settings(cutRatios)
	#res = paintingAnalyzer.analyze(painting, settings, "naive")
	#painting.setResults(result)

	#res = painting.getResults()

	"""
	for ratio in res:
		print ratio
		for cut in res[ratio]:
			print "\t%s objects in cut no. %s" % (len(res[ratio][cut]), cut)
			for result in res[ratio][cut]:
				print "\t\t%s" % res[ratio][cut][result][1].area
	"""

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
