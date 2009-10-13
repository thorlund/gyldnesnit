#!/usr/bin/env python
#
# Ulrik Bonde

"""
Compile and move libraries for testing
"""

import compileall
import glob, os, shutil

def init():
	"""Does it all"""
	src_dir = '../lib/'
	dst_dir = './lib/'

	# Initially, check if we are in the tests-directory
	# Monster ugly hack
	dir = os.getcwd()
	cwd = dir.split('/')[-1:][0]
	if not cwd == "tests":
		raise RuntimeError("Tests must be run from inside the tests directory. Sorry...")

	# Then, check if the destination exsist
	# If not, create it
	dir = os.path.join(dst_dir)
	if not os.path.isdir(dir):
		print "Destination folder does not exsist"
		print "Creating ./lib/"
		os.mkdir(dir)

	# First remove old compilations
	print "Cleaning destination"
	files = glob.iglob(os.path.join(dst_dir, "*.pyc"))
	for file in files:
		if os.path.isfile(file):
			os.remove(file)

	# Then compile the files in src/lib
	compileall.compile_dir(src_dir, force=True)
	
	# Finally move compiled files to src/tests/lib
	print "Moving compiled files"
	files = glob.iglob(os.path.join(src_dir, "*.pyc"))
	for file in files:
		if os.path.isfile(file):
			shutil.move(file, dst_dir)

if __name__ == "__main__":
	init()
