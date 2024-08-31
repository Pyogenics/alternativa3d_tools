'''
Copyright (c) 2024 Pyogenics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from struct import unpack
from array import array

def readArrayLength(package):
    print(f"Reading array @ package + {package.tell()}")
    arrayLength = 0

    arrayField = int.from_bytes(package.read(1), "little")
    arrayLengthType = arrayField & 0b10000000
    # Short array length
    if arrayLengthType == 0:
        print("> Short array length")
        # Length of the array is contained in the last 7 bits of this byte
        arrayLength = arrayField
    else: # Must be large array length
        print("> Long array length")
        longArrayLengthType = arrayField & 0b01000000
        # Length in last 6 bits + next byte
        if longArrayLengthType == 0:
            print("Ll")
            lengthByte = int.from_bytes(package.read(1), "little")
            arrayLength = (arrayField & 0b00111111) << 8
            arrayLength += lengthByte
        else: # Length in last 6 bits + next 2 bytes
            print("LL")
            lengthBytes = int.from_bytes(package.read(2), "big")
            arrayLength = (arrayField & 0b00111111) << 16
            arrayLength += lengthBytes

    print(f"array len: {arrayLength}")
    return arrayLength

def readA3DObjectArray(package, objReader, optionalMask):
    length = readArrayLength(package)
    objects = []
    for _ in range(length):
        obj = objReader()
        obj.read(package, optionalMask)
        objects.append(obj)

    return objects

'''
Common types
'''
def readString(package):
    stringLength = readArrayLength(package)
    string = package.read(stringLength)
    string = string.decode("utf-8")
    print(string)

    return string

def readInt16Array(package):
    length = readArrayLength(package)
    integers = unpack(f"{length}h", package.read(length*2))
    integers = array("h", integers)

    return integers

def readIntArray(package):
    length = readArrayLength(package)
    integers = unpack(f"{length}i", package.read(length*4))
    integers = array("i", integers)

    return integers

def readInt64Array(package):
    length = readArrayLength(package)
    integers = unpack(f"{length}q", package.read(length*8))
    integers = array("q", integers)

    return integers

def readFloatArray(package):
    length = readArrayLength(package)
    floats = unpack(f"<{length}f", package.read(length*4))
    floats = array("f", floats)

    return floats