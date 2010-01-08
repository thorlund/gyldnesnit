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
paintings = paintings.filter(b.AND(m.Result.q.run==runId,m.Result.q.painting == m.Painting.q.id))
results = m.Result.select("painting.title NOT LIKE '%detail%'")
results = results.filter(b.AND(m.Result.q.run==runId,m.Result.q.painting == m.Painting.q.id))
artists = m.Artist.select("painting.title NOT LIKE '%detail%'")
artists = artists.filter(b.AND(m.Result.q.run==runId, m.Result.q.painting == m.Painting.q.id, m.Painting.q.artist == m.Artist.q.id))
#sorts resulsts after numberOfRegions, the starting one low and rising
goldenresults = results.filter(b.AND(m.Result.q.cutRatio < 0.62 , m.Result.q.cutRatio > 0.61))
#only the golden ratios and the paintings
goldenpaintings = paintings.filter(b.AND(m.Result.q.cutRatio < 0.62 , m.Result.q.cutRatio > 0.61))

print "Total number of regions found across all pictures"
numberOfRegions = results.sum(m.Result.q.numberOfRegions)
print numberOfRegions

print "Total number of paintings"
print paintings.distinct().count()

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
ratios=dict()
periodes=dict()
area=dict()
for timeline in timelines:
	timeline = timeline[0]
	cuts = []
	for cut in range(4):
		for ratio in diffratios:
			ratio = ratio[0]
			ratios[ratio]=results.filter(b.AND(m.Result.q.cutRatio==ratio , m.Result.q.cutNo==cut, m.Artist.q.timeline==timeline)).distinct().sum(m.Result.q.numberOfRegions)
		cuts.append(ratios)
		ratios=dict()
	picTimeline=paintings.filter(b.AND( m.Painting.q.artist==m.Artist.q.id, m.Artist.q.timeline==timeline)).distinct()
	for painting in picTimeline:
		if not (painting.realWidth == None and painting.realHeight == None):
			if int(painting.realWidth*painting.realHeight) not in area:
				area[int(painting.realWidth * painting.realHeight)] = results.filter(painting.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
			else:
				area[int(painting.realWidth*painting.realHeight)] =results.filter(painting.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions) + area[int(painting.realWidth*painting.realHeight)]
	picTimeline = picTimeline.count()
	periodes[timeline] = (cuts,area,picTimeline)
	area = dict()
print "This tuple shows how many features are detected in the golden ratio and overall and the amount of pictures in/of a given timeline"
print periodes

print "The features per paintings dict"
featPerPicture = dict()
topten = dict()
toptengolden = dict()
area = dict()
#This is also used toptengolden and topten images
#Also a ratio for the size of the paintings
for picture in paintings.distinct():
	numbOfRegions = paintings.filter(picture.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
	numbOfGoldenRegions = goldenpaintings.filter(picture.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
	if numbOfRegions not in topten:
		topten[numbOfRegions] = [picture.id]
	else:
		topten[numbOfRegions].append(picture.id)
	if numbOfGoldenRegions not in toptengolden:
		toptengolden[numbOfGoldenRegions] = [picture.id]
	else:
		toptengolden[numbOfGoldenRegions].append(picture.id)
	if numbOfRegions not in featPerPicture:
		featPerPicture[numbOfRegions] = 1
	else:
		featPerPicture[numbOfRegions] = featPerPicture[numbOfRegions] +1
	#Size of painting calculations
	if picture.realHeight != None and picture.realWidth !=None:
		if int(picture.realWidth*picture.realHeight) not in area:
			print "I R IN LOOP"
			area[int(painting.realWidth * painting.realHeight)] = results.filter(painting.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
		else:
			area[int(picture.realWidth*picture.realHeight)] = area[int(picture.realWidth*picture.realHeight)] + results.filter(painting.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
print featPerPicture

#printing the area/feats
print "The area combined with how many regions are found"
print area

print "Procentage of different schools use the golden ratio "
schoolsSelect = conn.sqlrepr(b.Select(m.Artist.q.school).distinct())
schools = conn.queryAll(schoolsSelect)
countries = dict()
area = dict()
for school in schools:
	cuts = []
	school = school[0]#dont ask
	for cut in range(4):
		for ratio in diffratios:
			ratio = ratio[0]
			ratios[ratio]=results.filter(b.AND(m.Result.q.cutRatio==ratio , m.Result.q.cutNo==cut, m.Artist.q.school==school)).distinct().sum(m.Result.q.numberOfRegions)
		cuts.append(ratios)
		ratios = dict()
	amountOfPaintings = paintings.filter(b.AND(m.Painting.q.artist == m.Artist.q.id, m.Artist.q.school == school)).distinct().count()
	amountOfArtist = artists.filter(m.Artist.q.school==school).distinct().count()
	schoolsPaintings =paintings.filter(b.AND(m.Painting.q.artist == m.Artist.q.id, m.Artist.q.school == school)).distinct()
	for painting in schoolsPaintings:
		if painting.realWidth != None and painting.realHeight != None:
			if int(painting.realWidth * painting.realHeight) not in area:
				area[int(painting.realWidth * painting.realHeight)] = paintings.filter(painting.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
			else:
				area[int(painting.realWidth * painting.realHeight)] = area[int(painting.realWidth * painting.realHeight)]+paintings.filter(painting.id == m.Painting.q.id).distinct().sum(m.Result.q.numberOfRegions)
	countries[school] = (cuts,area,amountOfPaintings)
	area = dict()
print countries 

goldenpictures = paintings.filter(b.AND(m.Result.q.cutRatio < 0.62,m.Result.q.cutRatio > 0.61, m.Result.q.numberOfRegions > 0)).distinct().count()
print "Antallet af billeder, der har regioner i det gyldne snit, for snit 0-3"
print goldenpictures

#top ten images with the most features in the golden ratio
#from the toptengolden dict in the calcutation of how many features in general is in a picture
print "The top ten images with the most features in the golden ratio"
toptengoldenkeys = toptengolden.keys()
for feats in toptengoldenkeys[-10:]:
	for paintingId in toptengolden[feats]:
		toptenimages=  m.Painting.select(m.Painting.q.id == paintingId).getOne()
		print toptenimages.filepath
		print "with:"
		print feats

#top then image with the most features
#from the topten dict in the calcutation of how many features in general is in a picture
print "The top ten images with the most features in any ratio"
toptenkeys = topten.keys()
for feats in toptenkeys[-10:]:
	for paintingId in topten[feats]:
		toptenimages=  m.Painting.select(m.Painting.q.id == paintingId).getOne()
		print toptenimages.filepath
		print "with:"
		print feats
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
