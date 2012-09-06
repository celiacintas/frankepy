#!/usr/bin/env python
# coding=utf-8

#<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
#<img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" 
#/></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Tribute to my son</span> by 
#<a xmlns:cc="http://creativecommons.org/ns#" href="takenoko@home"
# property="cc:attributionName" rel="cc:attributionURL">Lucía B. Avalle</a> is licensed under a 
#<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">Creative Commons Attribution-ShareAlike 3.0
# Unported License</a>.
 
# Copyright 2010
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
#       Celia Cintas (cintas dot celia at gmail dot com)

# $ Other authors contributing to the code are indicated in the corresponding line$

try:
    from scipy import std
    from scipy.stats import linregress
except ImportError:
    print('Please install python-scipy')
    sys.exit(1)
try:
    import pylab
except ImportError:
    print('Please install python-matplotlib')
    sys.exit(1)


def do_std(values):
    """ give the standard deviation """
    return std(values)

def do_linealregression(x_values, y_values):
    """ """
    slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
    #print "slope", slope
    #print "intercept", intercept
    #print "r_value", r_value
    #print "p_value", std_err
    pylab.plot(x_values, y_values, 'bx')
    #pylab.plot(x_values, intercept + x_values, 'r-')
    
    pylab.show()

def plot_data(x_values, y_values, color, label):
    """Plot chart of x_values vs. y_values using color and label."""
    data, = pylab.plot(x_values, y_values, color=color, label=label)
    pylab.legend()
    pylab.xlabel('x')
    pylab.ylabel('y')