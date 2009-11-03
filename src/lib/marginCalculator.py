import math
# marginCalcualder taks are list of rations and return the max margin
# the lines can have i %
def getPercentage(Rlist):
	size = len(Rlist)
	#the max magin that the function can return
	tmp = 100
	for i in range(0, size):
		for j in range(0, size):
			if abs(Rlist[i] - Rlist[j]) < tmp and not(j == i):
				tmp = abs(Rlist[i] - Rlist[j])
	return (tmp)/2.0
	
def getPixels(image, line, marginPercentage):
	
	(p1, p2) = line.getPoints()
	if p1.x == p2.x:
		# Initialize the seed and set deltas for increasing the seed
		tmp = int(image.width * marginPercentage)
	elif p1.y == p2.y:
		tmp = int(image.height * marginPercentage)
	else:
		raise lib.OrientationException("Unknown orientation")
	return tmp
