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
#       Celia Cintas    (cintas.celia at gmail dot com)
# $ Other authors contributing to the code are indicated in the corresponding 
#line$

import sys
import argparse
from os import path, listdir
from repositorio import Repositorio

# location of db
MYDB = "../db/frank"

def insert_multiple_files(dirFiles, mydb = MYDB):
     """Get the files from a dir and dumped into the db"""
	
     files = listdir(dirFiles)
     for f in files:
         myDB.insert_data(path.join(dirFiles, f))



def usage_and_exit():
    program_name = sys.argv[0]
    msg = """Usage: %s <input-file> 

Example:
%s CVchapita08V.txt 
""" % (program_name, program_name)
    print(msg)
    sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""For getting and dumping data
                                                  into the db""")
    parser.add_argument("--get", dest="get", help="""This option is used to
    obtain data of the db, you have to pass the filename""")
    parser.add_argument("--get-lineal-r", dest="get_lineal", help="""This
    option is used to obtain the values of lineal regression of the db,
    you have to pass the filename""")
    parser.add_argument("--put", dest="put", help="""This is for dump values
    into the db, you have to pass the filename or a path""")
    args = parser.parse_args()

    myDB = Repositorio(MYDB)
    if args.get:
        if path.isfile(args.get):
            #its a file not just a part of the name
            values = myDB.get_original_data(args.get)
            x_processed_values, y_processed_values = myDB.get_processed_data(args.get)
            print x_values, y_values
        else:
            #its a RE
            descriptions = myDB.get_filenames_with_re(args.get)
            x_values = []; y_values = []
            x_total_proc_values = []; y_total_proc_values = []

            for d in descriptions:
                values = myDB.get_original_data(d)
                x_values += values[0]
                y_values += values[1]

                xps, yps = myDB.get_processed_data(d)
                x_total_proc_values += xps
                y_total_proc_values += yps
		    
		print x_values, y_values
    #Now we can do something with this values...
    if args.put:
        if path.isfile(args.put):
            myDB.insert_data(args.put)
        else:
            insert_multiple_files(args.put)
    if args.get_lineal:
        std, slope, intercept, r_value, p_value = myDB.get_lineal_regression(args.get_lineal)
        #do something with this values
        print """
            std : %1.8f 
            slope : %1.8f 
            intercept : %1.8f
            r_value : %1.8f 
            p_value : %1.8f """ % (std, slope, intercept, r_value, p_value)
