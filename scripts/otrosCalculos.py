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


from loaddb import insert_data, dump_data, MYDB
from os import path
from calculos import DELIMITER_ASCII_OUT
import argparse


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


def save_ascii(ascii_file, x_values, y_values):
    "Save the data to a file"
    values = zip(x_values, y_values)
    f = open(ascii_file, 'w')
    for value in values:
        f.write("%s %s %.18f\n" % (value[0], DELIMITER_ASCII_OUT, value[1]))
    f.close()

def do_std(values):
    """ give the standard deviation """
    return std(values)

def do_linealregression(x_values, y_values):
    """ """
    slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
    print "slope", slope
    print "intercept", intercept
    print "r_value", r_value
    print "p_value", std_err
    #pylab.plot(x_values, y_values, 'bx')
    #pylab.plot(x_values, intercept + x_values, 'r-')
    #pylab.show()
    return [slope, intercept, r_value, p_value, std_err]

def plot_data(y_values, about, title):
    """Plot chart of x_values vs. y_values using color and label."""
    data, = pylab.plot(y_values)
    pylab.legend()
    pylab.title(title)
    pylab.text(400, -0.0002, about, {'color': 'g', 'fontsize': 15})
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.savefig("../plots/matplot2std.png", dpi = 100)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='For test linealregression and standar desviation')
    parser.add_argument("-f", "--file", dest="file", help='This option is used to pass the data file')
    args = parser.parse_args()    
    #nos aseguramos de guardar en la db el archivo
    x_values, y_values = insert_data(args.file, MYDB)
    #obtain de std of y values
    desviation_y = do_std(y_values)
    #dump into the db
    dump_data(args.file, MYDB, [None], [desviation_y], "std")
    plot_data(y_values,  r'$\sigma = %.18f $' %(desviation_y), "y_values and std")
    #do the same with lineal regression 
    results_lineal = do_linealregression(x_values, y_values)
    labels = ['slope', 'intercept', 'r_value', 'p_value']

    for value, about in zip(results_lineal, labels):
        dump_data(args.file, MYDB, [None], [value], about)
        filename = "../fileTest/liear_fit" + path.basename(args.file)
        save_ascii(filename, labels, results_lineal)
    pylab.show()
