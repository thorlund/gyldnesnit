#!/usr/bin/env python
"""
Model
Classes/tables for the database

Keys marked with underscores are primary keys
Keys marked with a ^ are foreign keys
"""

import sqlobject as s

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

class Result(s.SQLObject):
	"""
	_id_, ^runId, ^paintingId, cutRatio, cutNo, numberOfRegions
	"""

	runId = s.ForeignKey('Run')
	paintingId = s.ForeignKey('Painting')
	cutRatio = s.FloatCol()
	cutNo = s.IntCol()
	numberOfRegions = s.IntCol()

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

	t = Run(trsh1=2, trsh2=2, lo=3, up=2, marginPercentage=0.0009)
	print Run.get(1).id

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
