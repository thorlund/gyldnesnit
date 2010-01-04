#! /usr/bin/env python
import sys
import os

sys.path.append(os.getcwd()[:os.getcwd().find('src')])
import src.model as m
from src.settings import GlobalSettings
from src.database import Database
from src.lib import goldenLibrary
from sqlobject import sqlbuilder as b
import sqlobject as s


globalSettings = GlobalSettings()
db = Database(globalSettings)
runId = m.Result.select().max('run_id')
paintings = m.Painting.select("painting.title NOT LIKE '%detail%'")
paintings = paintings.filter(b.AND(m.Result.q.run==runId,m.Result.q.painting == m.Painting.q.id)).distinct()
results = m.Result.select("painting.title NOT LIKE '%detail%'")
results = results.filter(b.AND(m.Result.q.run==runId,m.Result.q.painting == m.Painting.q.id))
artists = m.Artist.select("painting.title NOT LIKE '%detail%'")
artists = artists.filter(b.AND(m.Result.q.run==runId, m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist == m.Artist.q.id))
#results = m.Result.select(m.Result.q.run==runId)
#sorts resulsts after numberOfRegions, the starting one low and rising
results = results.orderBy('numberOfRegions')
goldenresults = results.filter(b.AND(m.Result.q.cutRatio < 0.62 , m.Result.q.cutRatio > 0.61))

print "Total number of regions found across all pictures"
numberOfRegions = results.sum('number_of_regions')
print numberOfRegions

numberOfPaintings = m.Painting.select(b.AND(m.Result.q.run==runId,m.Painting.q.id==m.Result.q.painting))
numberOfPaintings = numberOfPaintings.distinct().count()
print "Total number of paintings"
print paintings.count()

conn = m.Result._connection
nameselect = conn.sqlrepr(b.Select(m.Result.q.cutRatio).distinct())
diffratios = conn.queryAll(nameselect)
ratios=dict()
cuts = []
for cut in range(4):
	for ratio in diffratios:
		ratio = ratio[0]
		ratios[ratio]=results.filter(b.AND(m.Result.q.cutRatio==ratio , m.Result.q.cutNo==cut)).sum(m.Result.q.numberOfRegions)
	cuts.append(ratios)
	ratios = dict()

print "The different ratios followed by the amount of features found i that ratio:"
print cuts

goldenratiocuts=[0,0,0,0]
for cut in range(4):
	goldenratiocuts[cut]=goldenresults.filter(m.Result.q.cutNo==cut).sum(m.Result.q.numberOfRegions)
print "How the four different cuts are used"
print goldenratiocuts

nameselect = conn.sqlrepr(b.Select(m.Artist.q.timeline).distinct())
timelines = conn.queryAll(nameselect)

periodes=dict()
for timeline in timelines:
	timeline = timeline[0]
	goldenFeatTimeline=goldenresults.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist==m.Artist.q.id, m.Artist.q.timeline==timeline)).distinct().sum(m.Result.q.numberOfRegions)
	picTimeline=results.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist==m.Artist.q.id, m.Artist.q.timeline==timeline)).distinct().count()
	featsInTimeline = results.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist==m.Artist.q.id, m.Artist.q.timeline==timeline)).distinct().sum(m.Result.q.numberOfRegions)
	periodes[timeline] = (goldenFeatTimeline,featsInTimeline,picTimeline)

print "This tuple shows how many features are detected in the golden ratio and overall and the amount of pictures in/of a given timeline"
print periodes


print "The features per pcitures dict"
featPerPicture = dict()
for picture in paintings:
	numbOfRegions = paintings.filter(picture.id == m.Painting.q.id).sum(m.Result.q.numberOfRegions)
	if numbOfRegions not in featPerPicture:
		featPerPicture[numbOfRegions] = 1
	else:
		featPerPicture[numbOfRegions] = featPerPicture[numbOfRegions] +1
print featPerPicture

print "Procentage of different schools use the golden ratio "
schoolsSelect = conn.sqlrepr(b.Select(m.Artist.q.school).distinct())
schools = conn.queryAll(schoolsSelect)
countries = dict()
for school in schools:
	school = school[0]#dont ask
	amountOfPaintings = paintings.filter(b.AND(m.Painting.q.artist == m.Artist.q.id, m.Artist.q.school == school)).distinct().count()
#	print paintings.filter(b.AND(m.Painting.q.artist == m.Artist.q.id, m.Artist.q.school == school)).distinct()
	amountOfArtist = artists.filter(m.Artist.q.school==school).distinct().count()
	amountOfRegions = results.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist == m.Artist.q.id, m.Artist.q.school == school)).distinct().count()
	amountOfGoldenRegions =goldenresults.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist == m.Artist.q.id, m.Artist.q.school == school)).distinct().count()
	print school
	print amountOfGoldenRegions
	print amountOfRegions
	print amountOfPaintings
	countries[school] = (amountOfGoldenRegions, amountOfRegions, amountOfPaintings,amountOfGoldenRegions/amountOfRegions/amountOfPaintings)
print countires 

goldenpictures = paintings.filter(b.AND(m.Result.q.cutRatio < 0.62,m.Result.q.cutRatio > 0.61, m.Result.q.numberOfRegions > 0)).distinct().count()
print "Antallet af billeder, der har regioner i det gyldne snit, for snit 0-3"
print goldenpictures

#top ten images with the most features in the golden ratio
print "The top ten images with the most features in the golden ratio"
for image in goldenresults.orderBy('numberOfRegions')[-10:]:
	toptenimages=  m.Painting.select(m.Painting.q.id == image.painting).getOne()
	print toptenimages.filepath
	print "with:"
	print image.numberOfRegions

#top then image with the most features
print "The top ten images with the most features in any ratio"
for image in results.orderBy('numberOfRegions')[-10:]:
	toptenimages=  m.Painting.select(m.Painting.q.id == image.painting).getOne()
	print toptenimages.filepath
	print "with:"
	print image.numberOfRegions

paintings = paintings.distinct()
# Get number of paintings with golden section canvas BY PIXEL SIZE
print ""
print "Number of images with golden section canvas MEASSURED BY PIXEL SIZE"
gCount = 0
lower = goldenLibrary.phi - (0.024 * goldenLibrary.phi)
upper = goldenLibrary.phi + (0.024 * goldenLibrary.phi)
print "	We have that the larger side, divided by the smaller"
print "	is in the interval [%s, %s]" % (lower, upper)
for painting in paintings.filter(b.AND(m.Painting.q.height!=None,m.Painting.q.width!=None)):
	factor = max(painting.height, painting.width)/float(min(painting.height, painting.width))
	if lower <= factor <= upper:
		gCount = gCount + 1

total = paintings.filter(b.AND(m.Painting.q.height!=None,m.Painting.q.width!=None)).count()
print "%s painting with a canvas as a golden rectangle of %s total" % (gCount, total)
print "That is %s percent" % ((float(gCount)/total)*100)

# Get number of paintings with golden section canvas BY REAL SIZE
print ""
print "Number of images with golden section canvas MEASSURED BY REAL SIZE"
gCount = 0
print "	We have that the larger side, divided by the smaller"
print "	is in the interval [%s, %s]" % (lower, upper)
for painting in paintings.filter(b.AND(m.Painting.q.realWidth!=None,m.Painting.q.realHeight!=None)).distinct():
	factor = max(painting.realHeight, painting.realWidth)/min(painting.realHeight, painting.realWidth)
	if lower <= factor <= upper:
		gCount = gCount + 1

total = paintings.filter(b.AND(m.Painting.q.realWidth!=None,m.Painting.q.realHeight!=None)).distinct().count()
print "%s painting with a canvas as a golden rectangle of %s total" % (gCount, total)
print "That is %s percent" % ((float(gCount)/total)*100)
