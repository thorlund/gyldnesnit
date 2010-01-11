def main():
	yerfile = open("yers_snitsU.txt")
	lines = yerfile.readlines()[0]
	#print lines
	lines = lines.split(")")
	lines.pop(16)
	size = len(lines)
	newfile0 = open('csv/yearcut0U.csv' , 'w' )
	newfile1 = open('csv/yearcut1U.csv' , 'w' )
	newfile2 = open('csv/yearcut2U.csv' , 'w' )
	newfile3 = open('csv/yearcut3U.csv' , 'w' )
	newfile0.write("\"ratios\",\"interessante regioner\"\n")
	newfile1.write("\"ratios\",\"interessante regioner\"\n")
	newfile2.write("\"ratios\",\"interessante regioner\"\n")
	newfile3.write("\"ratios\",\"interessante regioner\"\n")

	for line in lines:
		number = int(line.rstrip("(").split("}")[5].lstrip(", "))
		year = line.rstrip("(").lstrip(", ").split(" ")[0].rstrip("\\r\\n':").lstrip("'")
		hoisontal1 = line.rstrip("(").split("}")[0].lstrip("'" +year+ "': ([").lstrip("{").split(",")
		newfile0.write(str(year) + ', ' + str(int(hoisontal1[-1].split(": ")[1])/number) + "\n")

		hoisontal2 = line.rstrip("(").split("}")[1].lstrip(", {").lstrip("{").split(",")
		newfile1.write(str(year) + ', ' + str(int(hoisontal2[-1].split(": ")[1])/number) + "\n")

		vertikal1 = line.rstrip("(").split("}")[2].lstrip(", {").lstrip("{").split(",")
		newfile2.write(str(year) + ', ' + str(int(vertikal1[-1].split(": ")[1])/number) + "\n")
	
		vertikal2 = line.rstrip("(").split("}")[3].lstrip(", {").lstrip("{").split(",")
		newfile3.write(str(year) + ', ' + str(int(vertikal2[-1].split(": ")[1])/number) + "\n")

		dimontion = line.rstrip("(").split("}")[4].lstrip("], {")

	print number
if __name__ == "__main__":
	main()
