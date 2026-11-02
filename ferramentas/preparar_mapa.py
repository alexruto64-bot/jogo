# Converte um terreno escaneado (OBJ, FBX, glTF) num mapa do jogo:
#   modelo.glb  -> malha reduzida com a foto do terreno (WebP), para desenhar
#   altura.png  -> alturas do chão (R e G = 16 bits; B = 255 onde dá para pisar)
#   mapa.json   -> tamanho, alturas, ponto de partida e cor do chão
# Uso: python3 -I preparar_mapa.py '<json de opções>'
#   opções: entrada, saida, nome, tri (triângulos), modo ('topo' ou 'piso'), tam (lado em metros, 0 = manter),
#           cima ('auto', 'x', '-x', 'y', '-y', 'z', '-z'), tex (lado máximo da textura), n (grade de alturas)
import bpy, bmesh, os, sys, json, math, glob, tempfile
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
O = json.loads(sys.argv[-1])
ENT, SAI = O['entrada'], O['saida']
os.makedirs(SAI, exist_ok=True)
TMP = tempfile.mkdtemp(prefix='mapa-')
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------- importa ----------
ext = os.path.splitext(ENT)[1].lower()
if ext == '.obj':
    bpy.ops.wm.obj_import(filepath=ENT, forward_axis='Y', up_axis='Z')   # coordenadas cruas
elif ext == '.fbx':
    bpy.ops.import_scene.fbx(filepath=ENT)
elif ext in ('.gltf', '.glb'):
    bpy.ops.import_scene.gltf(filepath=ENT)
elif ext == '.ply':
    bpy.ops.wm.ply_import(filepath=ENT, forward_axis='Y', up_axis='Z')
else:
    raise SystemExit('formato não suportado: ' + ext)
malhas = [o for o in bpy.data.objects if o.type == 'MESH']
for o in list(bpy.data.objects):
    if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')
for o in malhas: o.select_set(True)
bpy.context.view_layer.objects.active = malhas[0]
if len(malhas) > 1: bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = obj.data
print('importado:', len(me.polygons), 'faces,', len(me.vertices), 'vértices, materiais', [m.name if m else None for m in me.materials])

def verts():
    a = np.empty(len(me.vertices) * 3, dtype=np.float64); me.vertices.foreach_get('co', a); return a.reshape(-1, 3)

# ---------- qual lado é para cima ----------
v = verts()
cima = O.get('cima', 'z')   # 'auto' estima pela forma (falha em penhascos e encostas)
if cima == 'auto':
    amostra = v[np.random.default_rng(1).choice(len(v), min(len(v), 200000), replace=False)]
    cov = np.cov((amostra - amostra.mean(0)).T)
    w, vec = np.linalg.eigh(cov)
    eixo = vec[:, 0]   # menor variação = vertical, num terreno
    me.calc_normals_split() if hasattr(me, 'calc_normals_split') else None
    nrm = np.empty(len(me.polygons) * 3); me.polygons.foreach_get('normal', nrm); nrm = nrm.reshape(-1, 3)
    area = np.empty(len(me.polygons)); me.polygons.foreach_get('area', area)
    media = (nrm * area[:, None]).sum(0)
    if media @ eixo < 0: eixo = -eixo
    k = int(np.argmax(np.abs(eixo)))
    print('eixo vertical estimado', np.round(eixo, 3), 'variâncias', np.round(w, 2))
    if abs(eixo[k]) > 0.85: eixo = np.eye(3)[k] * np.sign(eixo[k])   # alinhado a um eixo: usa ele exato
    up = Vector(eixo)
else:
    s = -1 if cima.startswith('-') else 1
    up = Vector(np.eye(3)['xyz'.index(cima[-1])] * s)
print('para cima =', tuple(round(c, 3) for c in up))
rot = up.rotation_difference(Vector((0, 0, 1))).to_matrix().to_4x4()
me.transform(rot)
if O.get('girar_z'): me.transform(Matrix.Rotation(math.radians(O['girar_z']), 4, 'Z'))

# ---------- tira pontas soltas para baixo (erros do escaneamento) ----------
v = verts()
p1, p99 = np.percentile(v[:, 2], [1, 99])
corte = p1 - 0.25 * (p99 - p1) if O.get('cortar', True) else -np.inf
if (v[:, 2] < corte).any():
    bm = bmesh.new(); bm.from_mesh(me)
    ruins = [x for x in bm.verts if x.co.z < corte]
    bmesh.ops.delete(bm, geom=ruins, context='VERTS'); bm.to_mesh(me); bm.free()
    print('pontas cortadas abaixo de %.1f: %d vértices' % (corte, len(ruins)))
# ---------- centraliza e põe na escala ----------
v = verts()
mn, mx = v.min(0), v.max(0)
lado = max(mx[0] - mn[0], mx[1] - mn[1])
esc = O['tam'] / lado if O.get('tam') else 1.0
me.transform(Matrix.Scale(esc, 4) @ Matrix.Translation(Vector((-(mn[0] + mx[0]) / 2, -(mn[1] + mx[1]) / 2, -mn[2]))))
v = verts(); mn, mx = v.min(0), v.max(0)
print('tamanho (m): %.1f x %.1f, altura %.1f; escala aplicada %.4f' % (mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2], esc))
# ---------- para objetos postos num mapa: nivela pelo chão e recorta a base ----------
if O.get('nivelar'):
    # plano que passa pelos pontos mais baixos (o chão em volta das pedras), tirado de todos os pontos
    v = verts(); baixo = v[v[:, 2] < np.percentile(v[:, 2], 25)]
    A = np.c_[baixo[:, 0], baixo[:, 1], np.ones(len(baixo))]
    coef = np.linalg.lstsq(A, baixo[:, 2], rcond=None)[0]
    v[:, 2] -= v[:, 0] * coef[0] + v[:, 1] * coef[1] + coef[2]
    me.vertices.foreach_set('co', v.ravel()); me.update()
    print('nivelado: inclinação %.3f, %.3f' % (coef[0], coef[1]))
if O.get('corte') is not None:
    bm = bmesh.new(); bm.from_mesh(me)
    fora = [x for x in bm.verts if x.co.z < O['corte']]
    bmesh.ops.delete(bm, geom=fora, context='VERTS')
    bmesh.ops.translate(bm, verts=bm.verts[:], vec=Vector((0, 0, -O['corte'])))
    bm.to_mesh(me); bm.free()
    print('base recortada em %.2f m: %d vértices fora; sobram %d faces' % (O['corte'], len(fora), len(me.polygons)))
    v = verts(); mn, mx = v.min(0), v.max(0)
if O.get('paredes_caixa'):
    # paredes retas da caixa que veio junto com o escaneado: faces de pé, viradas para x ou y, perto da borda
    nrm = np.empty(len(me.polygons) * 3); me.polygons.foreach_get('normal', nrm); nrm = nrm.reshape(-1, 3)
    cen = np.empty(len(me.polygons) * 3); me.polygons.foreach_get('center', cen); cen = cen.reshape(-1, 3)
    vv = verts(); lo, hi = vv.min(0), vv.max(0); m = O['paredes_caixa']
    perto_x = (cen[:, 0] < lo[0] + m) | (cen[:, 0] > hi[0] - m)
    perto_y = (cen[:, 1] < lo[1] + m) | (cen[:, 1] > hi[1] - m)
    parede = (np.abs(nrm[:, 2]) < 0.25) & (((np.abs(nrm[:, 0]) > 0.9) & perto_x) | ((np.abs(nrm[:, 1]) > 0.9) & perto_y))
    # e o que estiver colado na borda e baixo (rodapé da caixa)
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in np.nonzero(parede)[0]], context='FACES'); bm.to_mesh(me); bm.free()
    print('paredes da caixa tiradas: %d faces' % int(parede.sum()))
if O.get('area_max'):
    # faces enormes perto das faces normais do escaneamento são de caixas e placas que vieram junto: saem
    area = np.empty(len(me.polygons)); me.polygons.foreach_get('area', area)
    limite = np.median(area) * O['area_max']
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    grandes = [bm.faces[i] for i in np.nonzero(area > limite)[0]]
    bmesh.ops.delete(bm, geom=grandes, context='FACES'); bm.to_mesh(me); bm.free()
    print('faces enormes tiradas: %d (acima de %.4f m²)' % (len(grandes), limite))
if O.get('agua') and O.get('foto'):
    # tira as faces cor de água (verde-azulado), olhando a foto no centro de cada face
    foto = np.asarray(Image.open(O['foto']).convert('RGB')).astype(np.int16)
    hh, ww = foto.shape[:2]
    uvl = me.uv_layers.active
    uv = np.empty(len(me.loops) * 2); uvl.data.foreach_get('uv', uv); uv = uv.reshape(-1, 2)
    tot = np.empty(len(me.polygons), dtype=np.int64); me.polygons.foreach_get('loop_total', tot)
    face = np.repeat(np.arange(len(me.polygons)), tot)
    c = np.zeros((len(me.polygons), 2)); np.add.at(c, face, uv); c /= tot[:, None]
    px = np.clip((c[:, 0] % 1) * ww, 0, ww - 1).astype(int); py = np.clip((1 - c[:, 1] % 1) * hh, 0, hh - 1).astype(int)
    r, g, b = foto[py, px, 0], foto[py, px, 1], foto[py, px, 2]
    agua = (g - r > O.get('agua_g', 10)) & (b - r > O.get('agua_b', 6))
    if O.get('agua_baixa'):
        # perto do nível da água, tira também o que é cinza-azulado (água rasa refletindo o céu)
        cen = np.empty(len(me.polygons) * 3); me.polygons.foreach_get('center', cen); cen = cen.reshape(-1, 3)
        agua |= (cen[:, 2] < O['agua_baixa']) & (b - r > -3)
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in np.nonzero(agua)[0]], context='FACES')
    # pedaços soltos pequenos também saem
    vistos, ilhas = set(), []
    for f0 in bm.faces:
        if f0.index in vistos: continue
        pilha, ilha = [f0], []
        vistos.add(f0.index)
        while pilha:
            f = pilha.pop(); ilha.append(f)
            for e in f.edges:
                for f2 in e.link_faces:
                    if f2.index not in vistos: vistos.add(f2.index); pilha.append(f2)
        ilhas.append(ilha)
    ilhas.sort(key=len, reverse=True)
    soltas = [f for il in ilhas if len(il) < O.get('ilha_min', 2000) for f in il]
    bmesh.ops.delete(bm, geom=soltas, context='FACES')
    bm.to_mesh(me); bm.free()
    print('água tirada: %d faces; pedaços soltos tirados: %d faces; sobram %d faces' % (int(agua.sum()), len(soltas), len(me.polygons)))
    v = verts(); mn, mx = v.min(0), v.max(0)
print('alturas (percentis 1, 50, 99):', np.round(np.percentile(v[:, 2], [1, 50, 99]), 2))

# ---------- reduz a malha ----------
bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.triangulate(bm, faces=bm.faces[:]); bm.to_mesh(me); bm.free()
tri = len(me.polygons)
if tri > O['tri']:
    mod = obj.modifiers.new('reduzir', 'DECIMATE'); mod.ratio = O['tri'] / tri; mod.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=mod.name)
print('triângulos: %d -> %d' % (tri, len(me.polygons)))
if O.get('aresta_max'):
    # triângulos compridos demais (lascas que ligam pontos distantes) saem
    bm = bmesh.new(); bm.from_mesh(me)
    lascas = [f for f in bm.faces if max(e.calc_length() for e in f.edges) > O['aresta_max']]
    bmesh.ops.delete(bm, geom=lascas, context='FACES'); bm.to_mesh(me); bm.free()
    print('lascas tiradas: %d faces' % len(lascas))

# ---------- materiais: só a foto (cor), reduzida ----------
pasta = os.path.dirname(os.path.dirname(ENT)) if os.path.basename(os.path.dirname(ENT)) != 'source' else os.path.dirname(os.path.dirname(ENT))
raiz = O.get('raiz', os.path.dirname(ENT))
def acha_imagem(img):
    f = bpy.path.abspath(img.filepath) if img.filepath else ''
    if f and os.path.exists(f): return f
    if img.packed_file or (img.has_data and not img.filepath):
        dst = os.path.join(TMP, 'embutida_%s.png' % len(os.listdir(TMP)))
        img.filepath_raw = dst; img.file_format = 'PNG'; img.save()
        return dst
    base = os.path.splitext(os.path.basename(img.filepath or img.name))[0].lower()
    for c in glob.glob(os.path.join(raiz, '**', '*'), recursive=True):
        if os.path.splitext(os.path.basename(c))[0].lower() == base and c.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff')): return c
    return None
def imagem_cor(mat):
    if not mat or not mat.use_nodes: return None
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            l = n.inputs['Base Color'].links
            if l:
                no = l[0].from_node
                while no.type != 'TEX_IMAGE' and no.inputs and any(i.links for i in no.inputs):
                    no = [i for i in no.inputs if i.links][0].links[0].from_node
                if no.type == 'TEX_IMAGE' and no.image: return no.image
    for n in mat.node_tree.nodes:
        if n.type == 'TEX_IMAGE' and n.image and not any(t in n.image.name.lower() for t in ('normal', 'occlusion', 'rough', 'ao')): return n.image
    return None
fotos = []
for i, mat in enumerate(me.materials):
    img = imagem_cor(mat)
    f = acha_imagem(img) if img else None
    if not f and O.get('foto'): f = O['foto']
    fotos.append(f)
print('fotos:', fotos)
usadas = [f for f in fotos if f]
# fotos em arquivos .webp à parte, quase na resolução original (até 8192 px; com várias fotos, até 4096 cada)
lado_tex = O.get('tex') or (8192 if len(set(usadas)) <= 1 else 4096)
arquivos = {}
cores = []
reduzidas = {}
for f in set(usadas):
    im = Image.open(f).convert('RGB')
    w0, h0 = im.size
    k = min(1, lado_tex / max(w0, h0))
    if k < 1: im = im.resize((max(1, round(w0 * k)), max(1, round(h0 * k))), Image.LANCZOS)
    cores.append(np.asarray(im.resize((64, 64))).reshape(-1, 3).mean(0))
    dst = os.path.join(TMP, 'f%d.jpg' % len(reduzidas)); im.resize((256, 256)).save(dst, quality=90)   # só para o Blender
    reduzidas[f] = dst
    nome = 'foto%d.webp' % len(arquivos); arquivos[f] = nome
    for q in (82, 74, 66, 58):
        im.save(os.path.join(SAI, nome), 'WEBP', quality=q, method=5)
        if os.path.getsize(os.path.join(SAI, nome)) < 14.5e6: break
    print('  %s: %d KB (qualidade %d)' % (nome, os.path.getsize(os.path.join(SAI, nome)) // 1024, q))
    print('foto %s: %dx%d -> %dx%d' % (os.path.basename(f), w0, h0, im.size[0], im.size[1]))
novos = []
for i, f in enumerate(fotos):
    m = bpy.data.materials.new('chao%d' % i); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = 1.0; p.inputs['Metallic'].default_value = 0.0
    if f:
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(reduzidas[f], check_existing=True)
        nt.links.new(t.outputs['Color'], p.inputs['Base Color'])
    else:
        p.inputs['Base Color'].default_value = (0.4, 0.36, 0.3, 1)
    novos.append(m)
for i, m in enumerate(novos): me.materials[i] = m
texturas = {'chao%d' % i: arquivos[f] for i, f in enumerate(fotos) if f}
cor = (np.mean(cores, 0) / 255).tolist() if cores else [0.4, 0.36, 0.3]

# ---------- grade de alturas ----------
v = verts(); mn, mx = v.min(0), v.max(0)
n = O.get('n', 512)
ladoX, ladoY = float(mx[0] - mn[0]), float(mx[1] - mn[1])
L = 2 * max(abs(mn[0]), abs(mx[0]), abs(mn[1]), abs(mx[1])) * 1.02   # quadrado centrado na origem que cobre tudo
bvh = BVHTree.FromObject(obj, bpy.context.evaluated_depsgraph_get())
H = np.zeros((n, n)); ok = np.zeros((n, n), bool)
topo = O.get('modo', 'topo') == 'topo'
z0, z1 = float(mn[2]) - 5, float(mx[2]) + 5
for k in range(n):                      # linha k = z do jogo, de -L/2 a +L/2 (z do jogo = -y do Blender)
    zj = -L / 2 + k / (n - 1) * L
    for i in range(n):
        xj = -L / 2 + i / (n - 1) * L
        if topo: hit = bvh.ray_cast(Vector((xj, -zj, z1)), Vector((0, 0, -1)))
        else: hit = bvh.ray_cast(Vector((xj, -zj, z0)), Vector((0, 0, 1)))
        if hit[0] is not None: H[k, i] = hit[0].z; ok[k, i] = True
print('células com chão: %.0f%%' % (100 * ok.mean()))
# fora do escaneado: copia a altura do vizinho mais próximo (só para não dar degrau no desenho; lá não se anda)
from scipy import ndimage
_, (ik, ii) = ndimage.distance_transform_edt(~ok, return_indices=True)
H = H[ik, ii]
# aparas: tira as bordas finas e ilhas soltas do contorno escaneado
ok = ndimage.binary_erosion(ok, iterations=2)
rot, nlab = ndimage.label(ok)
if nlab > 1:
    tam = ndimage.sum(ok, rot, range(1, nlab + 1)); ok = rot == (1 + int(np.argmax(tam)))
hmin, hmax = float(H.min()), float(H.max())
q = np.round((H - hmin) / max(1e-6, hmax - hmin) * 65535).astype(np.uint32)
rgb = np.stack([(q >> 8).astype(np.uint8), (q & 255).astype(np.uint8), np.where(ok, 255, 0).astype(np.uint8)], -1)
Image.fromarray(rgb, 'RGB').save(os.path.join(SAI, 'altura.png'), optimize=True)
# ponto de partida: perto do centro, onde o chão é plano
gk, gi = np.gradient(H, L / (n - 1))
inclina = np.hypot(gk, gi)
plano = ndimage.uniform_filter(inclina, 7)
kk, ii2 = np.mgrid[0:n, 0:n]
dist = np.hypot(kk - n / 2, ii2 - n / 2) / n
custo = np.where(ok & ndimage.binary_erosion(ok, iterations=8), plano + dist * 1.5, np.inf)
if not np.isfinite(custo).any(): custo = np.where(ok, plano + dist * 1.5, np.inf)
k0, i0 = np.unravel_index(np.argmin(custo), custo.shape)
inicio = {'x': round(-L / 2 + i0 / (n - 1) * L, 2), 'z': round(-L / 2 + k0 / (n - 1) * L, 2)}

# ---------- coordenadas da foto: cada face volta para o quadrado 0..1 (fotos lado a lado, tipo UDIM) ----------
uvl = me.uv_layers.active
if uvl:
    uv = np.empty(len(me.loops) * 2); uvl.data.foreach_get('uv', uv); uv = uv.reshape(-1, 2)
    print('UV antes: min', np.round(uv.min(0), 3), 'max', np.round(uv.max(0), 3))
    ini = np.empty(len(me.polygons), dtype=np.int64); me.polygons.foreach_get('loop_start', ini)
    tot = np.empty(len(me.polygons), dtype=np.int64); me.polygons.foreach_get('loop_total', tot)
    face = np.repeat(np.arange(len(me.polygons)), tot)
    centro = np.zeros((len(me.polygons), 2)); np.add.at(centro, face, uv); centro /= tot[:, None]
    uv -= np.floor(centro)[face]
    uvl.data.foreach_set('uv', uv.ravel())
    print('UV depois: min', np.round(uv.min(0), 3), 'max', np.round(uv.max(0), 3))
# ---------- exporta ----------
bpy.ops.object.shade_smooth()
glb = os.path.join(SAI, 'modelo.glb')
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', export_yup=True, export_normals=False, export_texcoords=True,
                          export_image_format='NONE', export_materials='EXPORT',
                          export_animations=False, export_skins=False)
meta = {'nome': O['nome'], 'n': n, 'lado': round(L, 3), 'ladoX': round(ladoX, 2), 'ladoZ': round(ladoY, 2),
        'ymin': round(hmin, 4), 'ymax': round(hmax, 4), 'modo': 'topo' if topo else 'piso', 'inicio': inicio,
        'cor': [round(c, 3) for c in cor], 'triangulos': len(me.polygons), 'texturas': texturas}
meta.update(O.get('extra', {}))
json.dump(meta, open(os.path.join(SAI, 'mapa.json'), 'w'), ensure_ascii=False, indent=1)
print('PRONTO', json.dumps(meta, ensure_ascii=False), 'glb %d KB' % (os.path.getsize(glb) // 1024))
