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
def main():
	antalcuts = 9
	cuts = [goldenLibrary.PHI]
	while antalcuts > 0:
		oldcut = cuts[len(cuts)-1]
		newcut = oldcut +0.05
		if newcut > 1:
			newcut = newcut - 0.5
		cuts.append(newcut)
		antalcuts = antalcuts - 1
	settings = Settings(cuts)
	globalSettings = GlobalSettings()
	db = Database(globalSettings)
	#db.empy doesnt work since the database might be half full or half empty
	db.constructDatabase()
	run = m.createNewRun(settings)
	paintings = m.Painting.select(m.Painting.q.form=="painting")
	for painting in paintings:
		if os.path.isfile(painting.filepath):
			try:
				paintingContainer = Painting(painting)
				paintingContainer.setResults(paintingAnalyzer.analyze(paintingContainer,settings))
				m.saveResults(run.id,paintingContainer)
			except:
				pass

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
