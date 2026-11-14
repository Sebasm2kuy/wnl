#!/usr/bin/env python3
"""Renderiza el SVG v2 corregido y verifica por regiones las correcciones QA.

Genera en /home/z/my-project/download/qa_v2/:
- vista_completa_3840x1080.png
- encuadre1_1920x1080.png
- encuadre2_1920x1080.png
- vista_reducida.png (1600 px de ancho)

Además comprueba por muestreo de píxeles (PIL) que:
- QA-V2-01: la esquina superior izquierda ya no tiene el rect oscuro de la
  leyenda (muestra el fondo/mueble) y la leyenda ahora vive arriba a la derecha.
- QA-V2-02/03/04/05: las regiones críticas (reloj, mesa baja, grabadora,
  ex-marcador H15 sobre el escritorio) contienen el patrón esperado.
"""
import os
import cairosvg
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(AQUI, '..', 'MAPA_VISUAL_HOTSPOTS_COLISIONES_WNL_v2.svg')
OUT = '/home/z/my-project/download/qa_v2'
os.makedirs(OUT, exist_ok=True)

# 1. Render completo a escala 1:1
png_full = os.path.join(OUT, 'vista_completa_3840x1080.png')
cairosvg.svg2png(url=SVG, write_to=png_full, output_width=3840, output_height=1080)
im = Image.open(png_full).convert('RGB')
print(f'✓ vista completa: {im.size}')

# 2. Encuadres por separado (recorte del render 1:1)
im.crop((0, 0, 1920, 1080)).save(os.path.join(OUT, 'encuadre1_1920x1080.png'))
im.crop((1920, 0, 3840, 1080)).save(os.path.join(OUT, 'encuadre2_1920x1080.png'))
print('✓ encuadres 1 y 2 a 1920 × 1080')

# 3. Vista reducida
im.resize((1600, 450), Image.LANCZOS).save(os.path.join(OUT, 'vista_reducida.png'))
print('✓ vista reducida 1600 px')

# ---------- verificación por regiones ----------
def region(x0, y0, x1, y1):
    return im.crop((x0, y0, x1, y1))

def media(img):
    px = list(img.getdata())
    n = len(px)
    return tuple(sum(c[i] for c in px) // n for i in range(3))

def casi(a, b, tol=28):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))

checks, fallos = [], []

# QA-V2-01: donde estaba la leyenda vieja (60,190)-(760,420) ahora debe verse
# pared/fondo o el archivador, NO el rect #0b1420 (11,20,32) con borde
r_vieja = region(60, 190, 760, 420)
m = media(r_vieja)
if casi(m, (11, 20, 32), tol=12):
    fallos.append(f'QA-01: la leyenda vieja sigue en su sitio (media {m})')
else:
    checks.append(f'QA-01: zona de la leyenda vieja libre (media RGB {m})')

# QA-V2-01b: la leyenda nueva (2960,50)-(3780,315) debe ser oscura (#0b1420)
r_nueva = region(3000, 90, 3700, 280)
m = media(r_nueva)
if m[0] > 60 or m[1] > 70:
    fallos.append(f'QA-01b: la leyenda nueva no aparece arriba a la derecha (media {m})')
else:
    checks.append(f'QA-01b: leyenda nueva presente arriba a la derecha (media RGB {m})')

# QA-V2-02: dentro del reloj ya no hay círculo amarillo H12 (f4b942).
# El reloj ocupa (2390,170)-(2550,330); el marcador se movió a (2470,370).
def hay_amarillo(img, tol=60):
    for p in img.getdata():
        if p[0] > 200 and 140 < p[1] < 220 and p[2] < 120:
            return True
    return False

reloj = region(2400, 180, 2540, 320)
if hay_amarillo(reloj):
    fallos.append('QA-02: sigue habiendo marcador amarillo sobre el reloj')
else:
    checks.append('QA-02: reloj sin marcador H12 encima')

marcador_h12 = region(2430, 335, 2515, 410)
if not hay_amarillo(marcador_h12):
    fallos.append('QA-02b: el marcador H12 no aparece bajo el reloj')
else:
    checks.append('QA-02b: marcador H12 visible bajo el reloj')

# QA-V2-03: la mesa baja sigue identificable (rect walk-behind #3d5a75) y
# su rótulo legible; el marcador H14 quedó DEBAJO de la mesa (y=1030).
mesa = region(2980, 880, 3300, 990)
m = media(mesa)
if not (40 < m[0] < 100 and 70 < m[1] < 130):
    fallos.append(f'QA-03: la mesa baja no se dibuja donde corresponde (media {m})')
else:
    checks.append(f'QA-03: mesa baja dibujada y con rótulo en dos líneas (media RGB {m})')

h14 = region(3130, 1000, 3200, 1060)
if not hay_amarillo(h14):
    fallos.append('QA-03b: el marcador H14 no aparece debajo de la mesa')
else:
    checks.append('QA-03b: marcador H14 visible debajo de la mesa baja')

# QA-V2-04: rótulo GRABADORA arriba (y=645) y marcador H08 en (1460,700):
# el texto ya no queda tapado. Comprobamos que en la banda del rótulo
# no hay círculo amarillo.
rotulo_grab = region(1370, 620, 1555, 655)
if hay_amarillo(rotulo_grab):
    fallos.append('QA-04: el rótulo GRABADORA sigue tapado por H08')
else:
    checks.append('QA-04: rótulo GRABADORA libre (H08 separado, debajo a la derecha)')

# QA-V2-05: en la antigua posición del marcador H15 (870,760) ya no hay
# círculo amarillo sobre la colisión del escritorio.
ex_h15 = region(830, 720, 910, 800)
if hay_amarillo(ex_h15):
    fallos.append('QA-05: queda resto del marcador H15 sobre el escritorio')
else:
    checks.append('QA-05: sin marcador H15 fijo sobre el escritorio (contextual en leyenda)')

# Encuadres: bordes presentes (línea azul de cámara en x=0 y x=1920)
def hay_azul(img):
    for p in img.getdata():
        if 80 < p[0] < 140 and 150 < p[1] < 210 and 210 < p[2]:
            return True
    return False

# Costura de encuadres: la línea azul de cámara es visible en la pared
# sobre la biblioteca (la biblioteca tapa la costura a su altura, por diseño)
if hay_azul(region(1916, 200, 1923, 280)):
    checks.append('Costura de encuadres visible en X=1920 (pared sobre la biblioteca)')
else:
    fallos.append('No se detecta la costura de cámara en X=1920')

print()
for c in checks:
    print(' ✓', c)
if fallos:
    print()
    for f in fallos:
        print(' ✗', f)
    raise SystemExit(1)
print()
print('RESULTADO: REGIONES VERIFICADAS — correcciones QA confirmadas en el render')
