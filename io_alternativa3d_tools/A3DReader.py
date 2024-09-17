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

from zlib import decompress as zDecompress
from io import BytesIO

from . import A3D2Objects
from . import AlternativaProtocol
from .IOTools import unpackStream

def readPackage(file):
    # Read "Package Length" field
    packageLength = 0
    packageGzip = False

    packageLengthField = int.from_bytes(file.read(1), "little")
    packageLengthSize = packageLengthField & 0b10000000
    if packageLengthSize == 0:
        # Short package: 14 bits
        print("This is a short package")
        packageLength += (packageLengthField & 0b00111111) << 8
        packageLength += int.from_bytes(file.read(1), "little")

        packageGzip = packageLengthField & 0b01000000
    else:
        # Long package: 31 bits
        print("This is a long package")
        packageLength += (packageLengthField & 0b01111111) << 24
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
    
    return package

def readVersion(package):
    # Read "version" field
    versionMajor, versionMinor = unpackStream(">2H", package)
    print(f"A3D version: {versionMajor}.{versionMinor}")

    return (versionMajor, versionMinor)

def readObjects(package, nullMask):
    ambientLights = []
    hasAmbientLights = nullMask.getOptional()
    print(f"## AmbientLights {hasAmbientLights}")
    if hasAmbientLights:
        ambientLights = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2AmbientLight, nullMask)

    animationClips = []
    hasAnimationClips = nullMask.getOptional()
    print(f"## AnimationClips {hasAnimationClips}")
    if hasAnimationClips:
        animationClips = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2AnimationClip, nullMask)

    animationTracks = []
    hasAnimationTracks = nullMask.getOptional()
    print(f"## AnimationTracks {hasAnimationTracks}")
    if hasAnimationTracks:
        animationTracks = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2AnimationTrack, nullMask)

    boxes = []
    hasBoxes = nullMask.getOptional()
    print(f"## Boxes {hasBoxes}")
    if hasBoxes:
        boxes = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Box, nullMask)

    cubeMaps = []
    hasCubeMaps = nullMask.getOptional()
    print(f"## CubeMaps {hasCubeMaps}")
    if hasCubeMaps:
        cubeMaps = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2CubeMap, nullMask)

    decals = []
    hasDecals = nullMask.getOptional()
    print(f"## Decals {hasDecals}")
    if hasDecals:
        decals = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Decal, nullMask)

    directionalLights = []
    hasDirectionalLights = nullMask.getOptional()
    print(f"## DirectionalLights {hasDirectionalLights}")
    if hasDirectionalLights:
        directionalLights = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2DirectionalLight, nullMask)

    images = []
    hasImages = nullMask.getOptional()
    print(f"## Images {hasImages}")
    if hasImages:
        images = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Image, nullMask)

    indexBuffers = []
    hasIndexBuffers = nullMask.getOptional()
    print(f"## IndexBuffers {hasIndexBuffers}")
    if hasIndexBuffers:
        indexBuffers = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2IndexBuffer, nullMask)

    joints = []
    hasJoints = nullMask.getOptional()
    print(f"## Joints {hasJoints}")
    if hasJoints:
        joints = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Joint, nullMask)

    maps = []
    hasMaps = nullMask.getOptional()
    print(f"## Maps {hasMaps}")
    if hasMaps:
        maps = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Map, nullMask)

    materials = []
    hasMaterials = nullMask.getOptional()
    print(f"## Materials {hasMaterials}")
    if hasMaterials:
        materials = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Material, nullMask)

    meshes = []
    hasMeshes = nullMask.getOptional()
    print(f"## Meshes {hasMeshes}")
    if hasMeshes:
        meshes = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Mesh, nullMask)

    objects = []
    hasObjects = nullMask.getOptional()
    print(f"## Objects {hasObjects}")
    if hasObjects:
        objects = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Object, nullMask)

    omniLights = []
    hasOmniLights = nullMask.getOptional()
    print(f"## OmniLights {hasOmniLights}")
    if hasOmniLights:
        omniLights = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2OmniLight, nullMask)

    spotLights = []
    hasSpotLights = nullMask.getOptional()
    print(f"## SpotLights {hasSpotLights}")
    if hasSpotLights:
        spotLights = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2SpotLight, nullMask)

    sprites = []
    hasSprites = nullMask.getOptional()
    print(f"## Sprites {hasSprites}")
    if hasSprites:
        sprites = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Sprite, nullMask)

    skins = []
    hasSkins = nullMask.getOptional()
    print(f"## Skins {hasSkins}")
    if hasSkins:
        skins = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2Skin, nullMask)

    vertexBuffers = []
    hasVertexBuffers = nullMask.getOptional()
    print(f"## Vertex buffers {hasVertexBuffers}")
    if hasVertexBuffers:
        vertexBuffers = AlternativaProtocol.readObjectArray(package, A3D2Objects.A3D2VertexBuffer, nullMask)

    return [] #TODO

def readFromFile(file):
    package = readPackage(file)
    nullMask = AlternativaProtocol.OptionalMask()
    nullMask.read(package)
    versionMajor, versionMinor = readVersion(package)
    objects = readObjects(package, nullMask)