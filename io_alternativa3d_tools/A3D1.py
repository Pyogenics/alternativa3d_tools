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

from . import AlternativaProtocol
from .IOTools import unpackStream
from .A3D2 import A3D2Matrix # XXX

'''
Objects
'''
class A3D1Transform:
    def __init__(self):
        # Optional
        self.matrix = None
    
    def read(self, stream, optionalMask):
        print("Read Transform")
        if optionalMask.getOptional():
            self.matrix = A3D2Matrix()
            self.matrix.read(stream, optionalMask)

class A3D1IndexBuffer:
    def __init__(self):
        self.indexCount = 0

        # Optional
        self.byteBuffer = None

    def read(self, stream, optionalMask):
        print("Read IndexBuffer")
        if optionalMask.getOptional():
            self.byteBuffer = stream.read(
                AlternativaProtocol.readArrayLength(stream)
            )
        self.indexCount, = unpackStream(">I", stream)

class A3D1VertexBuffer:
    def __init__(self):
        self.vertexCount = 0

        # Optional
        self.attributes = None # Bytes
        self.byteBuffer = None # Bytes

    def read(self, stream, optionalMask):
        print("Read VertexBuffer")
        if optionalMask.getOptional():
            self.attributes = stream.read(
                AlternativaProtocol.readArrayLength(stream)
            )
        if optionalMask.getOptional():
            self.byteBuffer = stream.read(
                AlternativaProtocol.readArrayLength(stream)
            )
        self.vertexCount, = unpackStream(">H", stream)

class A3D1Surface:
    def __init__(self):
        self.indexBegin = 0
        self.numTriangles = 0

        # Optional
        self.materialId = None # Int

    def read(self, stream, optionalMask):
        print("Read Surface")
        self.indexBegin, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.materialId, = unpackStream(">I", stream)
        self.numTriangles, = unpackStream(">I", stream)

'''
Main objects
'''
class A3D1Box:
    def __init__(self):
        # Optional
        self.bounds = None # float array
        self.id = None

    def read(self, stream, optionalMask):
        print("Read Box")
        if optionalMask.getOptional():
            self.bounds = AlternativaProtocol.readFloatArray(stream)
        if optionalMask.getOptional():
            self.id, = unpackStream(">I", stream)

class A3D1Geometry:
    def __init__(self):
        # Optional
        self.id = None
        self.indexBuffer = None
        self.vertexBuffers = None

    def read(self, stream, optionalMask):
        print("Read Geometry")
        if optionalMask.getOptional():
            self.id, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.indexBuffer = A3D1IndexBuffer()
            self.indexBuffer.read(stream, optionalMask)
        if optionalMask.getOptional():
            self.vertexBuffers = AlternativaProtocol.readObjectArray(stream, A3D1VertexBuffer, optionalMask)

class A3D1Image:
    def __init__(self):
        # Optional
        self.id = None
        self.url = None

    def read(self, stream, optionalMask):
        print("Read Image")
        if optionalMask.getOptional():
            self.id, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.url = AlternativaProtocol.readString(stream)

class A3D1Map:
    def __init__(self):
        self.channel = 0

        # Optional
        self.id = None
        self.imageId = None
        self.uOffset = None
        self.uScale = None
        self.vOffset = None
        self.vScale = None

    def read(self, stream, optionalMask):
        print("Read Map")
        self.channel, = unpackStream(">H", stream)
        if optionalMask.getOptional():
            self.id, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.imageId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.uOffset, = unpackStream(">f", stream)
        if optionalMask.getOptional():
            self.uScale, = unpackStream(">f", stream)
        if optionalMask.getOptional():
            self.vOffset, = unpackStream(">f", stream)
        if optionalMask.getOptional():
            self.vScale, = unpackStream(">f", stream)

class A3D1Material:
    def __init__(self):
        # Optional
        self.diffuseMapId = None
        self.glossinessMapId = None
        self.id = None
        self.lightMapId = None
        self.normalMapId = None
        self.opacityMapId = None
        self.specularMapId = None

    def read(self, stream, optionalMask):
        print("Read Material")
        if optionalMask.getOptional():
            self.diffuseMapId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.glossinessMapId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.id, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.lightMapId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.normalMapId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.opacityMapId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.specularMapId, = unpackStream(">I", stream)

class A3D1Object:
    def __init__(self):
        # Optional
        self.boundBoxId = None
        self.geometryId = None
        self.id = None
        self.name = None
        self.parentId = None
        self.surfaces = None
        self.transform = None
        self.visible = None

    def read(self, stream, optionalMask):
        print("Read Object")
        if optionalMask.getOptional():
            self.boundBoxId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.geometryId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.id, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.name = AlternativaProtocol.readString(stream)
        if optionalMask.getOptional():
            self.parentId, = unpackStream(">I", stream)
        if optionalMask.getOptional():
            self.surfaces = AlternativaProtocol.readObjectArray(stream, A3D1Surface, optionalMask)
        if optionalMask.getOptional():
            self.transform = A3D1Transform()
            self.transform.read(stream, optionalMask)
        if optionalMask.getOptional():
            self.visible = bool(stream.read(1))

'''
Main
'''
class A3D1:
    def __init__(self):
        self.boxes = []
        self.geometry = []
        self.images = []
        self.maps = []
        self.materials = []
        self.objects = []

    def readObjects(self, stream, optionalMask):
        print("Reading object data")

        if optionalMask.getOptional():
            self.boxes = AlternativaProtocol.readObjectArray(stream, A3D1Box, optionalMask)
        if optionalMask.getOptional():
            self.geometry = AlternativaProtocol.readObjectArray(stream, A3D1Geometry, optionalMask)
        if optionalMask.getOptional():
            self.images = AlternativaProtocol.readObjectArray(stream, A3D1Image, optionalMask)
        if optionalMask.getOptional():
            self.maps = AlternativaProtocol.readObjectArray(stream, A3D1Map, optionalMask)
        if optionalMask.getOptional():
            self.materials = AlternativaProtocol.readObjectArray(stream, A3D1Material, optionalMask)
        if optionalMask.getOptional():
            self.objects = AlternativaProtocol.readObjectArray(stream, A3D1Object, optionalMask)

    '''
    Drivers
    '''
    def read(self, stream):
        print("Reading A3D1")

        optionalMask = AlternativaProtocol.OptionalMask()
        optionalMask.read(stream)
        self.readObjects(stream, optionalMask)
    
    def write(self, stream):
        print("Writing A3D1")