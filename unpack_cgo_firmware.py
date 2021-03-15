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

#Unpacker for Yuneec CGO3 firmware files
#Thanks to hc1982 on the GoPrawn forums for some insight into aspects of the file format I completely missed
# https://www.goprawn.com/forum/ambarella-cams/18473-color-correction-and-3d-lut-cube?p=19540#post19540

import os
import sys
import struct

def copypart(src,dest,start,length,bufsize=1024*1024):
    with open(src,'rb') as f1:
        f1.seek(start)
        with open(dest,'wb') as f2:
            while length:
                chunk = min(bufsize,length)
                data = f1.read(chunk)
                f2.write(data)
                length -= chunk

if(len(sys.argv) < 2):
    print("Too few arguments")
    exit(-1)

bin_file = sys.argv[1]

with open(bin_file,'rb') as myfile:

    blocknum = 0
    myfile.seek(0, os.SEEK_END)
    filelen = myfile.tell()

    myfile.seek(0xc)
    (armlen, ubilen, hdrlen) = struct.unpack('<LLL', myfile.read(12))
    print(armlen)
    print(ubilen)
    print(hdrlen)

    copypart(bin_file, 'header.bin', 0, hdrlen)
    copypart(bin_file, 'arm.bin', hdrlen, armlen)
    copypart(bin_file, 'ubifs.bin', hdrlen+armlen, ubilen)
