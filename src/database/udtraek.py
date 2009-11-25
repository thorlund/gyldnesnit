#! /usr/bin/env python
import sys
import os

sys.path.append(os.getcwd()[:os.getcwd().find('src')])
import src.model as m
from src.settings import GlobalSettings
from src.database import Database

db = Database(globalSettings)
results = m.Result.select(m.Result.q.run==2)

numberOfRegions = 0
amountOfPictures = 0
for result in results:
	numberOfRegions = numberOfRegion + result.numberOfRegions
	amountOfPictures = amountOfPictures +1

print ('There was %i regions detected in %i pictures',(numberOfRegions,amountOfPictures))
print 'average was :%i',(numberOfRegions/amountOfPictures)
