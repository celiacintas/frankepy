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
# $ Other authors contributing to the code are indicated in the corresponding line$

import csv
import sys
import sqlite3 as lite
from calculos import load_data, INTERVAL_START, INTERVAL_END

def insert_data(filename, mydb):
    """Insert data from file into db and return the x's y's values for ploting"""
    
    x_values, y_values = load_data(filename)
    try:
        con = lite.connect(mydb)
    
        cursor = con.cursor()
        cursor.execute("INSERT INTO muestra VALUES(NULL,?)", (str(filename),))
        cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
        id_muestra = cursor.fetchone()
        
        map(lambda pos : cursor.execute("INSERT INTO pos_in VALUES(?,NULL,?,?, NULL)", (id_muestra[0], float(pos[0]), float(pos[1]))), zip(x_values, y_values))
        con.commit()
        cursor.close()
        
        return x_values, y_values
    
    except lite.DatabaseError, e:
        print u"Data already in the db, working with them anywhere"
        
        return x_values, y_values
        
    except lite.Error, e:
       if con:
          con.rollback()
          print "Error %s:" % e.args[0]
          sys.exit(1)
       
    finally:
        if con:
           con.close() 

def dump_data(filename, mydb, x_values, y_values, about):
    """Dump values into the db """
    
    try:
        con = lite.connect(mydb)
    
        cursor = con.cursor()
        cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
        id_muestra = cursor.fetchone()
        
        map(lambda pos : cursor.execute("INSERT INTO pos_out VALUES(?, NULL,?,?,?, NULL, NULL, NULL)", (id_muestra[0], about, float(pos[0]), float(pos[1]))), zip(x_values, y_values))
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
           
def dump_data_in_range(filename, mydb, x_values, y_values):
    """Dump values in certain range into the db """
    #this part of the code is from Lucia, just adding map for dump in the db
    
    filter_function = lambda (x, y): INTERVAL_START <= x <= INTERVAL_END
    if INTERVAL_START > INTERVAL_END:
        print('NOTICE: The interval start %s is bigger than the interval end %s, using all the data.' %
              (INTERVAL_START, INTERVAL_END))
        interval_values = zip(x_values, y_values)
    else:
        print('NOTICE: Calculating integrals for every value in the closed interval [%s, %s].' %
              (INTERVAL_START, INTERVAL_END))
        interval_values = filter(filter_function, zip(x_values, y_values))
        
    try:
        con = lite.connect(mydb)
    
        cursor = con.cursor()
        cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
        id_muestra = cursor.fetchone()
        
        map(lambda values : cursor.execute("INSERT INTO pos_out VALUES(?, NULL, NULL, ?, ?, NULL, ?, ?)", 
        (id_muestra[0], float(values[0])/1.0, float(values[1]), INTERVAL_START, INTERVAL_END)), interval_values)
        
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
    pass
    