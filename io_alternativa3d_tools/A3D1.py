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

'''
Objects
'''
class box:
	def __init__(self):
		# Optional
		self.bounds = None # float array
		self.id = None

	def read(self, package, optionalMask):
		if optionalMask.getOptional():
			self.bounds = A3DArray.readFloatArray(package)
		if optionalMask.getOptional():
			self.id = int.from_bytes(package.read(4), "little")

class geometry:
	def __init__(self):
		# Optional
		self.id = None
		self.indexBuffer = None
		self.vertexBuffers = None

	def read(self, package, optionalMask):
		hasId, hasIndexBuffer, hasVertexBuffers = optionalMask.getOptionals(3)

		if hasId:
			self.id = int.from_bytes(package.read(4), "little")
		if hasIndexBuffer:
			self.indexBuffer = indexBuffer()
			self.indexBuffer.read(package, optionalMask)
		if hasVertexBuffers:
			self.vertexBuffers = A3DArray.readA3DObjectArray(package, vertexBuffer, optionalMask)

class image:
	def __init__(self):
		# Optional
		self.id = None
		self.url = None

	def read(self, package, optionalMask):
		hasId, hasUrl = optionalMask.getOptionals(2)

		if hasId:
			self.id = int.from_bytes(package.read(4), "little")
		if hasUrl:
			self.url = A3DArray.readString(package)

class map:
	def __init__(self):
		self.channel = 0

		# Optional
		self.id = None
		self.imageId = None
		self.uOffset = None
		self.uScale = None
		self.vOffset = None
		self.vScale = None

	def read(self, package, optionalMask):
		hasId, hasImageId, hasUOffset,
		hasUScale, hasVOffset, hasVScale = optionalMask.getOptionals(6)

		self.channel = int.from_bytes(package.read(2), "little")
		if hasId:
			self.id = int.from_bytes(package.read(4), "little")
		if hasImageId:
			self.imageId = int.from_bytes(package.read(4), "little")
		if hasUOffset:
			self.uOffset = unpack("f", package.read(4))
		if hasUScale:
			self.uScale = unpack("f", package.read(4))
		if hasVOffset:
			self.vOffset = unpack("f", package.read(4))
		if hasVScale:
			self.vScale = unpack("f", package.read(4))

class material:
	def __init__(self):
		# Optional
		self.diffuseMapId = None
		self.glossinessMapId = None
		self.id = None
		self.lightMapId = None
		self.normalMapId = None
		self.opacityMapId = None
		self.specularMapId = None

	def read(self, package, optionalMask):
		hasDiffuseMapId, hasGlossinessMapId, hasId, hasLightMapId,
		hasNormalMapId, hasOpacityMapId, hasSpecularMapId = optionalMask.getOptionals(7)

		if hasDiffuseMapId:
			self.diffuseMapId = int.from_bytes(package.read(4), "little")
		if hasGlossinessMapId:
			self.glossinessMapId = int.from_bytes(package.read(4), "little")
		if hasId:
			self.id = int.from_bytes(package.read(4), "little")
		if hasLightMapId:
			self.lightMapId = int.from_bytes(package.read(4), "little")
		if hasNormalMapId:
			self.normalMapId = int.from_bytes(package.read(4), "little")
		if hasOpacityMapId:
			self.opacityMapId = int.from_bytes(package.read(4), "little")
		if hasSpecularMapId:
			self.specularMapId = int.from_bytes(package.read(4), "little")

class object:
	def __init__(self):
		# Optional
		self.boundBoxId = None
		self.geometryId = None
		self.id = None
		self.name = None
		self.parentId = None
		self.surfaces = None
		self.transformation = None
		self.visible = None

	def read(self, package, optionalMask):
		hasBoundBoxId, hasGeometryId, hasId, hasName, hasParentId,
		hasSurfaces, hasTransformation,hasVisible = optionalMask.getOptionals(8)

		if hasBoundBoxId:
			self.boundBoxId = int.from_bytes(package.read(4), "little")
		if hasGeometryId:
			self.geometryId = int.from_bytes(package.read(4), "little")
		if hasId:
			self.id = int.from_bytes(package.read(4), "little")
		if hasName:
			self.name = A3DArray.readString(package)
		if hasParentId:
			self.parentId = int.from_bytes(package.read(4), "little")
		if hasSurfaces:
			self.surfaces = A3DArray.readA3DObjectArray(package, surface)
		if hasTransformation:
			self.transformation = transformation()
			self.transformation.read(package, optionalMask)
		if hasVisible:
			self.visible = bool(package.read(1))

class indexBuffer:
	def __init__(self):
		self.indexCount = 0

		# Optional
		self.byteBuffer = None

	def read(self, package, optionalMask):
		if optionalMask.getOptional():
			self.byteBuffer = package.read(
        		A3DArray.readArrayLength(package)
			)
		self.indexCount = int.from_bytes(package.read(4), "little")

class vertexBuffer:
	def __init__(self):
		self.vertexCount = 0

		# Optional
		self.attributes = None # [Byte]
		self.byteBuffer = None # Bytes

	def read(self, package, optionalMask):
		if optionalMask.getOptional():
			self.attributes = package.read(
        		A3DArray.readArrayLength(package)
			)
		if optionalMask.getOptional:
			self.byteBuffer = package.read(
        		A3DArray.readArrayLength(package)
			)
		self.vertexCount = int.from_bytes(package.read(4), "little")

'''
Main
'''
class A3D1:
	def __init__(self):
		self.boxes = []
		self.geometries = []
		self.images = []
		self.maps = []
		self.materials = []
		self.objects = []
	
	'''
	Drivers
	'''
	def read(self, stream):
		print("Reading A3D1")
	
	def write(self, stream):
		print("Writing A3D1")