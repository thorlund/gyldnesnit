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
results = m.Result.select(m.Result.q.run==runId)
#sorts resulsts after numberOfRegions, the starting one low and rising
results = results.orderBy('numberOfRegions')
goldenresults = results.filter(b.AND(m.Result.q.cutRatio < 0.62 , m.Result.q.cutRatio > 0.61))

print "Total number of regions found across all pictures"
numberOfRegions = results.sum('number_of_regions')
print numberOfRegions

numberOfPaintings = m.Painting.select(b.AND(m.Result.q.run==runId,m.Painting.q.id==m.Result.q.painting))
numberOfPaintings = numberOfPaintings.distinct().count()
print "Total number of paintings"
print numberOfPaintings

conn = m.Result._connection
nameselect = conn.sqlrepr(b.Select(m.Result.q.cutRatio).distinct())
diffratios = conn.queryAll(nameselect)
ratios=dict()
for ratio in diffratios:
	ratio = ratio[0]
	ratios[ratio]=results.filter(m.Result.q.cutRatio==ratio).sum(m.Result.q.numberOfRegions)


print "The different ratios followed by the amount of features found i that ratio:"
print ratios
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
	picTimeline=results.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist==m.Artist.q.id, m.Artist.q.timeline==timeline)).distinct().sum(m.Result.q.numberOfRegions)
	featsInTimeline = results.filter(b.AND(m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist==m.Artist.q.id, m.Artist.q.timeline==timeline)).distinct().sum(m.Result.q.numberOfRegions)
	periodes[timeline] = (goldenFeatTimeline,featsInTimeline,picTimeline)

print "This tuple shows how many features are detected in the golden ratio and overall and the amount of pictures in/of a given timeline"
print periodes


print "The features per picture dict"
featPerPicture = dict()
for picture in results:
	if picture.numberOfRegions not in featPerPicture:
		featPerPicture[picture.numberOfRegions] = 1
	else:
		featPerPicture[picture.numberOfRegions] = featPerPicture[picture.numberOfRegions] +1
print featPerPicture

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
