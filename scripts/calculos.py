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
#       Natalia Bidart (nataliabidart at gmail dot com)

# $ Other authors contributing to the code are indicated in the corresponding line$

import csv
import sys

try:
    import pylab
except ImportError:
    print('Please install python-matplotlib')
    sys.exit(1)

try:
    from numpy import linspace, random
    from scipy import interpolate, integrate
except ImportError:
    print('Please install python-numpy')
    sys.exit(1)

try:
    from scipy import interpolate, integrate
except ImportError:
    print('Please install python-scipy')
    sys.exit(1)

# controls if spline is applied to input data or not
DO_SPLINE = False

# x-coord to be used to re-center the graphic on y-coord.
# Use X_0 = None to avoid recentering
X_0 = None

DELIMITER_IN = ' '  # delimiter to read input data, change to whatever you need
DELIMITER_OUT = ' ' # delimiter to store output data, change to whatever you need
DELIMITER_ASCII_OUT = ' ' # delimiter to store ascii data, change to whatever you need

COLUMN_X = 0 # 0-based column index to read data from to build x-values
COLUMN_Y = 1 # 0-based column index to read data from to build y-values
INTERVAL_START = 0.269165039062500000# x-coord indicating the start of the interval to calculate
                   
INTERVAL_END = 0.279235839843750000# x-coord indicating the end of the interval to calculate
                   
def usage_and_exit():
    program_name = sys.argv[0]
    msg = """Usage: %s <input-file> <output-file> <ascii-file> <ascii_selected_range-file>

Example:
%s CVchapita08V.txt test.txt ascii.txt ascii_selected_range-file.txt
""" % (program_name, program_name)
    print(msg)
    sys.exit(1)

def formateo(filename):
	fi = open(filename)
	lines = fi.readlines()
	newlines = []
	for l in lines:
		newlines.append(l.replace("   "," "))
	#TODO terminar
def load_data(filename):
    """Load data from file at location filename."""

    x_values = []
    y_values = []
    #parche para archivos con varios espacios
    formateo(filename)
    f = open(filename, 'r')
    reader = csv.reader(f, delimiter=DELIMITER_IN)
    for line in reader:
        try:
            x, y = float(line[COLUMN_X]), float(line[COLUMN_Y])
            x_values.append(x)
            y_values.append(y)
        except IndexError:
            print('Index error when accessing values for line %s' % (line,))
        except ValueError:
            print('Cast error when converting to float for line %s' % (line,))

    f.close()

    return x_values, y_values

def plot_data(x_values, y_values, color, label):
    """Plot chart of x_values vs. y_values using color and label."""
    data, = pylab.plot(x_values, y_values, color=color, label=label)
    pylab.legend()
    pylab.xlabel('x')
    pylab.ylabel('y')

def do_spline(x_values, y_values):
    """Attempt to use spline interpolation using scipy's library."""

    # ATTENTION: current implementation of spline does not work for
    # the samples CVchapita05Videm.txt and CVchapita08V.txt
    # The underlying Fortran rutine fails with no further information.

    # spline parameters
    s=3.0  # smoothness parameter
    k=3    # spline order
    nest=2 # estimate of number of knots needed (-1 = maximal)

    # find the knot points
    tckp, u = interpolate.splprep([x_values, y_values], s=s, k=k, nest=nest)
    interpolate.splrep(x_values, y_values, k=2, s=3.0, quiet=0)

    # evaluate spline, including interpolated points
    xnew, ynew = interpolate.splev(u, tckp)

    return xnew, ynew

def recenter(x_values, y_values):
    """Recenter x_values and y_values over x and y axis respectively."""

    if X_0 is None:
        print('NOTICE: value X_0 is None, skipping recentering.')
        return

    # filter all y-values that match the X_0 constant
    matches = filter(lambda (x, y): x == X_0, zip(x_values, y_values))
    if len(matches) <= 0:
        print('NOTICE: value X_0 = %s was not found in the x-values, skipping recentering.' % X_0)
        return

    # calculate average between the max and min values
    y_max = max(matches)[1]
    y_min = min(matches)[1]
    delta = y_max - (y_min + y_max) / 2.0
    print('NOTICE: adding delta %s to every y-value to recenter.' % delta)
    # add delta to every y-value
    y_values = map(lambda y: y + delta, y_values)
    return x_values, y_values

def diff_integrate(x_values, y_values):
    positive_res = 0
    negative_res = 0

    filter_function = lambda (x, y): INTERVAL_START <= x <= INTERVAL_END
    if INTERVAL_START > INTERVAL_END:
        print('NOTICE: The interval start %s is bigger than the interval end %s, using all the data.' %
              (INTERVAL_START, INTERVAL_END))
        interval_values = zip(x_values, y_values)
    else:
        print('NOTICE: Calculating integrals for every value in the closed interval [%s, %s].' %
              (INTERVAL_START, INTERVAL_END))
        interval_values = filter(filter_function, zip(x_values, y_values))

    positive_x_values = []
    positive_y_values = []
    negative_x_values = []
    negative_y_values = []
    # split positive and negative y-values
    for x, y in interval_values:
        if y < 0:
            negative_x_values.append(x)
            negative_y_values.append(y)
        else:
            positive_x_values.append(x)
            positive_y_values.append(y)

    positive_res = integrate.trapz(positive_y_values, positive_x_values)
    negative_res = integrate.trapz(negative_y_values, negative_x_values)

    return positive_res, negative_res

def dump_data(output_file, pos, neg):
    f = open(output_file, 'w')
    values = map(str, (INTERVAL_START, INTERVAL_END, pos, neg))
    result = DELIMITER_OUT.join(values)
    print 'RESULT', result
    f.write(result + '\n')
    f.close()

def save_ascii_selected_range(ascii_selected_range_output_file, x_values, y_values): #This piece of code was modified by Lucia B. Avalle!!

    #f = open(ascii_selected_range_output_file, 'w')

    filter_function = lambda (x, y): INTERVAL_START <= x <= INTERVAL_END
    if INTERVAL_START > INTERVAL_END:
        print('NOTICE: The interval start %s is bigger than the interval end %s, using all the data.' %
              (INTERVAL_START, INTERVAL_END))
        interval_values = zip(x_values, y_values)
    else:
        print('NOTICE: Calculating integrals for every value in the closed interval [%s, %s].' %
              (INTERVAL_START, INTERVAL_END))
        interval_values = filter(filter_function, zip(x_values, y_values))
        for value in interval_values:
            f.write("%.18f %s %.18f\n" % ((value[0] / 1.0), DELIMITER_ASCII_OUT, (value[1])))
#            f.write("%.18f %s %.18f\n" % ((value[0] - 3.388), DELIMITER_ASCII_OUT, (value[1]/1000)))
    f.close()

def save_ascii(ascii_file, x_values, y_values):
    "Save the data to a file"
    values = zip(x_values, y_values)
    f = open(ascii_file, 'w')
    for value in values:
        f.write("%.18f %s %.18f\n" % (value[0], DELIMITER_ASCII_OUT, value[1]))
    f.close()

if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        ascii_file = sys.argv[3]
        ascii_selected_range_output_file = sys.argv[4]
    except Exception, e:
        usage_and_exit()

    # get initial data from file
    x_values, y_values = load_data(input_file)

    # plot initial data
    pylab.subplot(2,1,1)
    pylab.axhline() # draw line for y-coord 0
    plot_data(x_values, y_values, color='red', label='Initial data')
    save_ascii(ascii_file, x_values, y_values)
    save_ascii_selected_range(ascii_selected_range_output_file, x_values, y_values)

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

    # show results and dump to file
    dump_data(output_file, pos, neg)

    # show all the plots
    pylab.show()
