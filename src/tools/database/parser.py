#!/usr/bin/env python
"""
Methods for parsing the csv-file from the repository
"""

def parseTechnique(str):
	"""
	Should return this: (technique, realHeight, realWidth) = parser.parseTechnique(line[4])
	"""
	return str

def yearParser(line):
	"""
	Dont't touch me!
	"""
	pass


def bornDied(str):
	"""A really really ugly parser for artist birth/death"""
	bornDied = []
	if str.startswith('(b.'):
		str = str.strip('()')
		str = str.split(',')
		for i in range(0, len(str), 2):
			tmp = str[i].strip('b. ca. d. after')
			bornDied.append(tmp)
	elif str.startswith('(active'):
		str = str.split('-')
		if len(str) == 1:
			print str
			# Says 1890s ish or other crap
			# Hohohohoh this is really ugly
			# Damn damn damn don't know why I am doing this
			# We could just throw a regular expression in
			year = ''
			tmp = str[0].split()
			tmpstr = []
			for token in tmp:
				if token.isalnum():
					tmpstr.append(token)
			str = " ".join(tmpstr)
			str = str.rstrip("s in ")
			year = int(str)
			str = [year, year+10]
		else:
			for i in range(len(str)):
				tmpstr = ''
				for c in str[i]:
					if not (c.isalpha() or c.isspace()):
						tmpstr += c
				# Evil removal of stupid years
				str[i] = tmpstr.split('/')[0]
		bornDied = str
	else:
		bornDied = "lort"
	return (bornDied[0], bornDied[1])


def main():
	line = "ALBANI, Francesco;(b. 1578, Bologna, d. ca. 1660, Bologna);The Annunciation;-;Oil on copper, 62 x 47 cm;The Hermitage, St. Petersburg;http://www.wga.hu/html/a/albani/annuncia.html;painting;religious;Italian;1601-1650"
#	line = "BRUGMAN, Willem Claesz.;(active 1641-1665);Candlestick;1652;Silver, height 32 cm, diameter 22 cm;Rijksmuseum, Amsterdam;http://www.wga.hu/html/b/brugman/candlest.html;metalwork;other;Dutch;1651-1700"
#	line = "CHRISTUS, Petrus;(active 1444-1475/76 in Bruges);Isabel of Portugal with St Elizabeth;1457-60;Oak panel, 59 x 33 cm;Groeninge Museum, Bruges;http://www.wga.hu/html/c/christus/2/isabel.html;painting;religious;Flemish;1451-1500"
#	line = "COESERMANS, Johannes;(active 1660s in Delft);Interior of the Nieuwe Kerk, Delft;1663;Pen painting in grisaille on wood, 52 x 45 cm;Private collection;http://www.wga.hu/html/c/coeserma/interior.html;painting;interior;Dutch;1651-1700"

	tokens = line.split(';')

	print bornDied(tokens[1])

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
