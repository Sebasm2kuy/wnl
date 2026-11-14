#!/usr/bin/env python3
"""Verificación del SVG v2 del mapa de la Habitación WNL.

Comprueba estructura (dimensiones, conteos, numeración, coordenadas) y,
desde la iteración de corrección QA, también SOLAPES VISUALES entre
elementos que deben leerse por separado:

- 15 hotspots fijos (H01–H14, H16) + H15 CONTEXTUAL sin marcador:
  se documenta en la leyenda; el verificador exige su mención textual
  y la ausencia de marcador fijo.
- La caja de la leyenda no debe intersecar muebles, colisiones, hotspots,
  zonas de aproximación ni rótulos de mobiliario.
- Los marcadores de hotspot no deben intersecar rótulos de mobiliario.
- Las cajas de texto estimadas (ancho ~ 0.62·tamaño·caracteres) no deben
  intersecarse entre sí (salvo pares permitidos por diseño).

Una ejecución en verde no sustituye la revisión visual rasterizada;
esta se realiza y documenta aparte (REVISION_QA_PLANO_HABITACION_WNL_V2.md).
"""
import os
import re
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(AQUI, '..', 'MAPA_VISUAL_HOTSPOTS_COLISIONES_WNL_v2.svg')
tree = ET.parse(SVG)
root = tree.getroot()
ns = {'s': 'http://www.w3.org/2000/svg'}
errors, notes = [], []


# ---------- utilidades ----------
def caja_rect(el):
    return (float(el.get('x', '0')), float(el.get('y', '0')),
            float(el.get('x', '0')) + float(el.get('width', '0')),
            float(el.get('y', '0')) + float(el.get('height', '0')))


def caja_circ(el):
    cx, cy, r = float(el.get('cx')), float(el.get('cy')), float(el.get('r'))
    return (cx - r, cy - r, cx + r, cy + r)


def caja_ellipse(el):
    cx, cy = float(el.get('cx')), float(el.get('cy'))
    return (cx - float(el.get('rx')), cy - float(el.get('ry')),
            cx + float(el.get('rx')), cy + float(el.get('ry')))


def caja_de(el):
    tag = el.tag.split('}')[-1]
    if tag == 'text':
        return caja_texto(el)
    return {'rect': caja_rect, 'circle': caja_circ, 'ellipse': caja_ellipse}[tag](el)


def caja_texto(el):
    """Caja estimada de un <text> (fuente sans ~0.62·em por carácter)."""
    size = 24.0
    m = re.match(r'(\d+)', el.get('font-size') or '')
    cls = el.get('class') or ''
    if m:
        size = float(m.group(1))
    elif 'large' in cls:
        size = 42.0
    elif 'med' in cls:
        size = 30.0
    elif 'small' in cls:
        size = 24.0
    txt = el.text or ''
    w = 0.62 * size * len(txt)
    x, y = float(el.get('x')), float(el.get('y'))
    return (x, y - 0.78 * size, x + w, y + 0.22 * size)


def intersecan(a, b, margen=0.0):
    return not (a[2] + margen <= b[0] or b[2] + margen <= a[0] or
                a[3] + margen <= b[1] or b[3] + margen <= a[1])


def dentro(a, b, margen=0.0):
    return (a[0] >= b[0] - margen and a[1] >= b[1] - margen and
            a[2] <= b[2] + margen and a[3] <= b[3] + margen)


# ---------- 1. dimensiones ----------
if not (root.get('width') == '3840' and root.get('height') == '1080'):
    errors.append('dimensiones incorrectas')
else:
    notes.append('Dimensiones 3840 × 1080')

# ---------- 2. inventario ----------
texts = root.findall('.//s:text', ns)
rects = root.findall('.//s:rect', ns)
ellipses = root.findall('.//s:ellipse', ns)
circles = root.findall('.//s:circle', ns)

legend = next(r for r in rects if r.get('fill') == '#0b1420')
legend_box = caja_rect(legend)

legend_texts = [t for t in texts if dentro(caja_texto(t), legend_box, 12)]
legend_samples = [el for el in rects + ellipses + circles
                  if el is not legend and dentro(caja_de(el), legend_box, 6)]

fuera = lambda el: not dentro(caja_de(el), legend_box, 6)
map_circles = [c for c in circles if fuera(c)]
map_ellipses = [e for e in ellipses if fuera(e)]
map_collision = [r for r in rects if r.get('class') == 'collision' and fuera(r)]
map_walkbehind = [r for r in rects if r.get('class') == 'walkbehind' and fuera(r)]
furn_rects = [r for r in rects if r.get('class') == 'furniture']
furn_texts = [t for t in texts if fuera(t) and (t.text or '').strip()
              and not re.fullmatch(r'\d{2}', t.text or '')
              and not (t.text or '').startswith(
                  ('3840', 'ENCUADRE', 'BANDA', 'ALFOMBRA', 'ESQUEMA'))]

# ---------- 3. conteos ----------
hot_fijos = [c for c in map_circles if float(c.get('r')) >= 26]
if len(hot_fijos) != 15:
    errors.append(f'hotspots fijos: {len(hot_fijos)} != 15 (H15 contextual sin marcador)')
else:
    notes.append('15 hotspots fijos con marcador (H15 contextual: sin marcador)')

if len(map_ellipses) != 16:
    errors.append(f'zonas de aproximación: {len(map_ellipses)} != 16')
else:
    notes.append('16 zonas de aproximación')

if len(map_collision) != 8:
    errors.append(f'colisiones: {len(map_collision)} != 8')
else:
    notes.append('8 colisiones sólidas')

nums = sorted(t.text for t in texts if re.fullmatch(r'\d{2}', t.text or ''))
esperados = sorted(f'{i:02d}' for i in range(1, 17) if i != 15)
if nums != esperados:
    errors.append(f'numeración presente {nums} != esperada {esperados}')
else:
    notes.append('Numeración H01–H14 y H16 (H15 sin marcador, contextual)')

# ---------- 4. H15 contextual documentado ----------
src = open(SVG, encoding='utf-8').read()
if 'H15' not in src or 'CONTEXTUAL' not in src:
    errors.append('H15 contextual no está documentado en la leyenda')
else:
    notes.append('H15 documentado como hotspot contextual en la leyenda')
if re.search(r'>15<', src):
    errors.append('quedó un marcador numerado 15 en el mapa')
else:
    notes.append('Sin marcador fijo para H15')

# ---------- 5. leyenda libre de colisiones visuales ----------
ocupantes = ([(caja_de(r), f'mueble x={r.get("x")}') for r in furn_rects]
             + [(caja_de(r), 'colisión') for r in map_collision]
             + [(caja_de(c), 'hotspot') for c in map_circles]
             + [(caja_de(e), 'aproximación') for e in map_ellipses]
             + [(caja_de(r), 'walk-behind') for r in map_walkbehind]
             + [(caja_texto(t), 'rótulo "' + (t.text or '')[:20] + '"')
                for t in furn_texts])
for box, que in ocupantes:
    if intersecan(legend_box, box, margen=6):
        errors.append(f'LEYENDA {legend_box} interseca {que} {box}')

# ---------- 6. hotspots no tapan rótulos ----------
for c in map_circles:
    cb = caja_circ(c)
    for t in furn_texts:
        if intersecan(cb, caja_texto(t), margen=4):
            errors.append(f'hotspot {cb} interseca rótulo "{(t.text or "")[:24]}"')

# ---------- 7. rótulos entre sí ----------
permitidos = {('MESA BAJA', '(WALK-BEHIND)')}  # rótulo en dos líneas, mismo elemento
for i, a in enumerate(furn_texts):
    for b in furn_texts[i + 1:]:
        par = {(a.text or '').strip(), (b.text or '').strip()}
        if par in permitidos:
            continue
        if intersecan(caja_texto(a), caja_texto(b), margen=2):
            errors.append(f'rótulos solapados: "{(a.text or "")[:22]}" × "{(b.text or "")[:22]}"')

# ---------- 8. marcadores dentro del lienzo ----------
for c in map_circles:
    b = caja_circ(c)
    if not (0 <= b[0] and b[2] <= 3840 and 0 <= b[1] and b[3] <= 1080):
        errors.append(f'hotspot fuera de lienzo: {b}')

# ---------- 9. coordenadas clave del plano ----------
claves = [
    ('archivadores', 'x="60" y="330" width="260" height="495"'),
    ('escritorio', 'x="380" y="490" width="600" height="335"'),
    ('silla', 'x="520" y="690" width="180" height="190"'),
    ('rack', 'x="1080" y="500" width="480" height="325"'),
    ('radio', 'x="1150" y="420" width="240" height="170"'),
    ('grabadora', 'x="1360" y="610" width="200" height="180"'),
    ('biblioteca', 'x="1620" y="300" width="560" height="490"'),
    ('cajonera', 'x="2320" y="520" width="330" height="305"'),
    ('reloj', 'x="2390" y="170" width="160" height="160"'),
    ('cama', 'x="2800" y="500" width="680" height="350"'),
    ('mesa baja', 'x="2980" y="880" width="320" height="110"'),
    ('armario', 'x="3540" y="330" width="260" height="520"'),
    ('alfombra', 'x="1500" y="880" width="900" height="155"'),
]
mal = [n for n, f in claves if f not in src]
if mal:
    errors.append(f'coordenadas no transcritas: {mal}')
else:
    notes.append(f'{len(claves)} coordenadas de mobiliario transcritas fielmente')

# ---------- 10. encuadres ----------
cams = [r for r in rects if r.get('class') == 'camera']
xs = sorted(float(r.get('x')) for r in cams)
if xs != [0.0, 1920.0]:
    errors.append(f'encuadres: {xs}')
else:
    notes.append('Encuadres de cámara en X=0 y X=1920')

# ---------- informe ----------
print('=' * 68)
print('VERIFICACIÓN SVG v2 (estructura + solapes visuales) — Habitación WNL')
print('=' * 68)
for n in notes:
    print(' ✓', n)
if errors:
    print()
    for e in errors:
        print(' ✗', e)
    raise SystemExit(1)
print('-' * 68)
print('RESULTADO: SVG v2 VERIFICADO — estructura y separación visual OK')
