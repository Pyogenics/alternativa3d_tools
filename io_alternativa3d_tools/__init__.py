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

import bpy
import bmesh
from bpy.types import Operator, PropertyGroup
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, FloatProperty

from .A3D2 import A3D2
from .A3D1 import A3D1
from .IOTools import unpackStream

bl_info = {
    "name": "Alternativa3d tools",
    "description": "Support for Alternativa3D (A3D) format files",
    "author": "David E Jones http://davidejones.com, Pyogenics https://www.github.com/Pyogenics",
    "version": (2, 0, 0),
    "blender": (4, 0, 0),
    "location": "File > Import-Export",
    "doc_url": "https://github.com/davidejones/alternativa3d_tools/",
    "tracker_url": "https://github.com/davidejones/alternativa3d_tools/issues",
    "category": "Import-Export"
}

'''
Blender IO drivers
'''
class BlenderA3DImporter:
    def __init__(self):
        self.a3d = None
        self.version = 0

    def read(self, stream):
        print("Starting A3D read")

        # Determine version of A3D we're dealing with
        version, = unpackStream(">H", stream)
        if version == 1:
            print("This is probably an A3D1 file")
            self.a3d = A3D1()
            self.version = 1
            stream.seek(4)
        else:
            print("This is probably an A3D2 file")
            self.a3d = A3D2()
            self.version = 2
            stream.seek(0)

        # Read
        self.a3d.read(stream)

    '''
    Blender import
    '''
    def A3DMatrix2BlenderMatrix(self, a3dMatrix):
        pass

    def processGeometry(self, geometry):
        print("Processing geometry")
        bm = bmesh.new()

        # Aggregate data
        positions = []
        normals = []
        tangents = []
        joints = []
        UV0 = []
        UV1 = []
        faces = []

        if geometry.vertexBuffers != None:
            for vertexBuffer in geometry.vertexBuffers:
                positions += vertexBuffer.positions
                normals += vertexBuffer.normals
                tangents += vertexBuffer.tangents
                joints += vertexBuffer.joints
                UV0 += vertexBuffer.UV0
                UV1 += vertexBuffer.UV1
        if geometry.indexBuffer != None:
            faces = geometry.indexBuffer.faces

        # Build mesh
        for position in positions:
            bm.verts.new(position)
        bm.verts.ensure_lookup_table()
        bm.verts.index_update()

        for face in faces:
            i0, i1, i2 = face

            # FIXME: Some models have duplicate indices in one face or even duplicate faces
            try:
                bm.faces.new([
                    bm.verts[i0],
                    bm.verts[i1],
                    bm.verts[i2]
                ])
            except: pass
        if len(UV0) != 0:
            UVLayer = bm.loops.layers.uv.new("UV0")
            for face in bm.faces:
                for loop in face.loops: loop[UVLayer].uv = UV0[loop.vert.index]
        if len(UV1) != 0:
            UVLayer = bm.loops.layers.uv.new("UV1")
            for face in bm.faces:
                for loop in face.loops: loop[UVLayer].uv = UV1[loop.vert.index]

        # Finalise
        me = bpy.data.meshes.new(f"{geometry.id}")
        bm.to_mesh(me)
        me.update()

        return me

    def blenderImport(self):
        print("Importing A3D into blender")

        for obj in self.a3d.objects:
            name = ""
            mesh = None
            if obj.name != None:
                name = obj.name  
            if obj.geometryId != None:
                geometry = self.a3d.getGeometryByID(obj.geometryId)
                mesh = self.processGeometry(geometry)          
            
            # We have enough data to add the object to the active collection now
            ob = bpy.data.objects.new(name, mesh)
            bpy.context.collection.objects.link(ob)

            if obj.transform != None:
                mat = self.A3DMatrix2BlenderMatrix(obj.transform.matrix)
                #ob.matrix_local = mat
            if obj.visible != None:
                ob.hide_set(obj.visible)

'''
Menus
'''
class ImportA3D(Operator, ImportHelper):
    bl_idname = "alternativa3d.importa3d"
    bl_label = "Import A3D"
    bl_options = {'PRESET', 'UNDO'}

    filter_glob: StringProperty(default="*.a3d", options={'HIDDEN'})

    scale: FloatProperty(name="Scale", min=0.0, soft_min=0.0, default=1.0)

    # alternativa3d_import_data
    import_geometry: BoolProperty(name="Import geometry", default=True)
    import_materials: BoolProperty(name="Import materials", default=True)
    import_objects: BoolProperty(name="Import objects", default=True)
    import_animation: BoolProperty(name="Import animation", default=True)
    import_skin: BoolProperty(name="Import skin", default=True)
    import_lights: BoolProperty(name="Import lights", default=True)
    import_decals: BoolProperty(name="Import decals", default=True)
    import_sprites: BoolProperty(name="Import sprites", default=True)

    def draw(self, context):
        self.layout.prop(self, "scale")
        import_panel_data(self.layout, self)

    def invoke(self, context, event):
        return self.invoke_popup(context)

    def execute(self, context):
        with open(self.filepath, "rb") as file:
            a3dImporter = BlenderA3DImporter()
            a3dImporter.read(file)
            a3dImporter.blenderImport()

        return {"FINISHED"}

def import_panel_data(layout, operator):
    header, body = layout.panel("alternativa3d_import_data", default_closed=False)
    header.label(text="Data")
    if body:
        body.prop(operator, "import_geometry")
        body.prop(operator, "import_materials")
        body.prop(operator, "import_objects")
        body.prop(operator, "import_animation")
        body.prop(operator, "import_skin")
        body.prop(operator, "import_lights")
        body.prop(operator, "import_decals")
        body.prop(operator, "import_sprites")

class ExportA3D(Operator, ExportHelper):
    bl_idname = "alternativa3d.exporta3d"
    bl_label = "Import A3D"

    filter_glob: StringProperty(default="*.a3d", options={'HIDDEN'})
    filename_ext: StringProperty(default=".a3d", options={'HIDDEN'})

    apply_modifiers: BoolProperty(name="Apply modifiers", description="Apply modifiers before exporting")

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        return {"FINISHED"}

def menu_func_import(self, context):
    self.layout.operator(ImportA3D.bl_idname, text="Alternativa3D (.a3d)")

def menu_func_export(self, context):
    self.layout.operator(ExportA3D.bl_idname, text="Alternativa3D (.a3d)")

'''
Register
'''
classes = [
    ImportA3D,
    ExportA3D
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()