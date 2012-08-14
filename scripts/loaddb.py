#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
#       Natalia Bidart (nataliabidart at gmail dot com)

# $ Other authors contributing to the code are indicated in the corresponding line$
import csv
import sys
import sqlite3 as lite

DELIMITER_IN = ' '  # delimiter to read input data, change to whatever you need
DELIMITER_OUT = ' ' # delimiter to store output data, change to whatever you need
DELIMITER_ASCII_OUT = ' ' # delimiter to store ascii data, change to whatever you need

COLUMN_X = 0 # 0-based column index to read data from to build x-values
COLUMN_Y = 1 # 0-based column index to read data from to build y-values

def load_data(filename):
    """Load data from file at location filename."""

    x_values = []
    y_values = []

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

def insert_data(filename, x_values, y_values, mydb):
    """Insert data into db"""
    
    try:
        con = lite.connect(mydb)
    
        cursor = con.cursor()
        cursor.execute("INSERT INTO muestra VALUES(NULL,?)", (str(filename),))
        cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
        id_muestra = cursor.fetchone()
        
        map(lambda pos : cursor.execute("INSERT INTO pos VALUES(?,NULL,?,?)", (id_muestra[0], float(pos[0]), float(pos[1]))), zip(x_values, y_values))
        con.commit()
        cursor.close()
        
    except lite.Error, e:
       if con:
          con.rollback()
          print "Error %s:" % e.args[0]
          sys.exit(1)
       
    finally:
        if con:
           con.close() 

 
if __name__ == '__main__':
    x, y = load_data("/home/celita/Documentos/FaMAF/requerimientos/12096-CV.txt")
    insert_data("/home/celita/Documentos/FaMAF/requerimientos/12096-CV.txt", x, y, "/home/celita/Documentos/FaMAF/Frankepy/frank")
    