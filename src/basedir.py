#!/usr/bin/env python
"""
Very clever hack for finding the project basedir.

Finds the first occurrence of 'src' in the absolute current work directory.

Only tested on linux
"""

import sys, os
sys.path.append(os.getcwd()[:os.getcwd().find('src')])

# vim: set noexpandtab tabstop=4 softtabstop=4 shiftwidth=4 :
