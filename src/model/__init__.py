#!/usr/bin/env python
"""
Model
Classes/tables for the database

Keys marked with underscores are primary keys
Keys marked with a ^ are foreign keys
"""

# Access to other libraries
import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

import sqlobject as s
from src.settings import Settings
from src.lib import graphicHelper as g
from src import painting as p
from opencv import cv

class Settings(s.SQLObject):
	paintingcount = s.IntCol()
	newestrun = s.IntCol()

class Artist(s.SQLObject):
	"""
	_id_, name, born, died, school, timeline
	"""
	name = s.StringCol()
	born = s.IntCol()
	died = s.IntCol()
	school = s.StringCol()
	timeline = s.StringCol()


class Painting(s.SQLObject):
	"""
	_id_, ^artistId, title, date, paint, material, location, url, form,
	type, realHeight, realWidth, height, width, filepath
	"""
	artist = s.ForeignKey('Artist')
	title = s.StringCol()
	date = s.IntCol()
	paint = s.StringCol()
	material = s.StringCol()
	location = s.StringCol()
	url = s.StringCol()
	form = s.StringCol()
	type = s.StringCol()
	realHeight = s.FloatCol()
	realWidth = s.FloatCol()
	height = s.IntCol()
	width = s.IntCol()
	filepath = s.StringCol()

	def getSize(self):
		"""Return cv.cvSize"""
		if (self.width is None) or (self.height is None):
			return None
		return cv.cvSize(self.width, self.height)

	def setSize(self, size):
		"""Input cv.cvSize"""
		self._set_height(size.height)
		self._set_width(size.width)


def createNewRun(settings):
	"""Create a new run using a settings class"""

	trsh1 = settings.edgeThreshold1
	trsh2 = settings.edgeThreshold2
	lo = settings.lo
	up = settings.up
	marginPercentage = settings.marginPercentage
	method = settings.method
	return Run(trsh1=trsh1, trsh2=trsh2, lo=lo, up=up, marginPercentage=marginPercentage, method=method)


class Run(s.SQLObject):
	"""
	_id_, trsh1, trsh2, lo, up, marginPercentage, method
	"""

	trsh1 = s.FloatCol()
	trsh2 = s.FloatCol()
	lo = s.IntCol()
	up = s.IntCol()
	marginPercentage = s.FloatCol()
	method = s.StringCol()


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
			result = Result(run=runId, painting=paintingId, cutRatio=cutRatio, cutNo=cutNo, numberOfRegions=numberOfRegions)
			resultId = result.id
			for region in paintingResults[cutRatio][cutNo]:
				component = paintingResults[cutRatio][cutNo][region][1]
				createNewRegion(resultId, component)


class Result(s.SQLObject):
	"""
	_id_, ^runId, ^paintingId, cutRatio, cutNo, numberOfRegions
	"""

	run = s.ForeignKey('Run')
	painting = s.ForeignKey('Painting')
	cutRatio = s.FloatCol()
	cutNo = s.IntCol()
	numberOfRegions = s.IntCol()

	def _set_cutRatio(self, value):
		val = float(value)
		self._SO_set_cutRatio(val)


def createNewRegion(resultId, component):
	"""Create a new region in the database from
	a connected component
	"""
	rect = component.rect
	x = int(rect.x)
	y = int(rect.y)
	height = int(rect.height)
	width = int(rect.width)
	blobArea = int(component.area)
	return Region(result=resultId, x=x, y=y, height=height, width=width, blobArea=blobArea)


class Region(s.SQLObject):
	"""
	_id_, ^resultId, x, y, height, width, blobArea
	"""

	result = s.ForeignKey('Result')
	x = s.IntCol()
	y = s.IntCol()
	height = s.IntCol()
	width = s.IntCol()
	blobArea = s.IntCol()

	def getBoundingBox(self):
		return cv.cvRect(self.x, self.y, self.width, self.height)


### Methods for reconstructing runs


def getSettingsForRunId(runId):
	"""Return the settings instance for a given run"""
	runInstance = Run.selectBy(id=runId)[0]

	# Get the cut ratios
	cutRatios = getCutRatiosForRunId(runId)

	settings = Settings(cutRatios)
	settings.setThresholds(runInstance.trsh1, runInstance.trsh2)
	settings.setLo(runInstance.lo)
	settings.setUp(runInstance.up)
	settings.setMarginPercentage(runInstance.marginPercentage)

	return settings


def getCutRatiosForRunId(runId):
	"""We need to hardcode some sql here due to SQLObject deficiencies :("""

	sql =  "SELECT DISTINCT result.cut_ratio "
	sql += "FROM result "
	sql += "WHERE result.run_id = (%s)" % runId

	query = Result._connection.queryAll(sql)
#Do some testing of this line to check if it correct
#	query = m.result.select(m.result.q.run_id == runID).distinct()

	cutRatios = []

	# This is a bit lame, but the result are put in a tuple
	for result in query:
		cutRatios.append(result)[0]

	return cutRatios


def getSettingsForResultId(resultId):
	# Get runId
	runId = Result.select(Result.q.id==resultId)[0].run.id

	# Get settings for runId
	return getSettingsForRunId(runId)


def getSettingsForRegionId(regionId):
	resultId = Region.select(Region.q.id==regionId)[0].result.id
	return getSettingsForResultId(resultId)


def getCutRatioForRegionId(regionId):
	return Region.select(Region.q.id==regionId)[0].result.cutRatio


def getCutNoForRegionId(regionId):
	return Region.select(Region.q.id==regionId)[0].result.cutNo


def getRegionsForResultId(resultId):
	return Region.select(Region.q.result==resultId)


def showPictureInResultId(resultId):
	painting = p.Painting(Result.select(Result.q.id==resultId)[0].painting)
	g.showImage(painting.getImage(), "Wee")


### Test ###

def main():
	# Stupid test for nothing
	print "Test"
	print ""
	print "A lot of crap-output"
	print ""
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

	res = Result(run=Run.get(1).id, painting=2, cutRatio=0.618, cutNo=0, numberOfRegions=2)
	print Result.get(1)
	Artist.createTable()
	Painting.createTable()
	vangogh = Artist(name="Van Gogh", born=1234, died=4321, school="klatmalerier", timeline="1600ish")
	print vangogh
	solsikker = Painting(artist=Artist.selectBy(name="Van Gogh")[0].id,title="Solsikker", date=1900, paint="maling", material='lort', location="../res/local/small_seurat_bathers.png",url="www.bogus.com/help",form="pas",type="klatmaling", realHeight=2, realWidth=3, height=None, width=None,filepath=None)
	print solsikker

	# Test that getSize returns None
	print "getSize == None is %s" % (solsikker.getSize() is None)

	# Make an instance painting (to load the image)
	painting = p.Painting(solsikker)

	# Get the size (maybe put a shorthand for this in Painting?)
	size = cv.cvGetSize(painting.getImage())

	# Test the setSize method
	solsikker.setSize(size)
	print solsikker

	# Test that we actually get the size now
	newSize = solsikker.getSize()
	print newSize.width, newSize.height


if __name__ == "__main__":
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
