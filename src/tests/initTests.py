"""Compile and move libraries for testing"""

import compileall
import glob, os, shutil

def init():
	"""Does it all"""
	src_dir = '../lib/'
	dst_dir = './lib/'

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
