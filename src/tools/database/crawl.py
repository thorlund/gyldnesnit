#!/usr/bin/python
import os
##
# This is a crawler of wga.hu, it works on thier csv catalog, that has to be place in the same document.
# How is works should be rather clear due to the fact that is it 8 lines of code ^^
#
#
##

f=open('catalog.csv','r')
for line in f:
	splittedline=line.split(';')
	if splittedline[4].find("Oil")!=-1:
		url = splittedline[6]
		url = url.replace('html','art',1)
		url = url.replace('html','jpg')
		print('wget ' + url)
		os.system('wget ' + url)
