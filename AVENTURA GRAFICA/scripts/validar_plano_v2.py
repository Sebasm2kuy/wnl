#!/usr/bin/env python3
"""Validación programática del plano de distribución v2 de la Habitación WNL.

Comprueba: cajas dentro del lienzo, solapes no intencionados, puntos de
aproxación fuera de colisiones y alcanzables (BFS), despeje vertical >=120 px
en la banda de circulación, frente de interacción >=150 px y encuadres.
"""
from collections import deque

W, H = 3840, 1080
CAM = 1920
GROUND = (760, 1079)
BAND = (850, 1015)

# ---- Datos v2 -------------------------------------------------------------
furniture = {
    'archivadores_izq': (60, 330, 320, 825),
    'escritorio':       (380, 490, 980, 825),
    'silla':            (520, 690, 700, 880),
    'rack':             (1080, 500, 1560, 825),
    'radio':            (1150, 420, 1390, 590),
    'grabadora':        (1360, 610, 1560, 790),
    'biblioteca':       (1620, 300, 2180, 790),
    'cajonera':         (2320, 520, 2650, 825),
    'reloj':            (2390, 170, 2550, 330),
    'cama':             (2800, 500, 3480, 850),
    'mesa_baja':        (2980, 880, 3300, 990),   # walk-behind, sin colisión
    'armario':          (3540, 330, 3800, 850),
    'alfombra':         (1500, 880, 2400, 1035),  # transitable, sin colisión
}

collisions = {
    'archivadores_izq': (60, 730, 320, 825),
    'escritorio':       (380, 730, 980, 825),
    'silla':            (540, 800, 680, 875),
    'rack':             (1080, 730, 1560, 825),
    'biblioteca':       (1620, 690, 2180, 790),
    'cajonera':         (2320, 730, 2650, 825),
    'cama':             (2800, 740, 3480, 850),
    'armario':          (3540, 730, 3800, 850),
}

approach = {
    'archivadores_izq': (190, 850),
    'escritorio':       (450, 850),
    'computadora':      (760, 850),
    'silla':            (610, 905),
    'rack':             (1180, 850),
    'radio':            (1320, 850),
    'grabadora':        (1460, 850),
    'documentos':       (1120, 890),
    'biblioteca':       (1740, 850),
    'libros':           (2020, 850),
    'cajonera':         (2430, 850),
    'reloj':            (2540, 875),
    'cama':             (2890, 880),
    'mesa_baja':        (3140, 1000),
    'armario':          (3660, 870),
    'objetos_personales': (870, 850),
}

hotspots = {
    'H01 computadora':   (600, 475, 830, 670),
    'H02 escritorio':    (380, 650, 980, 825),
    'H03 silla':         (490, 680, 730, 890),
    'H04 biblioteca':    (1620, 300, 2180, 790),
    'H05 libros':        (1700, 390, 2100, 690),
    'H06 rack':          (1080, 500, 1560, 825),
    'H07 radio':         (1150, 420, 1390, 590),
    'H08 grabadora':     (1360, 610, 1560, 790),
    'H09 cajonera':      (2320, 520, 2650, 825),
    'H10 documentos':    (1080, 600, 1350, 820),
    'H11 cama':          (2800, 500, 3480, 850),
    'H12 reloj':         (2390, 170, 2550, 330),
    'H13 armario':       (3540, 330, 3800, 850),
    'H14 mesa_baja':     (2980, 880, 3300, 990),
    'H16 archiv_izq':    (60, 330, 320, 825),
    # H15 objetos personales: sin caja fija (sobre superficies)
}

# Solapes intencionados (mueble montado sobre otro / silla bajo escritorio)
ok_furn_overlaps = {frozenset(p) for p in [
    ('radio', 'rack'), ('grabadora', 'rack'), ('silla', 'escritorio')]}

ok_hot_overlaps = {frozenset(p) for p in [
    ('H01 computadora', 'H02 escritorio'),
    ('H02 escritorio', 'H03 silla'),
    ('H04 biblioteca', 'H05 libros'),
    ('H06 rack', 'H07 radio'),
    ('H06 rack', 'H08 grabadora'),
    ('H06 rack', 'H10 documentos')]}

errors, notes = [], []

def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

# ---- 1. Cajas dentro del lienzo -------------------------------------------
for name, box in {**furniture, **hotspots, **{f'col_{k}': v for k, v in collisions.items()}}.items():
    if not (0 <= box[0] < box[2] <= W and 0 <= box[1] < box[3] <= H):
        errors.append(f'FUERA DE LIENZO: {name} {box}')

# ---- 2. Solapes de mobiliario ---------------------------------------------
for i, a in enumerate(furniture):
    for b in list(furniture)[i+1:]:
        if overlap(furniture[a], furniture[b]) and frozenset((a, b)) not in ok_furn_overlaps:
            errors.append(f'SOLAPE NO INTENCIONADO: {a} × {b}')

# ---- 3. Hotspots: solapes y dentro de lienzo ya cubierto ------------------
hot_items = list(hotspots.items())
for i, (a, ba) in enumerate(hot_items):
    for b, bb in hot_items[i+1:]:
        if overlap(ba, bb) and frozenset((a, b)) not in ok_hot_overlaps:
            errors.append(f'SOLAPE DE HOTSPOT NO PREVISTO: {a} × {b}')

# ---- 4. Puntos de aproximación fuera de colisiones y en suelo -------------
for name, (x, y) in approach.items():
    if not (GROUND[0] <= y <= GROUND[1] and 0 <= x < W):
        errors.append(f'PUNTO FUERA DE SUELO: {name} ({x},{y})')
    for cname, c in collisions.items():
        if c[0] <= x <= c[2] and c[1] <= y <= c[3]:
            errors.append(f'PUNTO DENTRO DE COLISIÓN: {name} ({x},{y}) en {cname}')

# ---- 5. BFS sobre suelo transitable ---------------------------------------
STEP = 8
gx, gy = W // STEP, (GROUND[1] + 1 - GROUND[0]) // STEP + 1

def blocked(cx, cy):
    x, y = cx * STEP, GROUND[0] + cy * STEP
    for c in collisions.values():
        if c[0] <= x <= c[2] and c[1] <= y <= c[3]:
            return True
    return False

walk = [[not blocked(cx, cy) for cy in range(gy)] for cx in range(gx)]

def cell(x, y):
    return x // STEP, (y - GROUND[0]) // STEP

start = cell(30, 950)
seen = [[False] * gy for _ in range(gx)]
dq = deque([start])
seen[start[0]][start[1]] = True
while dq:
    cx, cy = dq.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < gx and 0 <= ny < gy and walk[nx][ny] and not seen[nx][ny]:
            seen[nx][ny] = True
            dq.append((nx, ny))

for name, (x, y) in approach.items():
    cx, cy = cell(x, y)
    if not seen[cx][cy]:
        errors.append(f'PUNTO INALCANZABLE (BFS): {name} ({x},{y})')
end = cell(3810, 950)
if not seen[end[0]][end[1]]:
    errors.append('EXTREMO DERECHO INALCANZABLE (BFS)')

# ---- 6. Despeje vertical en la banda (>=120 px) ---------------------------
intruders = {n: c for n, c in collisions.items() if c[3] > BAND[0]}
for name, c in intruders.items():
    free = BAND[1] - c[3]
    status = 'OK' if free >= 120 else 'FALLO'
    (notes if free >= 120 else errors).append(
        f'Banda — {name} intruye hasta Y={c[3]}: libre {free}px [{status}]')
notes.append(f'Banda — muebles sin intrusión en banda: '
             f'{len(collisions) - len(intruders)}/{len(collisions)} '
             f'(libre {BAND[1]-BAND[0]}px = {BAND[1]-BAND[0]}px)')

# ---- 7. Frente de interacción >=150 px hasta borde inferior ---------------
for name, c in collisions.items():
    free = GROUND[1] - c[3]
    if free < 150:
        errors.append(f'FRENTE <150px: {name} ({free}px)')
notes.append(f'Frente de interacción: {min(GROUND[1]-c[3] for c in collisions.values())}'
             f'–{max(GROUND[1]-c[3] for c in collisions.values())}px libres (todos >=150)')

# ---- 8. Encuadres ----------------------------------------------------------
e1_full = ['archivadores_izq', 'escritorio', 'silla', 'rack', 'radio', 'grabadora']
e2_full = ['cajonera', 'reloj', 'cama', 'mesa_baja', 'armario']
for n in e1_full:
    if furniture[n][2] > CAM:
        errors.append(f'ENCUADRE 1: {n} no cabe completo')
for n in e2_full:
    if furniture[n][0] < CAM:
        errors.append(f'ENCUADRE 2: {n} no empieza tras la costura')
lib = furniture['biblioteca']
notes.append(f'Encuadre 1 — grupo de trabajo/equipos completo (X máx {max(furniture[n][2] for n in e1_full)} < 1920)')
notes.append(f'Encuadre 2 — descanso completo (X mín {min(furniture[n][0] for n in e2_full)} > 1920)')
notes.append(f'Biblioteca cruza la costura: {lib[0]}–{lib[2]} '
             f'({CAM-lib[0]}px en encuadre 1, {lib[2]-CAM}px en encuadre 2)')

# ---- Informe ---------------------------------------------------------------
print('=' * 72)
print('VALIDACIÓN PLANO v2 — HABITACIÓN WNL (3840 × 1080)')
print('=' * 72)
print(f'Mobiliario: {len(furniture)} piezas · Colisiones: {len(collisions)} · '
      f'Hotspots con caja: {len(hotspots)} (H15 sin caja fija) · '
      f'Puntos de aproximación: {len(approach)}')
print('-' * 72)
for n in notes:
    print('  ✓', n)
print('-' * 72)
if errors:
    print(f'ERRORES ({len(errors)}):')
    for e in errors:
        print('  ✗', e)
    raise SystemExit(1)
print('RESULTADO: TODO OK — plano v2 válido para presentación')
print()
print('ALCANCE DE ESTA VALIDACIÓN (aclaración tras revisión QA):')
print('- El BFS verifica la alcanzabilidad de PUNTOS sobre una cuadrícula de')
print('  8 px con las colisiones rectangulares declaradas.')
print('- No modela el ancho/profundidad del personaje, ni la oclusión por')
print('  walk-behinds, ni la cámara. No sustituye una prueba funcional en Godot.')
print('- La mesa baja (walk-behind sin colisión) es transitable para este BFS;')
print('  su comportamiento real de oclusión y navegación queda pendiente del')
print('  Art Test con sprite provisional (registrado en REVISION_QA §5).')
