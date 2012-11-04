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
import re
import sys
import sqlite3 as lite
import argparse
from os import path, listdir
#from calculos import load_data, INTERVAL_START, INTERVAL_END
from numpy import genfromtxt


class Repositorio:
    def __init__(self, location):
        self.position = location

    def insert_data(self, filename):
        """Insert data from file into db and return the
        x's y's values for ploting"""
        try:
            con = lite.connect(self.position)
            values = genfromtxt(filename)

            #sacamos todos los valores nan que contenga
            filter(lambda v: v != 'nan', values)

            cursor = con.cursor()
            #obtain the basename of the file for save into the db
            filename = path.basename(filename)
            cursor.execute("INSERT INTO muestra VALUES(NULL,?)",
                           (str(filename),))
            cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",
                           (str(filename),))
            id_muestra = cursor.fetchone()

            if values[0].size == 3: # We have x y z
                map(lambda value : cursor.execute("INSERT INTO pos_in VALUES(?,NULL,?,?,?)", (id_muestra[0], value[0], value[1], value[2])), values)
            elif values[0].size == 2: #We have x y 
                map(lambda value : cursor.execute("INSERT INTO pos_in VALUES(?,NULL,?,?,NULL)",(id_muestra[0], value[0], value[1])), values)
            con.commit()
            cursor.close()
            return self.get_values(values)

        except lite.DatabaseError, e:
            print u"Data already in the db, working with them anywhere"
            return self.get_values(values)

        except lite.Error, e:
            if con:
                con.rollback()
                print "Error %s:" % e.args[0]
	        sys.exit(1)
        finally:
            if con:
                con.close()
    
    def get_values(self, values):
        """changes to x y (or z) from the values of genfromtxt"""
        myNewValues = []
        for i in range(values[0].size):
            #get if we have xy or xyz
            myNewValues.append([])
            for j in range(len(values)-1):
                myNewValues[i].append(values[j][i])

        return myNewValues
                
        
    def dump_data(self,filename, x_values, y_values, about):
        """Dump values into the db """
        try:
            con = lite.connect(self.position)
    
            cursor = con.cursor()
            filename = path.basename(filename)
            cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
            id_muestra = cursor.fetchone()
        
            map(lambda pos : cursor.execute("INSERT INTO pos_out VALUES(?, NULL,?,?,?, NULL, NULL, NULL)", (id_muestra[0], 
                                            about, pos[0], pos[1])), zip(x_values, y_values))
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
           
    def dump_data_in_range(self, filename, x_values, y_values):
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
            con = lite.connect(self.position)
                 
            cursor = con.cursor()
            filename = path.basename(filename)
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

    def get_original_data(self, filename):
        """Get original values (pos_in) of the db """
    
        
        try:
            con = lite.connect(self.position)
        
            cursor = con.cursor()
            filename = path.basename(filename)
            
            cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
            id_muestra = cursor.fetchone()
            if id_muestra:
                x_values = []
                y_values = []
                z_values = []
                for row in cursor.execute("SELECT x,y,z FROM pos_in WHERE id_muestra = ? AND z != NULL",(id_muestra[0],)):
                    x_values.append(row[0])
                    y_values.append(row[1])
                    z_values.append(row[2])
   		if not (x_values and y_values and z_values): 
			 for row in cursor.execute("SELECT x,y FROM pos_in WHERE id_muestra = ?",(id_muestra[0],)):
                    		x_values.append(row[0])
                    		y_values.append(row[1])
                
		
            else:
                 print "These values are not found in the database. Please use --put First"
                 sys.exit(1)     
            cursor.close()
            
            return [x_values, y_values, z_values] 
            
        except lite.Error, e:
           if con:
              con.rollback()
              print "Error %s:" % e.args[0]
              sys.exit(1)
           
        finally:
            if con:
               con.close() 

    def get_processed_data(self, filename):
        """Get processed values (pos_out) of the db """
    
        try:
            con = lite.connect(self.position)
        
            cursor = con.cursor()
            filename = path.basename(filename)
            
            cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",
                           (str(filename),))
            id_muestra = cursor.fetchone()
            if id_muestra:
                x_values = []
                y_values = []
                for row in cursor.execute("SELECT x,y FROM pos_in WHERE id_muestra = ?",
                                          (id_muestra[0],)):
                    x_values.append(row[0])
                    y_values.append(row[1])
            else:
                print "These values are not found in the database. Please use --put First"
                sys.exit(1)        
                
            cursor.close()
            
            return x_values, y_values
        except lite.Error, e:
           if con:
              con.rollback()
              print "Error %s:" % e.args[0]
              sys.exit(1)
           
        finally:
            if con:
               con.close() 

    def get_lineal_regression(self, filename):
        try:
            con = lite.connect(self.position)
        
            cursor = con.cursor()
            filename = path.basename(filename)
            
            cursor.execute("SELECT id_muestra FROM muestra WHERE descripcion = ?",(str(filename),))
            id_muestra = cursor.fetchone()
            if id_muestra:
                cursor.execute("SELECT y FROM pos_out WHERE id_muestra = ? AND about = 'std'",(id_muestra[0],))
    	    	std = cursor.fetchone()
                cursor.execute("SELECT y FROM pos_out WHERE id_muestra = ? AND about = 'slope'",(id_muestra[0],))
    	    	slope = cursor.fetchone()
                cursor.execute("SELECT y FROM pos_out WHERE id_muestra = ? AND about = 'intercept'",(id_muestra[0],))
    	    	intercept = cursor.fetchone()
                cursor.execute("SELECT y FROM pos_out WHERE id_muestra = ? AND about = 'r_value'",(id_muestra[0],))
    	    	r_value = cursor.fetchone()
                cursor.execute("SELECT y FROM pos_out WHERE id_muestra = ? AND about = 'p_value'",(id_muestra[0],))
    	   	p_value = cursor.fetchone()
        
            else:
                print "These values are not found in the database. Please use otrosCalculos  First"
                sys.exit(1)        
                
            cursor.close()
            
            return std[0], slope[0], intercept[0], r_value[0], p_value[0]
    
        except lite.Error, e:
           if con:
              con.rollback()
              print "Error %s:" % e.args[0]
              sys.exit(1)
           
        finally:
            if con:
               con.close() 
               
    def get_filenames_with_re(self, name):
        """Get the descriptions that start with name """
    
        try:
            con = lite.connect(self.position)
        
            cursor = con.cursor()
    	#we tell to the db we only want description that start with 'name'
            rex = '^' + name 
    	    descripciones = []
    	    for row in  cursor.execute("SELECT descripcion FROM muestra"):
    		if (re.match(rex,row[0])):
    			descripciones.append(row[0])
            if not descripciones:
                print "These values are not found in the database. Please use --put First"
                sys.exit(1)        
                
            cursor.close()
            
            return descripciones
    
        except lite.Error, e:
           if con:
              con.rollback()
              print "Error %s:" % e.args[0]
              sys.exit(1)
           
        finally:
            if con:
               con.close() 
    
