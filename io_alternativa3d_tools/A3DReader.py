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

from sys import argv
from zlib import decompress as zDecompress
from io import BytesIO

from .A3D2 import A3D2Objects

class A3DReader:
    @staticmethod
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
            arrayLength += (arrayField & 63) << (8 * byteCount)
            arrayLength += package.read(byteCount + 1)
        print(f"> Length: {arrayLength}")
        return arrayLength

    @staticmethod
    def readFromFile(file):
        # Read "Package Length" field
        packageLength = 0
        packageGzip = False

        packageLengthField = int.from_bytes(file.read(1), "little")
        packageLengthSize = packageLengthField & 128
        if packageLengthSize == 0:
            # Short package: 14 bits
            print("This is a short package")
            packageLength += (packageLengthField & 63) << 8
            packageLength += int.from_bytes(file.read(1), "little")

            packageGzip = packageLengthField & 64
        else:
            # Long package: 31 bits
            print("This is a long package")
            packageLength += (packageLengthField & 127) << 24
            packageLength += int.from_bytes(file.read(3), "little")

            packageGzip = True
        print(f"Package length: {packageLength}")

        # Decompress gzip data
        package = file.read()
        if packageGzip:
            print("Decompressing package")
            package = zDecompress(package)
            print(f"Decompressed size: {len(package)}")
        package = BytesIO(package)

        # Read "Null-mask" field
        nullMask = b""

        nullMaskField = int.from_bytes(package.read(1), "little")
        nullMaskType = nullMaskField & 128
        if nullMaskType == 0:
            # Short null-mask: 5-29 bits
            print("Short null-mask")
            nullMaskLength = nullMaskField & 96
            
            nullMask += bytes(nullMaskField & 31)
            nullMask += file.read(nullMaskLength) # 1,2 or 3 bytes
        else:
            # Long null-mask: 64 - 4194304 bytes
            print("Long null-mask")
            nullMaskLengthSize = nullMaskField & 64
            if nullMaskLengthSize == 1:
                # Long length: 22 bits
                print("> Long length")
                nullMaskLength = nullMaskField & 63
                nullMaskLength += int.from_bytes(package.read(2), "little")
                
                nullMask += package.read(nullMaskLength)
            else:
                # Short length: 6 bits
                print("> Short length")
                nullMaskLength = nullMaskField & 63
                
                nullMask += package.read(nullMaskLength)
        # Read "version" field
        versionMajor = int.from_bytes(package.read(2), "big")
        versionMinor = int.from_bytes(package.read(2), "big")
        print(f"A3D version: {versionMajor}.{versionMinor}")

        # Read A3D2 objects
        ambientLights = []
        animationClips = []
        animationTracks = []
        boxes = []
        cubeMaps = []
        decals = []
        directionalLights = []
        images = []
        indexBuffers = []
        joints = []
        maps = []
        materials = []
        meshes = []
        objects = []
        omniLights = []
        spotLights = []
        sprites = []
        skins = []
        vertexBuffers = []