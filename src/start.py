#!/usr/bin/env python
"""
Quick n dirrrty test
"""

import sys,os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])
from lib import paintingAnalyzer
from lib import goldenLibrary
from lib import graphicHelper
from settings import Settings
from settings import GlobalSettings
from painting import Painting
import src.model as m
from database import Database
from experiments import tencuts as environment

def main():
	#Set this to true if you want to create a personal database
	testdatabase = False
	#Set this due to how large you want your testdatabase
	count = 10
	#creating a settings to be used with run
	cuts = environment.generateCuts()
	settings = Settings(cuts)
	environment.setSettings(settings)
	settings.setMethod("expanded")
	globalSettings = GlobalSettings()
	environment.setGlobalSettings(globalSettings)
	db = Database(globalSettings)
	#making a testdatabase if the varible is set
	if testdatabase == True:
		currentDBCount= m.Painting.select()).count()
		count = count - currentDBCount
		if count > 0:
			db.setCount(count)
			db.constructDatabase()
	else:
		db.constructDatabase()
	run = m.createNewRun(settings)
	paintings = m.Painting.select(m.Painting.q.form=="painting")
	for painting in paintings:
		if os.path.isfile(painting.filepath):
			try:
				paintingContainer = Painting(painting)
				print "working on"
				print painting.filepath
				paintingContainer.setResults(paintingAnalyzer.analyze(paintingContainer,settings))
				m.saveResults(run.id,paintingContainer)
			except:
				pass

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
