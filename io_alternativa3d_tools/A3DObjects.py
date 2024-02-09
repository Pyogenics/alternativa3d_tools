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

from . import A3DArray

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

class track:
    def __init__(self):
        pass

class box:
    def __init__(self):
        pass

class cubeMap:
    def __init__(self):
        pass

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