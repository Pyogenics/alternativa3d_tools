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

from . import A3DArray
from . import A3DObjects
from .A3DOptionalMask import A3DOptionalMask

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

def readNullMask(package):
    # Read "Null-mask" field
    nullMask = b""

    nullMaskField = int.from_bytes(package.read(1), "little")
    nullMaskType = nullMaskField & 0b10000000
    if nullMaskType == 0:
        # Short null-mask: 5-29 bits
        print("Short nullmask")
        nullMaskLength = nullMaskField & 0b01100000
        
        nullMask += bytes(nullMaskField & 0b00011111)
        nullMask += package.read(nullMaskLength) # 1,2 or 3 bytes
        nullMask = A3DOptionalMask(nullMask, 3) # we have 5 bits from the field byte
    else:
        # Long null-mask: 64 - 4194304 bytes
        print("Long nullmask")
        nullMaskLengthSize = nullMaskField & 0b01000000
        nullMaskLength = nullMaskField & 0b0011111
        if nullMaskLengthSize == 1:
            # Long length: 22 bits
            print("> Long length")
            nullMaskLength += int.from_bytes(package.read(2), "little")
        else:
            # Short length: 6 bits
            print("> Short length")
            
        nullMask += package.read(nullMaskLength)
        nullMask = A3DOptionalMask(nullMask, 0)
        
        return nullMask

def readVersion(package):
    # Read "version" field
    versionMajor = int.from_bytes(package.read(2), "big")
    versionMinor = int.from_bytes(package.read(2), "big")
    print(f"A3D version: {versionMajor}.{versionMinor}")

    return (versionMajor, versionMinor)

def readObjects(package, nullMask):
    ambientLights = []
    hasAmbientLights = nullMask.getOptional()
    print(f"## AmbientLights {hasAmbientLights}")
    if hasAmbientLights:
        ambientLights = A3DArray.readA3DObjectArray(package, A3DObjects.ambientLight, nullMask)

    animationClips = []
    hasAnimationClips = nullMask.getOptional()
    print(f"## AnimationClips {hasAnimationClips}")
    if hasAnimationClips:
        animationClips = A3DArray.readA3DObjectArray(package, A3DObjects.animationClip, nullMask)

    animationTracks = []
    hasAnimationTracks = nullMask.getOptional()
    print(f"## AnimationTracks {hasAnimationTracks}")
    if hasAnimationTracks:
        animationTracks = A3DArray.readA3DObjectArray(package, A3DObjects.animationTrack, nullMask)

    boxes = []
    hasBoxes = nullMask.getOptional()
    print(f"## Boxes {hasBoxes}")
    if hasBoxes:
        boxes = A3DArray.readA3DObjectArray(package, A3DObjects.box, nullMask)

    cubeMaps = []
    hasCubeMaps = nullMask.getOptional()
    print(f"## CubeMaps {hasCubeMaps}")
    if hasCubeMaps:
        cubeMaps = A3DArray.readA3DObjectArray(package, A3DObjects.cubeMaps, nullMask)

    decals = []
    hasDecals = nullMask.getOptional()
    print(f"## Decals {hasDecals}")
    if hasDecals:
        decals = A3DArray.readA3DObjectArray(package, A3DObjects.decal, nullMask)

    directionalLights = []
    hasDirectionalLights = nullMask.getOptional()
    print(f"## DirectionalLights {hasDirectionalLights}")
    if hasDirectionalLights:
        directionalLights = A3DArray.readA3DObjectArray(package, A3DObjects.directionalLight, nullMask)

    images = []
    hasImages = nullMask.getOptional()
    print(f"## Images {hasImages}")
    if hasImages:
        images = A3DArray.readA3DObjectArray(package, A3DObjects.image, nullMask)

    indexBuffers = []
    hasIndexBuffers = nullMask.getOptional()
    print(f"## IndexBuffers {hasIndexBuffers}")
    if hasIndexBuffers:
        indexBuffers = A3DArray.readA3DObjectArray(package, A3DObjects.indexBuffer, nullMask)

    joints = []
    hasJoints = nullMask.getOptional()
    print(f"## Joints {hasJoints}")
    if hasJoints:
        joints = A3DArray.readA3DObjectArray(package, A3DObjects.joint, nullMask)

    maps = []
    hasMaps = nullMask.getOptional()
    print(f"## Maps {hasMaps}")
    if hasMaps:
        maps = A3DArray.readA3DObjectArray(package, A3DObjects.map, nullMask)

    materials = []
    hasMaterials = nullMask.getOptional()
    print(f"## Materials {hasMaterials}")
    if hasMaterials:
        materials = A3DArray.readA3DObjectArray(package, A3DObjects.material, nullMask)

    meshes = []
    hasMeshes = nullMask.getOptional()
    print(f"## Meshes {hasMeshes}")
    if hasMeshes:
        meshes = A3DArray.readA3DObjectArray(package, A3DObjects.mesh, nullMask)

    objects = []
    hasObjects = nullMask.getOptional()
    print(f"## Objects {hasObjects}")
    if hasObjects:
        objects = A3DArray.readA3DObjectArray(package, A3DObjects.object, nullMask)

    omniLights = []
    hasOmniLights = nullMask.getOptional()
    print(f"## OmniLights {hasOmniLights}")
    if hasOmniLights:
        omniLights = A3DArray.readA3DObjectArray(package, A3DObjects.omniLight, nullMask)

    spotLights = []
    hasSpotLights = nullMask.getOptional()
    print(f"## SpotLights {hasSpotLights}")
    if hasSpotLights:
        spotLights = A3DArray.readA3DObjectArray(package, A3DObjects.spotLight, nullMask)

    sprites = []
    hasSprites = nullMask.getOptional()
    print(f"## Sprites {hasSprites}")
    if hasSprites:
        sprites = A3DArray.readA3DObjectArray(package, A3DObjects.sprite, nullMask)

    skins = []
    hasSkins = nullMask.getOptional()
    print(f"## Skins {hasSkins}")
    if hasSkins:
        skins = A3DArray.readA3DObjectArray(package, A3DObjects.skin, nullMask)

    vertexBuffers = []
    hasVertexBuffers = nullMask.getOptional()
    print(f"## Vertex buffers {hasVertexBuffers}")
    if hasVertexBuffers:
        vertexBuffers = A3DArray.readA3DObjectArray(package, A3DObjects.vertexBuffer, nullMask)

    return [] #TODO

def readFromFile(file):
    package = readPackage(file)
    nullMask = readNullMask(package)
    versionMajor, versionMinor = readVersion(package)
    objects = readObjects(package, nullMask)