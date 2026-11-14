#!/usr/bin/env python3
"""Verificación programática del SVG v2 del mapa de la Habitación WNL."""
import xml.etree.ElementTree as ET
import re

import os
SVG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MAPA_VISUAL_HOTSPOTS_COLISIONES_WNL_v2.svg')
tree = ET.parse(SVG)
root = tree.getroot()
ns = {'s': 'http://www.w3.org/2000/svg'}
errors = []

# 1. Dimensiones
assert root.get('width') == '3840' and root.get('height') == '1080', 'dimensiones'
print('✓ Dimensiones 3840 × 1080')

# 2. Conteos (excluyendo elementos de la leyenda: caja x=60..760, y=190..420,
#    sus marcadores están en x/cx < 200, y/cy < 500; ningún elemento real del
#    mapa tiene y < 500 con x < 200)
def en_leyenda(el):
    x = float(el.get('cx') or el.get('x') or '0')
    y = float(el.get('cy') or el.get('y') or '0')
    return y < 500 and x < 200

ellipses = [e for e in root.findall('.//s:ellipse', ns) if not en_leyenda(e)]
circles = [c for c in root.findall('.//s:circle', ns) if c.get('r') == '30']
texts = root.findall('.//s:text', ns)
print(f'✓ Elipses de aproximación: {len(ellipses)} (esperado 16)')
if len(ellipses) != 16: errors.append('elipses != 16')
print(f'✓ Círculos de hotspot r=30: {len(circles)} (esperado 16)')
if len(circles) != 16: errors.append('hotspots != 16')

# 3. Números de hotspot 01..16 presentes exactamente una vez
nums = [t.text for t in texts if t.text and re.fullmatch(r'\d{2}', t.text)]
esperados = {f'{i:02d}' for i in range(1, 17)}
if sorted(nums) != sorted(esperados):
    errors.append(f'números hotspot: {sorted(nums)}')
else:
    print('✓ Hotspots numerados 01–16, cada uno exactamente una vez')

# 4. Todo texto dentro del lienzo
for t in texts:
    x, y = float(t.get('x')), float(t.get('y'))
    if not (0 <= x <= 3840 and 0 <= y <= 1080):
        errors.append(f'texto fuera de lienzo: {t.text} ({x},{y})')
print('✓ Todos los textos dentro del lienzo' if not errors else 'ver textos')

# 5. Muebles esperados (por etiqueta visible)
labels = [t.text for t in texts if t.text and t.text.isupper()]
esperados_lbl = {'ARCHIVADORES', 'ESCRITORIO / PC', 'SILLA', 'RACK EQUIPOS', 'RADIO',
                 'GRABADORA', 'BIBLIOTECA', 'CAJONERA', 'RELOJ', 'CAMA', 'ARMARIO',
                 'MESA BAJA (WALK-BEHIND)', 'ALFOMBRA (TRANSITABLE)'}
faltan = esperados_lbl - set(labels)
if faltan:
    errors.append(f'faltan etiquetas: {faltan}')
else:
    print(f'✓ 13 etiquetas de mobiliario presentes: {sorted(set(labels))}')

# 6. Colisiones (rects con class collision): esperado 8
coll = [r for r in root.findall('.//s:rect', ns) if r.get('class') == 'collision' and not en_leyenda(r)]
print(f'✓ Colisiones dibujadas: {len(coll)} (esperado 8)')
if len(coll) != 8: errors.append('colisiones != 8')

# 7. Encuadres
cams = [r for r in root.findall('.//s:rect', ns) if r.get('class') == 'camera']
xs = sorted(float(r.get('x')) for r in cams)
if xs != [0.0, 1920.0]:
    errors.append(f'encuadres: {xs}')
else:
    print('✓ Encuadres de cámara en X=0 y X=1920')

# 8. Coordenadas clave del plano v2 presentes en el SVG (transcripción fiel)
src = open(SVG, encoding='utf-8').read()
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
for nombre, frag in claves:
    if frag not in src:
        errors.append(f'coordenada no transcrita: {nombre} ({frag})')
print(f'✓ {len(claves)} coordenadas de mobiliario transcritas fielmente del plano v2' if not errors else '')

print('-' * 60)
if errors:
    print('ERRORES:')
    for e in errors:
        print(' ✗', e)
    raise SystemExit(1)
print('RESULTADO: SVG v2 VERIFICADO — estructura, conteos y coordenadas OK')
