#"""
#Provides functionality for running FloodFill on images
#"""

# Import basic functionality
import goldenLibrary
import random


# Import what we need from OpenCV
from opencv import cv

#floofill the image at point x,y whit are lower andt opper thres hold of lo and up
def floofill(image,lo,up,point):

	# runing floodfil on the picture	
	b = random.randint(0,255)
	g = random.randint(0,255)
	r = random.randint(0,255)
	
	# color the fill whill be
	color = cv.CV_RGB(r,g,b);
	
	#x,y cordinats 
	seed = point
	
	cv.cvFloodFill(image,seed,color, cv.CV_RGB(lo,lo,lo), cv.CV_RGB(up,up,up))

	return image
