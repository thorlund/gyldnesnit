import sys,os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

from src.settings import Settings
from src.settings import GlobalSettings
from src.lib import goldenLibrary

#This function should return a list of cuts you want send to the analyzer
def generateCuts():
	antalcuts = 9
	cuts = [goldenLibrary.PHI]
	while antalcuts > 0:
		oldcut = cuts[len(cuts)-1]
		newcut = oldcut +0.05
		if newcut > 1:
			newcut = newcut - 0.5
		cuts.append(newcut)
		antalcuts = antalcuts - 1
	return cuts
#The settings is passed thru here, to be modified if needed
def setSettings(settings):
	settings.setMarginPercentage(0.024)
	return 0

def setGlobalSettings(globalSettings):
	return 0

if __name__ == '__main__':
	print generateCuts()
