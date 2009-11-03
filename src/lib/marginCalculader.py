import math
# marginCalcualder taks are list of rations and return the max margin
# the lines can have i %
def marginCalculader(Rlist)
	size = len(Rlist)
	#the max magin that the function can return
	tmp = 100
	for i in range(0, size):
		for j in range(0, size):
			if abs(Rlist[i] - Rlist[j]) < tmp and not(j == i):
				tmp = abs(Rlist[i] - Rlist[j])
	return (tmp*100)/2.0
