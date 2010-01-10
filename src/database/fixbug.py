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


globalSettings= GlobalSettings()
db = Database(globalSettings)
#run = sys.argv[1]
runId = m.Result.select().max('run_id')
results = m.Result.select(m.Result.q.run == runId)
conn = m.Result._connection
for result in results:
	count = 0
	feats = dict()
	regions = m.Region.select(m.Region.q.result == result.id).distinct()
	regionsSelect = conn.sqlrepr(b.Select([m.Region.q.x,m.Region.q.y,m.Region.q.height,m.Region.q.width,m.Region.q.blobArea],where=(result.id == m.Region.q.result)).distinct()) 
	regionsSelectResult=conn.queryAll(regionsSelect)
	"""
	for region in regions:
		key = str(region.x)+str(region.y)+str(region.height)+str(region.width)+str(region.blobArea)
		if key not in feats:
			feats[key]=True
			count = count +1
	print count
	"""
	result.numberOfRegions = len(regionsSelectResult)
	print result.id
