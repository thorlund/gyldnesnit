#!/usr/bin/env python
"""
Model
Classes/tables for the database

Keys marked with underscores are primary keys
Keys marked with a ^ are foreign keys
"""

# Access to other libraries
import sys
sys.path.append('../')

import sqlobject as s
from src.settings import Settings

class Artist(s.SQLObject):
	"""
	_id_, the rest
	"""
	name = s.StringCol()
	born = s.StringCol()
	school = s.StringCol()
	timeline = s.StringCol()

class Painting(s.SQLObject):
	"""
	_id_, ^artistId, the rest
	"""
	artist = s.ForeignKey('Artist')
	title = s.StringCol()
	date = s.StringCol()
	technique = s.StringCol()
	location = s.StringCol()
	url = s.StringCol()
	form = s.StringCol()
	type = s.StringCol()

def createNewRun(settings):
	"""Create a new run using a settings class"""
	trsh1 = settings.edgeThreshold1
	trsh2 = settings.edgeThreshold2
	lo = settings.lo
	up = settings.up
	marginPercentage = settings.marginPercentage
	return Run(trsh1=trsh1, trsh2=trsh2, lo=lo, up=up, marginPercentage=marginPercentage)

class Run(s.SQLObject):
	"""
	_id_, trsh1, trsh2, lo, up, marginPercentage
	"""

	trsh1 = s.FloatCol()
	trsh2 = s.FloatCol()
	lo = s.IntCol()
	up = s.IntCol()
	marginPercentage = s.FloatCol()

def saveResults(runId, painting):
	"""Given a class painting with results and the runId
	store the results in the database"""
	# Get id and results
	paintingId = painting.getId()
	paintingResults = painting.getResults()

	if paintingResults is None:
		"""Return if we have no results"""
		return -1

	for cutRatio in paintingResults:
		for cutNo in paintingResults[cutRatio]:
			numberOfRegions = len(paintingResults[cutRatio][cutNo])

			# Create a new result
			result = Result(runId=runId, paintingId=paintingId, cutRatio=cutRatio, cutNo=cutNo, numberOfRegions=numberOfRegions)
			resultId = result.id
			print "\t%s objects in cut no. %s" % (numberOfRegions, cutNo)
			for region in paintingResults[cutRatio][cutNo]:
				component = paintingResults[cutRatio][cutNo][regio][1]
				createNewRegion(resultId, component)


class Result(s.SQLObject):
	"""
	_id_, ^runId, ^paintingId, cutRatio, cutNo, numberOfRegions
	"""

	runId = s.ForeignKey('Run')
	paintingId = s.ForeignKey('Painting')
	cutRatio = s.FloatCol()
	cutNo = s.IntCol()
	numberOfRegions = s.IntCol()

def createNewRegion(resultId, component):
	"""Create a new region in the database from
	a connected component"""
	rect = component.rect
	x = int(rect.x)
	y = int(rect.y)
	heigth = int(rect.height)
	width = int(rect.width)
	blobArea = int(component.area)
	return Region(resultId=resultId, x=x, y=y, height=height, width=width, blobArea=blobArea)

class Region(s.SQLObject):
	"""
	_id_, ^resultId, x, y, height, width, blobArea
	"""

	resultId = s.ForeignKey('Result')
	x = s.IntCol()
	y = s.IntCol()
	height = s.IntCol()
	width = s.IntCol()
	blobArea = s.IntCol()

### Test ###

def main():
	# Stupid test for nothing
	print "Test"
	# Create an in-memory sqlite database just for test
	connection_string = 'sqlite:/:memory:'
	connection = s.connectionForURI(connection_string)
	s.sqlhub.processConnection = connection

	Run.createTable()
	Result.createTable()

	cuts = [0.618]

	settings = Settings(cuts)
	t = createNewRun(settings)
	
	print Run.get(1)
	print t.id

	res = Result(runId=Run.get(1).id, paintingId=2, cutRatio=0.618, cutNo=0, numberOfRegions=2)
	print Result.get(1)
	Artist.createTable()
	Painting.createTable()
	vangogh = Artist(name="Van Gogh",born="1234-4321",school="klatmalerier",timeline="1600ish")
	print vangogh
	solsikker = Painting(artist=Artist.selectBy(name="Van Gogh")[0].id,title="Solsikker",date="24 dec",technique="Fingermaling", location="/dev/null",url="www.bogus.com/help",form="pas",type="klatmaling")
	print solsikker


if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
