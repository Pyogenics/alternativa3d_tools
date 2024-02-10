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
from numpy import array as npArray

from . import A3DArray

def readMatrix(package):
    a, b, c, d, e, f, g, h, i, = unpack("9f", package.read(4*9))
    matrix = npArray([
        [a, b, c],
        [d, e, f],
        [g, h, i]
    ])

    return matrix

'''
Support objects, objects used by other objects
'''
class keyFrame:
    def __init__(self):
        self.time = 0.0
        self.transform = None # A3DMatrix

    def read(self, package):
        self.time = unpack("f", package.read(4))
        self.transform = readMatrix(package)

'''
File objects, these objects are contained in A3DArrays in every file
'''
class ambientLight:
    def __init__(self):
        self.color = 0
        self.id = 0
        self.intensity = 0
        self.visible = False

        # Optional
        self.boundBoxId = None
        self.name = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        hasBoundBoxId, hasName, hasParentId, hasTransform = optionalMask.getOptionals(4)
        
        if hasBoundBoxId:
            self.boundBoxId = int.from_bytes(package.read(4), "little")
        self.color, self.id, self.intensity = unpack("=Iqf", package.read(4+8+4))
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        if hasTransform:
            pass #TODO
        self.visible = bool(package.read(1))

        print(f"ambientLight\n> color: {self.color} id: {self.id} intensity: {self.intensity} visible: {self.visible}")

class animationClip:
    def __init__(self):
        self.id = 0
        self.loop = False
        self.tracks = [] # Int

        # Optional
        self.name = ""
        self.objectIDs = [] # Int64
    
    def read(self, package, optionalMask):
        hasName, hasObjectID = optionalMask.getOptionals(2)

        self.id, self.loop = unpack("=i?")
        if hasName:
            self.name = A3DArray.readString(package)
        if hasObjectID:
            self.objectIDs = A3DArray.readInt64Array(package)
        self.tracks = A3DArray.readIntArray(package)

        print(f"animationClip\n> id: {self.id} loop: {self.loop} tracks: {self.tracks}")

class animationTrack:
    def __init__(self):
        self.id = 0
        self.keyFrames = [] # A3D2Keyframe
        self.objectName = ""

    def read(self, package, optionalMask):
        self.id = int.from_bytes(package.read(4), "little")
        keyFrameCount = A3DArray.readArrayLength(package)
        for _ in range(keyFrameCount):
            obj = keyFrame()
            obj.read(package)
            self.keyFrames.append(obj)
        
        print(f"animationTrack\n> id: {self.id} keyFrames: {self.keyFrames} objectName: {self.objectName}")

class box:
    def __init__(self):
        self.bounds = [] # float
        self.id = 0

    def read(self, package, optionalMask):
        self.bounds = A3DArray.readFloatArray(package)
        self.id = int.from_bytes(package.read(4), "little")

        print(f"box\n> bounds: {self.bounds} id: {self.id}")

class cubeMap:
    def __init__(self):
        self.id = 0
        self.topId = 0

        # Optional
        self.backId = None
        self.bottomId = None
        self.frontId = None
        self.leftId = None
        self.rightId = None

    def read(self, package, optionalMap):
        hasBackId, hasBottomId, hasFrontId, hasLeftId, hasRightId = optionalMap.getOptionals()

        if hasBackId:
            self.backId = int.from_bytes(package.read(4), "little")
        if hasBottomId:
            self.bottomId = int.from_bytes(package.read(4), "little")
        if hasFrontId:
            self.frontId = int.from_bytes(package.read(4), "little")
        self.id = int.from_bytes(package.read(4), "little")
        if hasLeftId:
            self.leftId = int.from_bytes(package.read(4), "little")
        if hasRightId:
            self.rightId = int.from_bytes(package.read(4), "little")
        self.topId = int.from_bytes(package.read(4), "little")

        print(f"cubeMap:\n> backId: {self.backId} bottomId: {self.bottomId} frontId: {self.frontId} id: {self.id} leftId: {self.leftId} rightId: {self.rightId} topId: {self.topId}")

class decal:
    def __init__(self):
        pass

class directionalLight:
    def __init__(self):
        pass

class image:
    def __init__(self):
        pass

class indexBuffer:
    def __init__(self):
        pass

class joint:
    def __init__(self):
        pass

class map:
    def __init__(self):
        pass

class material:
    def __init__(self):
        pass

class mesh:
    def __init__(self):
        pass

class object:
    def __init__(self):
        pass

class omniLight:
    def __init__(self):
        pass

class spotLight:
    def __init__(self):
        pass

class sprite:
    def __init__(self):
        pass

class skin:
    def __init__(self):
        pass

class vertexBuffer:
    def __init__(self):
        pass