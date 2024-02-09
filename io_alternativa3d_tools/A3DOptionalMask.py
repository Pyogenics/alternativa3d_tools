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

class A3DOptionalMask:
    def __init__(self, optionalMaskBytes, offset):
        self.optionalMask = []
        
        optionalMaskBytes = BytesIO(optionalMaskBytes)
        # Process first byte (the first byte is missing some bits on some null-mask configs)
        for bitI in range(8 - offset):
            maskByte = int.from_bytes(optionalMaskBytes.read(1))
            self.optionalMask.append(
                bool(maskByte & (2**bitI))
            )

        for maskByte in optionalMaskBytes:
            for bitI in range(8):
                maskByte = int.from_bytes(maskByte)
                self.optionalMask.append(
                    bool(maskByte & (2**bitI))
                )

    def getOptionals(self, count=1):
        optionals = ()
        for _ in range(count):
            optionals += (self.optionalMask.pop(0),)
        return optionals