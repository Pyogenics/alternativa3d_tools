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
    arrayField = int.from_bytes(package.read(1), "little")
    arrayLengthType = arrayField & 128
    arrayLength = 0
    if arrayLengthType == 0:
        # Short array: 7 bit size
        print("> Short array")
        arrayLength += arrayField & 127
    else:
        # Long array: 6 bits + 1-2 bytes
        print("> Long array")
        byteCount = ((arrayField & 64) >> 7)
        print(f">> Byte count: {byteCount + 1}")
        arrayLength += (arrayField & 63) << (8 * byteCount)
        arrayLength += int.from_bytes(package.read(byteCount + 1), "little")
    print(f"> Length: {arrayLength}")
    return arrayLength

'''
Common types
'''
def readString(package):
    stringLength = readArrayLength(package)
    string = package.read(stringLength).decode("utf-8")

    return string

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