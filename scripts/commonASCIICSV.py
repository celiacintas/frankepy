# coding=utf-8

# Copyright 2010
# Lucía B. Avalle
#Group of Electrochemistry. Experimental and Theoretical Aspects. Institut of Physics Enrique Gaviola (IFEG), FaMAF, UNC
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
#       Matias Bordese (mbordese at gmail dot com)
#       Natalia Bidart (nataliabidart at gmail dot com)
#       Leoncio Juan Ernesto L\'opez (anicholo at gmail dot com)
# $ Id: TransientLaplace.py 7 2010-05-25 20:51:48Z nessita $

import csv
import sys

from numpy import arange

def parse_params():
    """ Set a params dictionary with the values of the arguments passed """
    params = {}
    for argument in sys.argv[1:]:
        option, value = argument.split('=')
        params[option] = value

    return params

def get_values_from_file_csv(filename, row=0, col=0):
    """ Get values from the given column of filename csv file,
        starting from the given row"""
    ret = []
    row = int(row)
    col = int(col)
    f = open(filename, 'r')
    reader = csv.reader(f)

    # ignore the first row lines
    for i in range(row):
        reader.next()

    # get the col value for the following lines
    for line in reader:
        try:
            ret.append(float(line[col]))
        except ValueError:
            print 'Error de casting a float para la linea', line
            sys.exit(1)
    f.close()

    return ret

def get_values_from_file_ascii (filename, row=0, col=0):
    """ Get values from file in ascii format"""
    ret = []
    row = int(row)
    col = int(col)
    f = open(filename, 'r')

    # ignore the first row lines
    for i in range(row):
        f.next()

    for line in f:
        try:
            values = line.split(' ')
            ret.append(float(values[col]))
        except ValueError:
            print 'Error of casting a float for line', line
            sys.exit(1)
    f.close()

    return ret

def generate_values(start, end, step=1):
    """ Generate values from start to end by the given step """
    start = float(start)
    end = float(end)
    step = float(step)
    return arange(start, end, step)

def get_values_from(desc, format='ascii'):
    """ Get values for variable according to description:
            file:filename:row:col
            range:start:end:step
    """
    values = desc.split(':')
    if values[0]=='file':
        if format == 'csv':
            ret = get_values_from_file_csv(*values[1:])
        elif format == 'ascii':
            ret = get_values_from_file_ascii(*values[1:])
        else:
            print "Error: Unknown file format"
            usage_and_exit()
    elif values[0]=='range':
        ret = generate_values(*values[1:])
    else:
        usage_and_exit()
    return ret

def dump_data(filename, values, cols=None):
    """ Dump the results to the given file,
        or if not specified to standard output """
    if filename:
        outfile = open(filename, 'w')
    else:
        outfile = sys.stdout

    res_writer = csv.writer(outfile)
    if cols:
        for r in values:
            row = [r[i] for i in cols]
            res_writer.writerow(row)
    else:
        res_writer.writerows(values)
    outfile.write('\n')

    if filename:
        outfile.close()

