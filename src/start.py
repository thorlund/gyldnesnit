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
	settings = Settings([0.66666,goldenLibrary.PHI])
	globalSettings = GlobalSettings()
	db = Database(globalSettings)
	#db.empy doesnt work since the database might be half full or half empty
	db.constructDatabase()
	run = m.createNewRun(settings)
	paintings = m.Painting.select(m.Painting.q.form=="painting")
	for painting in paintings:
		if os.path.isfile(painting.filepath):
			paintingContainer = Painting(painting)
			paintingContainer.setResults(paintingAnalyzer.analyze(paintingContainer,settings))
			m.saveResults(run.id,paintingContainer)

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
