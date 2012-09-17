#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
#<img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" 
#/></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Tribute to my son</span> by 
#<a xmlns:cc="http://creativecommons.org/ns#" href="takenoko@home"
# property="cc:attributionName" rel="cc:attributionURL">Lucía B. Avalle</a> is licensed under a 
#<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">Creative Commons Attribution-ShareAlike 3.0
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
#       Natalia Bidart (nataliabidart at gmail dot com)
#######################################################################
#       Celia Cintas    (cintas.celia at gmail dot com) 
#just refactoring for the implementation of the db 

import sys
from loaddb import insert_data, dump_data, dump_data_in_range
from calculos import plot_data, do_spline, recenter, diff_integrate

try:
    import pylab
except ImportError:
    print('Please install python-matplotlib')
    sys.exit(1)


# controls if spline is applied to input data or not
DO_SPLINE = False

# location of db
MYDB = "../db/frank"
           
def usage_and_exit():
    program_name = sys.argv[0]
    msg = """Usage: %s <input-file> 

Example:
%s CVchapita08V.txt 
""" % (program_name, program_name)
    print(msg)
    sys.exit(1)

if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
       
    except Exception, e:
        usage_and_exit()

    # get initial data from db
    x_values, y_values = insert_data(input_file, MYDB)
    
    # plot initial data
    pylab.subplot(2,1,1)
    pylab.axhline() # draw line for y-coord 0
    plot_data(x_values, y_values, color='red', label='Initial data')
    dump_data_in_range(input_file, MYDB, x_values, y_values) #TODO llevar a la db los valores en rango
    if DO_SPLINE:
        # calculate spline
        plot_data(x_values, y_values, color='red', label='Initial')
        x_values, y_values = do_spline(x_values, y_values)
        plot_data(x_values, y_values, color='green', label='Splined')

    # recenter using X_0. If X_0 = None, the recenter is not applied.
    result = recenter(x_values, y_values)
    if result is not None:
        x_values, y_values = result
        pylab.subplot(2,1,2)
        pylab.axhline() # draw line for y-coord 0
        plot_data(x_values, y_values, color='green', label='Recentered')

    # calculate positive and negative integrals
    pos, neg = diff_integrate(x_values, y_values)

    # dump results to db with some sort of comment 
    dump_data(input_file, MYDB, [float(pos)], [float(neg)], "Integrals positive and negative")

    # show all the plots
    pylab.show()