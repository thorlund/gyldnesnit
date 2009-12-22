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
for result in results:
    print "new result"
    count = 0
    feats = dict()
    regions = m.Region.select(m.Region.q.result == result.id).distinct()
    for region in regions:
#        print region
        key = str(region.x)+str(region.y)+str(region.height)+str(region.width)+str(region.blobArea)
        if key not in feats:
#            print "key:"
#            print key
            feats[key]=True
            count = count +1
    if count > 0 and ((result.numberOfRegions/count) >3):
#        print feats
#        print count
#        print result.numberOfRegions
    result.numberOfRegions = count
