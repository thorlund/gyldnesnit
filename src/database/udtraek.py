#! /usr/bin/env python
import sys
import os

sys.path.append(os.getcwd()[:os.getcwd().find('src')])
import src.model as m
from src.settings import GlobalSettings
from src.database import Database
from src.lib import goldenLibrary


globalSettings = GlobalSettings()
db = Database(globalSettings)
results = m.Result.select().max('run_id')
results = m.Result.select(m.Result.q.run==results)

numberOfRegions = 0
amountOfPictures = 0
categories=dict()
ratios=dict()
goldenratiocuts=[0,0,0,0]
periodes=dict()
toptencuts=dict()
toptenfeatures=dict()
toptengoldenfeatures=dict()
toptenthirdsfeatures=[]
for result in results:
#	Det her er hvad vi skal finde i den raekkefolge
#	Adding the number of features on a given ratio
	print result 
	if result.cutRatio not in ratios:
		ratios[result.cutRatio] = 0
	else:
		ratios[result.cutRatio] = ratios[result.cutRatio]+result.numberOfRegions
#	sammenlign gyldnesnit cuts
	if str(result.cutRatio) == str(goldenLibrary.PHI):
		goldenratiocuts[result.cutNo] = goldenratiocuts[result.cutNo]+result.numberOfRegions
#	summere periode paa gyldnesnit
	timeline = result.painting.artist.timeline
	if timeline not in periodes.keys():
		periodes[timeline]=0
	else:
		periodes[timeline]=periodes[timeline]+ result.numberOfRegions
#	top10 snit,billed? features, features i gyldnesnit per billed, features i 1/3 per billed
	toptencutskey = str(result.paintingID)+str(result.cutNo)
	print toptencutskey
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
	numberOfRegions = numberOfRegions + result.numberOfRegions
	amountOfPictures = amountOfPictures +1
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
