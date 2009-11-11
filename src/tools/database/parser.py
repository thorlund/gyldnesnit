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


def dateParser(str):
	"""
	Agressive parser.
	dates on the form yyyy-xx will be represented as yyyy. Punktum.
	"""
	if str == '-':
		return None
	str = str.rstrip('s').split('-')[0]
	return int(str)


def bornDied(str):
	"""
	A really really ugly parser for artist birth/death.
	I'm a really really deeply sorry for this piece of shit-code :(
	
	We have a finite number of variants (yyyy is year, ex. 1780):

	1. '(b. yyyy, Glostrup, d. yyyy, Haslev)'
	2. '(b. ca. yyyy, Glostrup, d. yyyy, Haslev)'
	3. '(b. yyyy, Glostrup, d. ca. yyyy, Haslev)'
	4. '(b. ca. yyyy, Glostrup, d. ca. yyyy, Haslev)'
	5. '(active yyyy-yyyy)'
	6. '(active yyyy-yyyy in Taastrup)'
	7. '(active yyyy-yyyy/yy)'
	8. '(active yyyy-yyyy/yy in Taastrup)'
	9. '(active yyyys in Vietnam)' dvs. '(active 1210s in Nam)'

	Parsing:

	* Everything 'ca.' will be ignored.
	* Places are ignored.
	* Active replaces born/died.
	* Years on the form yyyy/yy we use only the first year (str.split('/')[0])
	* 1460s is parsed as [yyyy, yyyy + 10], i.e. 1460 - 1470

	return an (int, int)-tuple
	"""

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
				# Again, sorry
				str[i] = tmpstr.split('/')[0].strip('()')
		bornDied = str
	else:
		return (None, None)
	return (int(bornDied[0]), int(bornDied[1]))


def main():
#	line = "ALBANI, Francesco;(b. 1578, Bologna, d. ca. 1660, Bologna);The Annunciation;-;Oil on copper, 62 x 47 cm;The Hermitage, St. Petersburg;http://www.wga.hu/html/a/albani/annuncia.html;painting;religious;Italian;1601-1650"
#	line = "BRUGMAN, Willem Claesz.;(active 1641-1665);Candlestick;1652;Silver, height 32 cm, diameter 22 cm;Rijksmuseum, Amsterdam;http://www.wga.hu/html/b/brugman/candlest.html;metalwork;other;Dutch;1651-1700"
#	line = "CHRISTUS, Petrus;(active 1444-1475/76 in Bruges);Isabel of Portugal with St Elizabeth;1457-60;Oak panel, 59 x 33 cm;Groeninge Museum, Bruges;http://www.wga.hu/html/c/christus/2/isabel.html;painting;religious;Flemish;1451-1500"
	line = "COESERMANS, Johannes;(active 1660s in Delft);Interior of the Nieuwe Kerk, Delft;1663;Pen painting in grisaille on wood, 52 x 45 cm;Private collection;http://www.wga.hu/html/c/coeserma/interior.html;painting;interior;Dutch;1651-1700"

	tokens = line.split(';')

	print bornDied(tokens[1])

if __name__ == '__main__':
	main()

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
