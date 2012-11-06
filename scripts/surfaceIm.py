#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<a rel="license"
#href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
#<img alt="Creative Commons License" style="border-width:0"
#src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png"
#/></a><br /><span xmlns:dct="http://purl.org/dc/terms/"
#property="dct:title">Tribute to my son</span> by
#<a xmlns:cc="http://creativecommons.org/ns#" href="takenoko@home"
# property="cc:attributionName" rel="cc:attributionURL">Lucía B. Avalle</a>
#is licensed under a <a rel="license"
#href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
#Creative Commons Attribution-ShareAlike 3.0
# Unported License</a>.
# Copyright 2012
# Lucía B. Avalle
# Grupo de Electroquímica Experimental y Teórica, FaMAF, UNC
# Córdoba, Argentina

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
#       Celia Cintas    (cintas.celia at gmail dot com)
# $ Other authors contributing to the code are indicated in the corresponding
# line$

import sys
import argparse
try:
	import numpy as np
except ImportError:
	print "please install numpy"
	sys.exit(1)
try:
	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt
except ImportError:
	print "please install matplotlib"
	sys.exit(1)
try:
	import Image
except ImportError:
	print "please install Image"
	sys.exit(1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='For surface drawing')
    	parser.add_argument("-f", "--file", dest="file", help='This option is used to pass the image file')
        args = parser.parse_args()  	
	if args.file:
		im = Image.open(args.file).convert("L")
		myArrayIm = np.asarray(im)
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		Z = z = myArrayIm
		x = np.arange(0, im.size[0])
		y = np.arange(0, im.size[1])
		X, Y = np.meshgrid(x, y)
		ax.plot_surface(X, Y, Z)

		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')

		plt.show()
