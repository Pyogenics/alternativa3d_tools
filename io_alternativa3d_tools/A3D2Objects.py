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

from . import AlternativaProtocol
from .IOTools import unpackStream

'''
Objects
'''
class A3D2Matrix:
    def __init__(self):
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.d = 0.0
        self.e = 0.0
        self.f = 0.0
        self.g = 0.0
        self.h = 0.0
        self.i = 0.0
        self.j = 0.0
        self.k = 0.0
        self.l = 0.0

    def read(self, package, optionalMask):
        self.a, self.b, self.c = unpackStream("<3f", package)
        self.d, self.e, self.f = unpackStream("<3f", package)
        self.g, self.h, self.i = unpackStream("<3f", package)
        self.j, self.k, self.l = unpackStream("<3f", package)

class A3D2Transform:
    def __init__(self):
        self.matrix = None

    def read(self, package, optionalMask):
        print(f"read transform: {package.tell()}")
        self.matrix = A3D2Matrix()
        self.matrix.read(package, optionalMask)
        print(f"transform: {package.tell()}")

class A3D2KeyFrame:
    def __init__(self):
        self.time = 0.0
        self.transform = None # A3D2Transform

    def read(self, package, optionalMask):
        self.time, = unpackStream("<f", package)
        self.transform = A3D2Transform()
        self.transform.read(package, optionalMask)

class A3D2Surface:
    def __init__(self):
        self.indexBegin = 0
        self.numTriangles = 0

        # Optional
        self.materialId = None

    def read(self, package, optionalMask):
        self.indexBegin, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.materialId, = unpackStream("<I", package)
        self.numTriangles, = unpackStream("<I", package)

'''
Main objects
'''
class A3D2AmbientLight:
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
        print(f"reading ambientLight @ {package.tell()}")
        
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.color, self.id, self.intensity = unpackStream("<IQf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

        print(f"ambientLight\n> boundBoxId: {self.boundBoxId} color: {self.color} id: {self.id} intensity: {self.intensity} visible: {self.visible} name: {self.name} @ {package.tell()}")

class A3D2AnimationClip:
    def __init__(self):
        self.id = 0
        self.loop = False
        self.tracks = [] # Int

        # Optional
        self.name = None
        self.objectIDs = None # Int64
    
    def read(self, package, optionalMask):
        self.id, = unpackStream("<I", package)
        self.loop = bool(package.read(1))
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.objectIDs = AlternativaProtocol.readInt64Array(package)
        self.tracks = AlternativaProtocol.readIntArray(package)

        print(f"animationClip\n> id: {self.id} loop: {self.loop} tracks: {self.tracks} name: {self.name} objectIDs: {self.objectIDs}")

class A3D2AnimationTrack:
    def __init__(self):
        self.id = 0
        self.keyFrames = [] # A3D2Keyframe
        self.objectName = ""

    def read(self, package, optionalMask):
        self.id, = unpackStream("<I", package)
        self.keyFrames = AlternativaProtocol.readObjectArray(package, keyFrame, optionalMask)
        
        print(f"animationTrack\n> id: {self.id} keyFrames: {self.keyFrames} objectName: {self.objectName}")

class A3D2Box:
    def __init__(self):
        self.bounds = [] # float
        self.id = 0

    def read(self, package, optionalMask):
        self.bounds = AlternativaProtocol.readFloatArray(package)
        self.id, = unpackStream("<I", package)

        print(f"box\n> bounds: {self.bounds} id: {self.id}")

class A3D2CubeMap:
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
        if optionalMask.getOptional():
            self.backId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.bottomId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.frontId, = unpackStream("<I", package)
        self.id, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.leftId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.rightId, = unpackStream("<I", package)
        self.topId, = unpackStream("<I", package)

        print(f"cubeMap:\n> backId: {self.backId} bottomId: {self.bottomId} frontId: {self.frontId} id: {self.id} leftId: {self.leftId} rightId: {self.rightId} topId: {self.topId}")

class A3D2Decal:
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
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.id, self.indexBufferId = unpackStream("<QI", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.offset = unpackStream("<f", package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        self.surfaces = AlternativaProtocol.readObjectArray(package, A3D2Surface, optionalMask)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.vertexBuffers = AlternativaProtocol.readIntArray(package)
        self.visible = bool(package.read(1))

class A3D2DirectionalLight:
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
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.color, self.id, self.intensity = unpackStream("<IQf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2Image:
    def __init__(self):
        self.id = 0
        self.url = ""

    def read(self, package, optionalMask):
        self.id, = unpackStream("<I", package)
        self.url = AlternativaProtocol.readString(package)

class A3D2IndexBuffer:
    def __init__(self):
        self.byteBuffer = b""
        self.id = 0
        self.indexCount = 0

    def read(self, package, optionalMask):
        self.byteBuffer = package.read(
            AlternativaProtocol.readArrayLength(package)
        )
        self.id, = unpackStream("<I", package)
        self.indexCount, = unpackStream("<I", package)

class A3D2Joint:
    def __init__(self):
        self.id = 0
        self.visible = False

        # Optional
        self.boundBoxId = None
        self.name = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.id, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))
        print(f"IndexBuffer\n> boundBoxId: {self.boundBoxId} id: {self.id} name: {self.name} parentId: {self.parentId} transform: {self.transform} visible: {self.visible}")

class A3D2Map:
    def __init__(self):
        self.channel = 0
        self.id = 0
        self.imageId = 0

    def read(self, package, optionalMask):
        self.channel, self.id, self.imageId = unpackStream("<H2I", package)
        print(f"map\n> channel: {self.channel} id: {self.id} imageId: {self.imageId}")

class A3D2Material:
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
        if optionalMask.getOptional():
            self.diffuseMapId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.glossinessMapId, = unpackStream("<I", package)
        self.id, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.lightMapId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.normalMapId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.opacityMapId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.reflectionCubeMapId, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.specularMapId, = unpackStream("<I", package)

        print(f"material\n> diffuseMapId: {self.diffuseMapId} glossinessMapId: {self.glossinessMapId} id: {self.id} lightMapId: {self.lightMapId} normalMapId: {self.normalMapId} opacityMapId: {self.opacityMapId} reflectionCubeMapId: {self.reflectionCubeMapId} specularMapId: {self.specularMapId}")

class A3D2Mesh:
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
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.id, self.indexBufferId = unpackStream("<QI", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        self.surfaces = AlternativaProtocol.readObjectArray(package, A3D2Surface, optionalMask)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.vertexBuffers = AlternativaProtocol.readIntArray(package)
        self.visible = bool(package.read(1))

class A3D2Object:
    def __init__(self):
        self.id = 0
        self.visible = False

        # Optional
        self.boundBoxId = None
        self.name = None
        self.parentId = None
        self.transform = None

    def read(self, package, optionalMask):
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.id, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2OmniLight:
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
        self.attenuationBegin, self.attenuationEnd = unpackStream("<2f", package)
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.color, self.id, self.intensity = unpackStream("<IQf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2SpotLight:
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
        self.attenuationBegin, self.attenuationEnd = unpackStream("<2f", package)
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.color, = unpackStream("<I", package)
        if optionalMask.getOptional():
            self.falloff = unpackStream("<f", package)
        if optionalMask.getOptional():
            self.hotspot = unpackStream("<f", package)
        self.id, self.intensity = unpackStream("<Qf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2Sprite:
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
        self.alwaysOnTop = bool(package.read(1))
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.height, self.id, self.materialId = unpackStream("<fQI")
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        self.originX, self.originY = unpackStream("<2f", package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<I", package)
        self.perspectiveScale = bool(package.read(1))
        self.rotation, = unpackStream("<f", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))
        self.width, = unpackStream("<f", package)

class A3D2Skin:
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
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream("<I", package)
        self.id, self.indexBufferId = unpackStream("<QI", package)
        self.jointBindTransforms = AlternativaProtocol.readObjectArray(package, jointBindTransform, optionalMask)
        self.joints = AlternativaProtocol.readInt64Array(package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        self.numJoints = AlternativaProtocol.readInt16Array(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream("<Q", package)
        self.surfaces = AlternativaProtocol.readObjectArray(package, A3D2Surface, optionalMask)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.vertexBuffers = AlternativaProtocol.readIntArray(package)
        self.visible = bool(package.read(1))

class A3D2VertexBuffer:
    def __init__(self):
        self.attributes = [] # int
        self.byteBuffer = b""
        self.id = 0
        self.vertexCount = 0

    def read(self, package, optionalMask):
        self.attributes = AlternativaProtocol.readIntArray(package)
        self.byteBuffer = package.read(AlternativaProtocol.readArrayLength(package))
        self.id, self.vertexCount = unpackStream("<IH", package)