#!/usr/bin/python3

#Copyright 2019 Andrew T. Dodd

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#unpacker/analyzer for Ambarella 3D LUT binary blobs
#Thanks to perapera on GoPrawn.com for discovering these and their structure
#https://www.goprawn.com/forum/ambarella-cams/18473-color-correction-and-3d-lut-cube

import os
import sys
import struct
import matplotlib.pyplot as plt
import numpy as np

if(len(sys.argv) < 2):
    print("Too few arguments")
    exit(-1)

bin_file = sys.argv[1]

with open(bin_file,'rb') as myfile:

    blocknum = 0
    myfile.seek(0, os.SEEK_END)
    filelen = myfile.tell()

    if(filelen != 17536):
        print("Not 17536 bytes long, not a likely LUT file")
        exit(0)

    myfile.seek(128)
    rgbdata = []
    for j in struct.iter_unpack('<L', myfile.read(16384)):
        w = j[0]
        b = w & 0x3ff
        g = (w >> 10) & 0x3ff
        r = (w >> 20) & 0x3ff
        rgbdata.append([r/1023.0,g/1023.0,b/1023.0])

    rgbdata = np.array(rgbdata)

    rgbdata = np.reshape(rgbdata,(16,256,3))

    gammadata1 = []
    for j in struct.iter_unpack('<H', myfile.read(512)):
        gammadata1.append(j[0])
    gammadata2 = []
    for j in struct.iter_unpack('<H', myfile.read(512)):
        gammadata2.append(j[0]/16.0)

plt.figure(1)
plt.plot(gammadata1, label='Input transform')
plt.plot(gammadata2, label='Output transform')
plt.legend()

plt.figure(2)
plt.imshow(rgbdata, origin='lower')
plt.show()
