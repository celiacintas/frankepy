#!/usr/bin/env python
# coding=utf-8

# coding=utf-8

# Copyright 2012
# Lucía B. Avalle
#Group of Electrochemistry. Experimental and Theoretical Aspects. Institut of Physics Enrique Gaviola (IFEG), FaMAF, UNC
# Córdoba, Argentina

#<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Tribute to my son</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="takenoko@home" property="cc:attributionName" rel="cc:attributionURL">Lucía B. Avalle</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.

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
#       Leoncio Juan Ernesto L\'opez (anicholo at gmail dot com)
#       Just refactoring for the db (Celia Cintas - cintas.celia at gmail dot com)
 
from commonASCIICSV import get_values_from, generate_values
from loaddb import dump_data

MYDB = "../db/frank"
ABOUT = "Descripcion de que grafico representa"

FILE_1 = "/home/lucia/Documents/TiO2/Ellipsometry/DifferentThickness/Electrode3/Elec3N2Tau1sRange.txt"
FILE_2 = "/home/lucia/Documents/TiO2/Ellipsometry/DifferentThickness/Electrode3/Elec3O2Tau1sRange.txt"
FILE_3 = "/home/lucia/Documents/TiO2/Ellipsometry/DifferentThickness/Electrode3/Elec3N2Tau2sRange.txt"
FILE_4 = "/home/lucia/Documents/TiO2/Ellipsometry/DifferentThickness/Electrode3/Elec3O2Tau2sRange.txt"
# Get the params
params = {}
params['i1'] = "file:%s:0:1" %(FILE_1) #refactoring for dumping into db
params['t1'] = "file:%s:0:0" %(FILE_1)
params['i2'] = "file:%s:0:1" %(FILE_2)
params['t2'] = "file:%s:0:0" %(FILE_2)
params['i3'] = "file:%s:0:1" %(FILE_3)
params['t3'] = "file:%s:0:0" %(FILE_3)
params['i4'] = "file:%s:0:1" %(FILE_4)
params['t4'] = "file:%s:0:0" %(FILE_4)

# Set the variable values according to the given params
i_values1 = get_values_from(params['i1'], format='csv')
t_values1 = get_values_from(params['t1'], format='csv')
i_values2 = get_values_from(params['i2'], format='csv')
t_values2 = get_values_from(params['t2'], format='csv')
i_values3 = get_values_from(params['i3'], format='csv')
t_values3 = get_values_from(params['t3'], format='csv')
i_values4 = get_values_from(params['i4'], format='csv')
t_values4 = get_values_from(params['t4'], format='csv')

it_values = [(i_values1, t_values1, FILE_1), (i_values2, t_values2, FILE_2), (i_values3, t_values3, FILE_3), 
             (i_values4, t_values4, FILE_4)]
             
#drop into the db
map(dump_data(it_values[3], MYDB, it_values[0], it_values[1], ABOUT), it_values)

# Cyclic Voltammetry
cv_data1 = zip(t_values1, i_values1)
cv_data2 = zip(t_values2, i_values2)
cv_data3 = zip(t_values3, i_values3)
cv_data4 = zip(t_values4, i_values4)

