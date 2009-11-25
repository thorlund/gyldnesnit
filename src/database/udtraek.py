#! /usr/bin/env python
import sys
import os

sys.path.append(os.getcwd()[:os.getcwd().find('src')])
import src.model as m
from src.settings import GlobalSettings
from src.database import Database


globalSettings = GlobalSettings()
db = Database(globalSettings)
results = m.Result.select(m.Result.q.run==2)

numberOfRegions = 0
amountOfPictures = 0
categories=dict()
for result in results:
	numberOfRegions = numberOfRegions + result.numberOfRegions
	amountOfPictures = amountOfPictures +1
	if result.numberOfRegions not in categories.keys():
		categories[result.numberOfRegions]=1
	else:
		categories[result.numberOfRegions]= categories[result.numberOfRegions]+1

print ('There was %i regions detected in %i pictures',(numberOfRegions,amountOfPictures))
print 'average was :%i',(numberOfRegions/amountOfPictures)
print categories
