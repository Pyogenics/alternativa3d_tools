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

from io import BytesIO
from struct import unpack
from zlib import decompress

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
        print("Read Matrix")
        self.a, self.b, self.c = unpackStream(">3f", package)
        self.d, self.e, self.f = unpackStream(">3f", package)
        self.g, self.h, self.i = unpackStream(">3f", package)
        self.j, self.k, self.l = unpackStream(">3f", package)

class A3D2Transform:
    def __init__(self):
        self.matrix = None

    def read(self, package, optionalMask):
        print("Read Transform")
        self.matrix = A3D2Matrix()
        self.matrix.read(package, optionalMask)

class A3D2KeyFrame:
    def __init__(self):
        self.time = 0.0
        self.transform = None # A3D2Transform

    def read(self, package, optionalMask):
        print("Read KeyFrame")
        self.time, = unpackStream(">f", package)
        self.transform = A3D2Transform()
        self.transform.read(package, optionalMask)

class A3D2Surface:
    def __init__(self):
        self.indexBegin = 0
        self.numTriangles = 0

        # Optional
        self.materialId = None

    def read(self, package, optionalMask):
        print("Read Surface")
        self.indexBegin, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.materialId, = unpackStream(">I", package)
        self.numTriangles, = unpackStream(">I", package)

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
        print("Read AmbientLight")
        
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.color, self.id, self.intensity = unpackStream(">IQf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2AnimationClip:
    def __init__(self):
        self.id = 0
        self.loop = False
        self.tracks = [] # Int

        # Optional
        self.name = None
        self.objectIDs = None # Int64
    
    def read(self, package, optionalMask):
        print("Read AnimationClip")
        self.id, = unpackStream(">I", package)
        self.loop = bool(package.read(1))
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.objectIDs = AlternativaProtocol.readInt64Array(package)
        self.tracks = AlternativaProtocol.readIntArray(package)

class A3D2AnimationTrack:
    def __init__(self):
        self.id = 0
        self.keyFrames = [] # A3D2Keyframe
        self.objectName = ""

    def read(self, package, optionalMask):
        print("Read AnimationTrack")
        self.id, = unpackStream(">I", package)
        self.keyFrames = AlternativaProtocol.readObjectArray(package, keyFrame, optionalMask)

class A3D2Box:
    def __init__(self):
        self.bounds = [] # float
        self.id = 0

    def read(self, package, optionalMask):
        print("Read Box")
        self.bounds = AlternativaProtocol.readFloatArray(package)
        self.id, = unpackStream(">I", package)

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
        print("Read CubeMap")
        if optionalMask.getOptional():
            self.backId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.bottomId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.frontId, = unpackStream(">I", package)
        self.id, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.leftId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.rightId, = unpackStream(">I", package)
        self.topId, = unpackStream(">I", package)

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
        print("Read Decal")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.id, self.indexBufferId = unpackStream(">QI", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.offset = unpackStream(">f", package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
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
        print("Read DirectionalLight")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.color, self.id, self.intensity = unpackStream(">IQf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2Image:
    def __init__(self):
        self.id = 0
        self.url = ""

    def read(self, package, optionalMask):
        print("Read Image")
        self.id, = unpackStream(">I", package)
        self.url = AlternativaProtocol.readString(package)

class A3D2IndexBuffer:
    def __init__(self):
        self.byteBuffer = b""
        self.id = 0
        self.indexCount = 0

    def read(self, package, optionalMask):
        print("Read IndexBuffer")
        self.byteBuffer = package.read(
            AlternativaProtocol.readArrayLength(package)
        )
        self.id, = unpackStream(">I", package)
        self.indexCount, = unpackStream(">I", package)

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
        print("Read Joint")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.id, = unpackStream(">Q", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))

class A3D2Map:
    def __init__(self):
        self.channel = 0
        self.id = 0
        self.imageId = 0

    def read(self, package, optionalMask):
        print("Read Map")
        self.channel, self.id, self.imageId = unpackStream(">H2I", package)

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
        print("Read Material")
        if optionalMask.getOptional():
            self.diffuseMapId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.glossinessMapId, = unpackStream(">I", package)
        self.id, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.lightMapId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.normalMapId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.opacityMapId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.reflectionCubeMapId, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.specularMapId, = unpackStream(">I", package)

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
        print("Read Mesh")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.id, self.indexBufferId = unpackStream(">QI", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
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
        print("Read Object")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.id, = unpackStream(">Q", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
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
        print("Read OmniLight")
        self.attenuationBegin, self.attenuationEnd = unpackStream(">2f", package)
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.color, self.id, self.intensity = unpackStream(">IQf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
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
        print("Read SpotLight")
        self.attenuationBegin, self.attenuationEnd = unpackStream(">2f", package)
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.color, = unpackStream(">I", package)
        if optionalMask.getOptional():
            self.falloff = unpackStream(">f", package)
        if optionalMask.getOptional():
            self.hotspot = unpackStream(">f", package)
        self.id, self.intensity = unpackStream(">Qf", package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
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
        print("Read Sprite")
        self.alwaysOnTop = bool(package.read(1))
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.height, self.id, self.materialId = unpackStream(">fQI")
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        self.originX, self.originY = unpackStream(">2f", package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">I", package)
        self.perspectiveScale = bool(package.read(1))
        self.rotation, = unpackStream(">f", package)
        if optionalMask.getOptional():
            self.transform = A3D2Transform()
            self.transform.read(package, optionalMask)
        self.visible = bool(package.read(1))
        self.width, = unpackStream(">f", package)

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
        print("Read Skin")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", package)
        self.id, self.indexBufferId = unpackStream(">QI", package)
        self.jointBindTransforms = AlternativaProtocol.readObjectArray(package, jointBindTransform, optionalMask)
        self.joints = AlternativaProtocol.readInt64Array(package)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(package)
        self.numJoints = AlternativaProtocol.readInt16Array(package)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">Q", package)
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
        print("Read VertexBuffer")
        self.attributes = AlternativaProtocol.readIntArray(package)
        self.byteBuffer = package.read(AlternativaProtocol.readArrayLength(package))
        self.id, self.vertexCount = unpackStream(">IH", package)

'''
Main
'''
class A3D2:
    def __init__(self):
        self.ambientLights = []
        self.animationClips = []
        self.animationTracks = []
        self.boxes = []
        self.cubeMaps = []
        self.decals = []
        self.directionalLights = []
        self.images = []
        self.indexBuffers = []
        self.joints = []
        self.maps = []
        self.materials = []
        self.meshes = []
        self.objects = []
        self.omniLights = []
        self.spotLights = []
        self.sprites = []
        self.skins = []
        self.vertexBuffers = []

    def readPackage(self, stream):
        print("Reading package")

        # Read "Package Length" field
        packageLength = 0
        packageGzip = False

        packageLengthField = int.from_bytes(stream.read(1), "little")
        packageLengthSize = packageLengthField & 0b10000000
        if packageLengthSize == 0:
            # Short package: 14 bits
            packageLength += (packageLengthField & 0b00111111) << 8
            packageLength += int.from_bytes(stream.read(1), "little")

            packageGzip = packageLengthField & 0b01000000
        else:
            # Long package: 31 bits
            packageLength += (packageLengthField & 0b01111111) << 24
            packageLength += int.from_bytes(stream.read(3), "little")

            packageGzip = True

        # Decompress gzip data
        package = stream.read()
        if packageGzip:
            print("Decompressing package")
            package = decompress(package)
        package = BytesIO(package)
        
        return package

    def readObjects(self, stream, optionalMask):
        print("Reading object data")

        if optionalMask.getOptional():
            self.ambientLights = AlternativaProtocol.readObjectArray(stream, A3D2AmbientLight, optionalMask)
        if optionalMask.getOptional():
            self.animationClips = AlternativaProtocol.readObjectArray(stream, A3D2AnimationClip, optionalMask)
        if optionalMask.getOptional():
            self.animationTracks = AlternativaProtocol.readObjectArray(stream, A3D2AnimationTrack, optionalMask)
        if optionalMask.getOptional():
            self.boxes = AlternativaProtocol.readObjectArray(stream, A3D2Box, optionalMask)
        if optionalMask.getOptional():
            self.cubeMaps = AlternativaProtocol.readObjectArray(stream, A3D2CubeMap, optionalMask)
        if optionalMask.getOptional():
            self.decals = AlternativaProtocol.readObjectArray(stream, A3D2Decal, optionalMask)
        if optionalMask.getOptional():
            self.directionalLights = AlternativaProtocol.readObjectArray(stream, A3D2DirectionalLight, optionalMask)
        if optionalMask.getOptional():
            self.images = AlternativaProtocol.readObjectArray(stream, A3D2Image, optionalMask)
        if optionalMask.getOptional():
            self.indexBuffers = AlternativaProtocol.readObjectArray(stream, A3D2IndexBuffer, optionalMask)
        if optionalMask.getOptional():
            self.joints = AlternativaProtocol.readObjectArray(stream, A3D2Joint, optionalMask)
        if optionalMask.getOptional():
            self.maps = AlternativaProtocol.readObjectArray(stream, A3D2Map, optionalMask)
        if optionalMask.getOptional():
            self.materials = AlternativaProtocol.readObjectArray(stream, A3D2Material, optionalMask)
        if optionalMask.getOptional():
            self.meshes = AlternativaProtocol.readObjectArray(stream, A3D2Mesh, optionalMask)
        if optionalMask.getOptional():
            self.objects = AlternativaProtocol.readObjectArray(stream, A3D2Object, optionalMask)
        if optionalMask.getOptional():
            self.omniLights = AlternativaProtocol.readObjectArray(stream, A3D2OmniLight, optionalMask)
        if optionalMask.getOptional():
            self.spotLights = AlternativaProtocol.readObjectArray(stream, A3D2SpotLight, optionalMask)
        if optionalMask.getOptional():
            self.sprites = AlternativaProtocol.readObjectArray(stream, A3D2Sprite, optionalMask)
        if optionalMask.getOptional():
            self.skins = AlternativaProtocol.readObjectArray(stream, A3D2Skin, optionalMask)
        if optionalMask.getOptional():
            self.vertexBuffers = AlternativaProtocol.readObjectArray(stream, A3D2VertexBuffer, optionalMask)

    '''
    Drivers
    '''
    def read(self, stream):
        print("Reading A3D2")

        # Read package and header data
        package = self.readPackage(stream)
        optionalMask = AlternativaProtocol.OptionalMask()
        optionalMask.read(package)
        versionMajor, versionMinor = unpackStream(">2H", package)
        print(f"This package is version {versionMajor}.{versionMinor}")

        # Read object data
        self.readObjects(package, optionalMask)

    def write(self, stream):
        print("Writing A3D2")