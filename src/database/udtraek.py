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
	periodes[timeline] = (goldenFeatTimeline,picTimeline)

print "The tuple is how many features is found in a given timeline and the amount of picutres"
print periodes

toptencuts=dict()
toptenfeatures=dict()
toptengoldenfeatures=dict()
toptenthirdsfeatures=[]
'''
for result in results:
#	Det her er hvad vi skal finde i den raekkefolge
#	top10 snit,billed? features, features i gyldnesnit per billed, features i 1/3 per billed
	toptencutskey = str(result.paintingID)+str(result.cutNo)
	if toptencutskey not in toptencuts:
		toptencuts[toptencutskey]=result.numberOfRegions
	else:
		toptencuts[toptencutskey]=toptencuts[toptencutskey]+result.numberOfRegions
	if result.paintingID not in toptenfeatures:
		toptenfeatures[result.paintingID]=result.numberOfRegions
	else:
		toptenfeatures[result.paintingID]=toptenfeatures[result.paintingID]+result.numberOfRegions
	if str(result.cutRatio) == str(goldenLibrary.PHI):
		if result.paintingID not in toptengoldenfeatures:
			toptengoldenfeatures[result.paintingID]=result.numberOfRegions
		else:
			toptengoldenfeatures[result.paintingID] = toptengoldenfeatures[result.paintingID]+result.numberOfRegions
	toptenthirdsfeatures.append(result.numberOfRegions)
	if result.numberOfRegions not in categories.keys():
		categories[result.numberOfRegions]=1
	else:
		categories[result.numberOfRegions]= categories[result.numberOfRegions]+1
	
print "number of features in different periodes\n"
print periodes
print "Which golden ration is the most popular, ranging from 0 to 3"
print goldenratiocuts
print "features in the different ratios"
print ratios
	
toptencuts = toptencuts.values()
toptenfeatures = toptenfeatures.values()
toptengoldenfeatures = toptengoldenfeatures.values()
toptencuts.sort()
toptenfeatures.sort()
toptengoldenfeatures.sort()
toptenthirdsfeatures.sort()
print "Top 10 cuts, where the most features was found"
print toptencuts[-10:]
print toptenfeatures[-10:]
print toptengoldenfeatures[-10:]
print toptenthirdsfeatures[-10:]
'''
