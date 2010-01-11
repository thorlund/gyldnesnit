def main():
	yerfile = open("yers_snits.txt")
	lines = yerfile.readlines()[0]
	#print lines
	lines = lines.split(")")
	lines.pop(16)
	size = len(lines)
	newfile0 = open('csv/yearcut0.csv' , 'w' )
	newfile1 = open('csv/yearcut1.csv' , 'w' )
	newfile2 = open('csv/yearcut2.csv' , 'w' )
	newfile3 = open('csv/yearcut3.csv' , 'w' )
	newfile0.write("\"ratios\",\"interessante regioner\"\n")
	newfile1.write("\"ratios\",\"interessante regioner\"\n")
	newfile2.write("\"ratios\",\"interessante regioner\"\n")
	newfile3.write("\"ratios\",\"interessante regioner\"\n")
	nulist = (lines[12],lines[10],lines[3],lines[8],lines[0],lines[6],lines[13],lines[5],lines[15],lines[2],lines[14],lines[7],lines[9],lines[11],lines[1],lines[4])
	for line in nulist:
		number = float(line.rstrip("(").split("}")[5].lstrip(", "))
		year = line.rstrip("(").lstrip(", ").split(" ")[0].rstrip("\\r\\n':").lstrip("'")
		if(number == 0):
			continue
		
		hoisontal1 = line.rstrip("(").split("}")[0].lstrip("'" +year+ "': ([").lstrip("{").split(",")
		newfile0.write(str(year) + ', ' + str(float(hoisontal1[-1].split(": ")[1])/number) + "\n")

		hoisontal2 = line.rstrip("(").split("}")[1].lstrip(", {").lstrip("{").split(",")
		newfile1.write(str(year) + ', ' + str(float(hoisontal2[-1].split(": ")[1])/number) + "\n")

		vertikal1 = line.rstrip("(").split("}")[2].lstrip(", {").lstrip("{").split(",")
		newfile2.write(str(year) + ', ' + str(float(vertikal1[-1].split(": ")[1])/number) + "\n")
	
		vertikal2 = line.rstrip("(").split("}")[3].lstrip(", {").lstrip("{").split(",")
		newfile3.write(str(year) + ', ' + str(float(vertikal2[-1].split(": ")[1])/number) + "\n")

		dimontion = line.rstrip("(").split("}")[4].lstrip("], {")

	print number
if __name__ == "__main__":
	main()
