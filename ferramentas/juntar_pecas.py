# Junta peças de um kit glTF (uma por arquivo) num glb só: cada peça vira um objeto com o nome dela;
# imagens e materiais repetidos viram um só; texturas em WebP.
# Uso: python3 -I juntar_pecas.py <pasta do kit> <saida.glb> <peça> <peça> ...
import bpy, os, sys
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
K, SAIDA, PECAS = args[0], args[1], args[2:]
bpy.ops.wm.read_factory_settings(use_empty=True)
for nome in PECAS:
    antes = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(K, nome + '.gltf'))
    novos = [o for o in bpy.data.objects if o not in antes]
    malhas = [o for o in novos if o.type == 'MESH']
    for o in novos:
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
    bpy.ops.object.select_all(action='DESELECT')
    for o in malhas: o.select_set(True)
    bpy.context.view_layer.objects.active = malhas[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if len(malhas) > 1: bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = nome; ob.data.name = nome
    for o in novos:
        if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    d = ob.dimensions
    print('%-22s %6.2f x %6.2f x %6.2f  %6d faces  materiais %s' % (nome, d.x, d.y, d.z, len(ob.data.polygons), [m.name for m in ob.data.materials]))
por_arquivo = {}
for img in list(bpy.data.images):
    chave = os.path.basename(bpy.path.abspath(img.filepath)) or img.name.split('.')[0]
    if chave in por_arquivo: img.user_remap(por_arquivo[chave]); bpy.data.images.remove(img)
    else: por_arquivo[chave] = img
base = {}
for m in list(bpy.data.materials):
    chave = m.name.rsplit('.', 1)[0] if m.name[-4:-3] == '.' and m.name[-3:].isdigit() else m.name
    if chave in base: m.user_remap(base[chave]); bpy.data.materials.remove(m)
    else: base[chave] = m
print('imagens', [(i.name, tuple(i.size)) for i in bpy.data.images])
bpy.ops.export_scene.gltf(filepath=SAIDA, export_format='GLB', export_image_format='WEBP', export_image_quality=82,
                          export_apply=True, export_yup=True, export_animations=False)
print('GLB', os.path.getsize(SAIDA) // 1024, 'KB')
