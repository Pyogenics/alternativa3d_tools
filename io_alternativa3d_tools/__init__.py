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
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty

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
Registration
'''
class ImportA3D(Operator, ImportHelper):
	bl_idname = "alternativa3d.importa3d"
	bl_label = "Import A3D"

	filter_glob: StringProperty(default="*.a3d", options={'HIDDEN'})

	import_lights: BoolProperty(name="Import lights")
	import_anims: BoolProperty(name="Import animations")
	import_decals: BoolProperty(name="Import decals")
	import_cubemaps: BoolProperty(name="Import cubemaps")
	import_joints: BoolProperty(name="Import joints")
	import_sprites: BoolProperty(name="Import sprites")
	import_skins: BoolProperty(name="Import skins")


	def invoke(self, context, event):
		return ImportHelper.invoke(self, context, event)

	def execute(self, context):
		return {"FINISHED"}

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