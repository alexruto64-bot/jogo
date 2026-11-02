# Prepara um item (glb) para o jogo: altura em metros, base no chão, centro em x/z, texturas até 2048 px em WebP.
# Uso: python3 -I preparar_item.py entrada.glb saida.glb altura_m
import bpy, sys, os
from mathutils import Vector, Matrix
ENT, SAI, ALT = sys.argv[-3], sys.argv[-2], float(sys.argv[-1])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=ENT)
malhas = [o for o in bpy.data.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in malhas: o.select_set(True)
bpy.context.view_layer.objects.active = malhas[0]
if len(malhas) > 1: bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
obj.parent = None
for o in list(bpy.data.objects):
    if o is not obj: bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
cs = [obj.matrix_world @ v.co for v in obj.data.vertices]
mn = Vector((min(c.x for c in cs), min(c.y for c in cs), min(c.z for c in cs)))
mx = Vector((max(c.x for c in cs), max(c.y for c in cs), max(c.z for c in cs)))
esc = ALT / (mx.z - mn.z)
obj.data.transform(Matrix.Scale(esc, 4) @ Matrix.Translation(Vector((-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z))))
for img in bpy.data.images:
    if img.size[0] > 2048: img.scale(2048, 2048 * img.size[1] // img.size[0])
d = obj.dimensions
print('tamanho (m): %.2f x %.2f x %.2f, %d faces, imagens %s' % (d.x, d.y, d.z, len(obj.data.polygons), [(i.name, tuple(i.size)) for i in bpy.data.images]))
bpy.ops.export_scene.gltf(filepath=SAI, export_format='GLB', export_image_format='WEBP', export_image_quality=85, export_animations=False)
print('GLB', os.path.getsize(SAI) // 1024, 'KB')
