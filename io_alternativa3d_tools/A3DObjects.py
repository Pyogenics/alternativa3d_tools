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

    def read(self, package, optionalMask):
        self.time = unpack("f", package.read(4))
        self.transform = readMatrix(package)

class surface:
    def __init__(self):
        self.indexBegin = 0
        self.numTriangles = 0

        # Optional
        self.materialId = None

    def read(self, package, optionalMask):
        hasMaterialId = optionalMask.getOptionals()

        self.indexBegin = int.from_bytes(package.read(4), "little")
        if hasMaterialId:
            self.materialId = int.from_bytes(package.read(4), "little")
        self.numTriangles = int.from_bytes(package.read(4), "little")

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
        self.keyFrames = A3DArray.readA3DObjectArray(package, keyFrame, optionalMask)
        
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

    def read(self, package, optionalMask):
        hasBackId, hasBottomId, hasFrontId, hasLeftId, hasRightId = optionalMask.getOptionals(5)

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
        self.id = 0
        self.indexBufferId = 0
        self.surfaces = [] # A3D2Surface
        self.indexBuffers = [] # int
        self.visible = False

        # Optional
        self.boundBoxId = None
        self.name = None
        self.offset = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        hasBoundBoxId, hasName, hasOffset, hasParentId, hasTransform = optionalMask.getOptionals(5)

        if hasBoundBoxId:
            self.boundBoxId = int.from_bytes(package.read(4), "little")
        self.id = int.from_bytes(package.read(8), "little")
        self.indexBufferId = int.from_bytes(package.read(4), "little")
        if hasName:
            self.name = A3DArray.readString(package)
        if hasOffset:
            self.offset = unpack("f", package.read(4))
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        self.surfaces = A3DArray.readA3DObjectArray(package, surface, optionalMask)
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.vertexBuffers = A3DArray.readIntArray(package)
        self.visible = bool(package.read(1))

class directionalLight:
    def __init__(self):
        self.color = 0
        self.id = 0
        self.intensity = 0.0
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
        self.color = int.from_bytes(package.read(4), "little")
        self.id = int.from_bytes(package.read(8), "little")
        self.intensity = unpack("f", package.read(4))
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class image:
    def __init__(self):
        self.id = 0
        self.url = ""

    def read(self, package, optionalMask):
        self.id = int.from_bytes(package.read(4), "little")
        self.url = A3DArray.readString(package)

class indexBuffer:
    def __init__(self):
        self.byteBuffer = b""
        self.id = 0
        self.indexCount = 0

    def read(self, package, optionalMask):
        self.byteBuffer = package.read(
            A3DArray.readArrayLength(package)
        )
        self.id = int.from_bytes(package.read(4), "little")
        self.indexCount = int.from_bytes(package.read(4), "little")

class joint:
    def __init__(self):
        self.id = 0
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
        self.id = int.from_bytes(package.read(8), "little")
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class map:
    def __init__(self):
        self.channel = 0
        self.id = 0
        self.imageId = 0

    def read(self, package, optionalMask):
        self.channel = int.from_bytes(package.read(2), "little")
        self.id = int.from_bytes(package.read(4), "little")
        self.imageId = int.from_bytes(package.read(4), "little")

class material:
    def __init__(self):
        self.id = 0

        # Optional
        self.diffuseMapId = None
        self.glossinessMapId = None
        self.lightMapId = None
        self.normalMapId = None
        self.opacityMapId = None
        self.reflectionCubeMapId = None
        self.specularMapId = None

    def read(self, package, optionalMask):
        hasDiffuseMapId, hasGlossinessMapId, hasLightMapId, hasNormalMapId,
        hasOpacityMapId, hasReflectionCubeMapId, hasSpecularMapId = optionalMask.getOptionals(7)

        if hasDiffuseMapId:
            self.diffuseMapId = int.from_bytes(package.read(4), "little")
        if hasGlossinessMapId:
            self.glossinessMapId = int.from_bytes(package.read(4), "little")
        self.id = int.from_bytes(package.read(4), "little")
        if hasLightMapId:
            self.lightMapId = int.from_bytes(package.read(4), "little")
        if hasNormalMapId:
            self.normalMapId = int.from_bytes(package.read(4), "little")
        if hasOpacityMapId:
            self.opacityMapId = int.from_bytes(package.read(4), "little")
        if hasReflectionCubeMapId:
            self.reflectionCubeMapId = int.from_bytes(package.read(4), "little")
        if hasSpecularMapId:
            self.specularMapId = int.from_bytes(package.read(4), "little")

class mesh:
    def __init__(self):
        self.id = 0
        self.indexBufferId = 0
        self.surfaces = [] # surface
        self.vertexBuffers = [] # int
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
        self.id = int.from_bytes(package.read(8), "little")
        self.indexBufferId = int.from_bytes(package.read(4), "little")
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        self.surfaces = A3DArray.readA3DObjectArray(package, surface, optionalMask)
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.vertexBuffers = A3DArray.readIntArray(package)
        self.visible = bool(package.read(1))

class object:
    def __init__(self):
        self.id = 0
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
        self.id = int.from_bytes(package.read(8), "little")
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class omniLight:
    def __init__(self):
        self.attenuationBegin = 0.0
        self.attenuationEnd = 0.0
        self.color = 0
        self.id = 0
        self.intensity = 0.0
        self.visible = False

        # Optional
        self.boundBoxId = None
        self.name = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        hasBoundBoxId, hasName, hasParentId, hasTransform = optionalMask.getOptionals(4)

        self.attenuationBegin = unpack("f", package.read(4))
        self.attenuationEnd = unpack("f", package.read(4))
        if hasBoundBoxId:
            self.boundBoxId = int.from_bytes(package.read(4), "little")
        self.color = int.from_bytes(package.read(4), "little")
        self.id = int.from_bytes(package.read(8), "little")
        self.intensity = unpack("f", package.read(4))
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class spotLight:
    def __init__(self):
        self.attenuationBegin = 0.0
        self.attenuationEnd = 0.0
        self.color = 0
        self.id = 0
        self.intensity = 0.0
        self.visible = False

        # Optional
        self.boundBoxId = None
        self.falloff = None
        self.hotspot = None
        self.name = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        hasBoundBoxId, hasFalloff, hasHotspot, hasName, hasParentId, hasTransform = optionalMask.getOptionals(6)

        self.attenuationBegin = unpack("f", package.read(4))
        self.attenuationEnd = unpack("f", package.read(4))
        if hasBoundBoxId:
            self.boundBoxId = int.from_bytes(package.read(4), "little")
        self.color = int.from_bytes(package.read(4), "little")
        if hasFalloff:
            self.falloff = unpack("f", package.read(4))
        if hasHotspot:
            self.hotspot = unpack("f", package.read(4))
        self.id = int.from_bytes(package.read(8), "little")
        self.intensity = unpack("f", package.read(4))
        if hasName:
            self.name = A3DArray.readString(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class sprite:
    def __init__(self):
        self.alwaysOnTop = False
        self.height = 0.0
        self.id = 0
        self.materialId = 0
        self.originX = 0.0
        self.originY = 0.0
        self.perspectiveScale = True
        self.rotation = 0.0
        self.visible = False
        self.width = 0.0

        # Optional
        self.boundBoxId = None
        self.name = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        hasBoundBoxId, hasName, hasParentId, hasTransform = optionalMask.getOptionals(4)

        self.alwaysOnTop = bool(package.read(1))
        if hasBoundBoxId:
            self.boundBoxId = int.from_bytes(package.read(4), "little")
        self.height = unpack("f", package.read(4))
        self.id = int.from_bytes(package.read(8), "little")
        self.materialId = int.from_bytes(package.read(4), "little")
        if hasName:
            self.name = A3DArray.readString(package)
        self.originX = unpack("f", package.read(4))
        self.originY = unpack("f", package.read(4))
        if hasParentId:
            self.parentId = int.from_bytes(package.read(4), "little")
        self.perspectiveScale = bool(package.read(1))
        self.rotation = unpack("f", package.read(4))
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))
        self.width = unpack("f", package.read(4))

class skin:
    def __init__(self):
        self.id = 0
        self.indexBufferId = 0
        self.jointBindTransforms = [] # A3D2JointBindTransform
        self.joints = [] # int64
        self.numJoints = [] # ushort
        self.surfaces = [] # A3D2Surface
        self.vertexBuffers = [] # int
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
        self.id = int.from_bytes(package.read(8), "little")
        self.indexBufferId = int.from_bytes(package.read(4), "little")
        self.jointBindTransforms = A3DArray.readA3DObjectArray(package, jointBindTransform, optionalMask)
        self.joints = A3DArray.readInt64Array(package)
        if hasName:
            self.name = A3DArray.readString(package)
        self.numJoints = A3DArray.readInt16Array(package)
        if hasParentId:
            self.parentId = int.from_bytes(package.read(8), "little")
        self.surfaces = A3DArray.readA3DObjectArray(package, surface, optionalMask)
        if hasTransform:
            self.transform = transform()
            self.transform.read(package, optionalMask)
        self.vertexBuffers = A3DArray.readIntArray(package)
        self.visible = bool(package.read(1))

class vertexBuffer:
    def __init__(self):
        self.attributes = [] # int
        self.byteBuffer = b""
        self.id = 0
        self.vertexCount = 0

    def read(self, package, optionalMask):
        self.attributes = A3DArray.readIntArray(package)
        self.byteBuffer = package.read(A3DArray.readArrayLength(package))
        self.id = int.from_bytes(package.read(4), "little")
        self.vertexCount = int.from_bytes(package.read(2), "little")