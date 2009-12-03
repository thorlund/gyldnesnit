import sys,os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

from settings import Settings
from settings import GlobalSettings
from lib import goldenLibrary

#This function should return a list of cuts you want send to the analyzer
def generateCuts():
	return [goldenLibrary.PHI]
#The settings is passed thru here, to be modified if needed
def setSettings(settings):
	settings.setMarginPercentage(0.024)
	return 0

def setGlobalSettings(globalSettings):
	return 0
