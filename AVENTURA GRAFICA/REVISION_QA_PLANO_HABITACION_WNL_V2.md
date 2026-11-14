# Revisión de QA — Plano y mapa visual de la Habitación WNL · v2

**Fecha:** 2026-11-14  
**Proyecto:** Aventura gráfica WNL  
**Base revisada:** `PLANO_DISTRIBUCION_HABITACION_WNL_v2.md`, `MAPA_VISUAL_HOTSPOTS_COLISIONES_WNL_v2.svg`, `scripts/validar_plano_v2.py` y `scripts/verificar_svg_v2.py`.  
**Estado:** observaciones de revisión; la v2 continúa como **PROPUESTA PENDIENTE DE APROBACIÓN**.  
**Alcance:** revisión de coherencia documental, estructura SVG y lectura del SVG renderizado. No se ha modificado el plano v2 ni el SVG.

---

## 1. Resultado general

La v2 corrige la discrepancia estructural principal de la v1: los archivadores izquierdos, escritorio/PC, rack analógico con radio y grabadora, biblioteca central, cajonera y reloj, cama con mesa baja y armario aparecen en el orden correcto.

Se conserva la biblioteca como elemento que cruza la costura entre los dos encuadres de 1920 × 1080. El SVG representa 16 hotspots, 16 zonas de aproximación, ocho colisiones sólidas y la mesa baja como elemento walk-behind.

La propuesta es una base de trabajo más coherente, pero la revisión del render detectó defectos de legibilidad y puntos que requieren validación dentro del motor antes de dar el plano por aprobado.

## 2. Defectos visuales observados en el SVG renderizado

### QA-V2-01 — La leyenda tapa el archivador izquierdo

La leyenda ocupa aproximadamente X = 60–760, Y = 190–420. Se superpone al archivador izquierdo, cuya caja empieza en X = 60, Y = 330. En el render, la leyenda oculta parte del mueble y tapa el rótulo «ARCHIVADORES».

**Corrección propuesta:** mover la leyenda a una zona libre de pared, por ejemplo a la parte superior derecha, comprobando que no tape el reloj, la cama ni otros elementos. No cambiar las coordenadas del mobiliario para resolver una superposición meramente gráfica.

### QA-V2-02 — El marcador H12 tapa el rótulo del reloj

El marcador circular H12 está centrado sobre el texto «RELOJ» dentro del dibujo del reloj. El marcador oculta parte del propio rótulo.

**Corrección propuesta:** separar el texto del marcador o desplazar el marcador a una zona del reloj que no tape su nombre ni su representación.

### QA-V2-03 — El marcador H14 tapa el rótulo de la mesa baja

El marcador H14 queda sobre el texto «MESA BAJA (WALK-BEHIND)».

**Corrección propuesta:** recolocar el texto y/o el marcador, conservando la identificación inequívoca del objeto y el hotspot.

### QA-V2-04 — H08 demasiado cerca del rótulo de la grabadora

El marcador H08 se solapa visualmente con el rótulo «GRABADORA» o queda demasiado pegado a él.

**Corrección propuesta:** separar el rótulo y el marcador para que ambos sean legibles al reducir el SVG a una vista de revisión.

### QA-V2-05 — H15 aparece sobre la franja de colisión del escritorio

El SVG sitúa H15 aproximadamente en (870, 760). La huella de colisión del escritorio se extiende desde Y = 730 hasta Y = 825. Por tanto, el marcador aparece sobre la zona roja de colisión, no claramente sobre una superficie con objetos personales.

El plano describe H15 como objetos personales distribuidos sobre escritorio, rack o estantes y sin una caja fija.

**Corrección propuesta:** no representar H15 como si fuera un único objeto en el suelo o dentro de la colisión del escritorio. Retirar el marcador genérico del SVG o ubicarlo sobre una superficie visible solo si se aclara que es un ejemplo representativo. La definición funcional debe seguir permitiendo hotspots independientes por objeto cuando el arte final lo requiera.

## 3. Errores editoriales del documento v2

### QA-V2-06 — Coordenada errónea en el anexo de colisiones

En la fila de la biblioteca del anexo final aparece:

`1620, 6690 → 2180, 790`

El valor coherente con la implantación principal, la huella de colisión y el SVG es:

`1620, 690 → 2180, 790`

La cifra 6690 es un error tipográfico manifiesto. Corregirla sin alterar el diseño.

### QA-V2-07 — Fila Markdown que une silla y rack

En el anexo de colisiones, la fila de la silla y la del rack quedaron concatenadas en una sola línea de tabla (aparece `|| Rack...` dentro de la fila de Silla). Separarlas en dos filas independientes para que los datos puedan leerse y compararse correctamente.

## 4. Límites de lo que demuestran los scripts actuales

### `validar_plano_v2.py`

El script comprueba:
- Que las cajas descritas se mantengan dentro del lienzo.
- Solapes de cajas de mobiliario y hotspots, aplicando excepciones explícitas.
- Que los puntos de aproximación no caigan dentro de las colisiones definidas.
- Alcanzabilidad de los puntos mediante BFS sobre una cuadrícula de 8 px en la franja de suelo.
- Despeje vertical y encuadres.

La comprobación BFS utiliza el punto de apoyo del personaje como punto de prueba y las colisiones rectangulares declaradas. **No dilata los obstáculos según el ancho/profundidad de un personaje real**, no modela su cápsula o forma de colisión, y no comprueba animaciones, navegación táctil, oclusión por walk-behinds ni el comportamiento de la cámara en Godot.

Por tanto, «TODO OK» significa que las comprobaciones geométricas codificadas pasan; no equivale a una prueba funcional dentro del motor.

### `verificar_svg_v2.py`

El script comprueba dimensiones, recuentos de elipses y círculos, numeración de hotspots, coordenadas de texto dentro del lienzo, presencia de etiquetas, cantidad de colisiones y correspondencia de algunas coordenadas clave.

No calcula intersecciones entre cajas de texto, marcadores, leyenda y mobiliario, ni verifica visualmente el orden de dibujo. Por eso puede pasar aunque el render muestre los defectos QA-V2-01 a QA-V2-05.

**Recomendación:** mantener las validaciones actuales y añadir comprobaciones de colisiones de etiquetas/leyenda o una revisión visual rasterizada como parte del QA.

## 5. Punto de diseño pendiente: mesa baja y walk-behind

La mesa baja se declara walk-behind y sin colisión. El plano coloca el punto de aproximación H14 en (3140, 1000), mientras la caja gráfica de la mesa ocupa X = 2980–3300, Y = 880–990.

Hay que precisar el comportamiento esperado:
- El personaje debe poder pasar por detrás de la mesa sin que esta bloquee indebidamente la circulación.
- El personaje no debería parecer que atraviesa el tablero o caminar sobre la mesa.
- La máscara de oclusión debe actuar según la profundidad del personaje, no cubrirlo indiscriminadamente en cualquier posición.
- Debe comprobarse cómo se llega al punto de interacción H14 y cómo se accede a la cama desde el lateral izquierdo de la mesa.

No asumir que «walk-behind» implica «sin ninguna colisión» en el montaje final. Oclusión visual, colisión física y navegación son sistemas distintos. La solución debe comprobarse con un sprite provisional y geometría de bloqueo en Godot antes de congelar el arte.

## 6. Qué no cambia

Esta revisión no modifica:
- La secuencia espacial general de la v2.
- Las coordenadas de mobiliario de la implantación principal.
- Los identificadores H01–H16.
- La existencia de ocho colisiones sólidas declaradas.
- La idea de biblioteca cruzando la costura de cámara.
- La condición de la Habitación como espacio completamente funcional desde el inicio.
- Las restricciones narrativas de la Habitación.

No se aprueba todavía la distribución ni se inicia la producción del escenario final.

## 7. Próximo paso recomendado

Preparar una iteración de corrección **solo de QA visual/editorial**, sin modificar la distribución principal:

1. Reubicar la leyenda.
2. Separar H08, H12 y H14 de sus rótulos.
3. Resolver la representación genérica de H15.
4. Corregir la coordenada de biblioteca y separar las filas del anexo.
5. Regenerar el SVG y revisar el render completo en los dos encuadres.
6. Probar mesa baja, aproximación a cama y movimiento del personaje con un sprite provisional en Godot cuando exista un Art Test.

Después de esa pasada, presentar de nuevo la v2 al autor para aprobación. Hasta entonces, conservar la v1 y la v2 como propuestas comparables.

---

**Conclusión:** la v2 resuelve la organización espacial principal, pero todavía necesita una pasada final de legibilidad, limpieza documental y validación de walk-behind. Esta revisión no sustituye la aprobación del autor.

---

## 8. Iteración de corrección QA (2026-11-14, segunda pasada)

Sobre la base de los hallazgos anteriores se ejecutó la pasada de corrección **sin modificar la distribución espacial**: secuencia, coordenadas de mobiliario, encuadres, 8 colisiones, H01–H16, alfombra y mesa baja walk-behind permanecen intactos.

### Resultado por hallazgo

| Hallazgo | Estado | Detalle de la corrección |
|---|---|---|
| QA-V2-01 · Leyenda sobre el archivador | **Corregido** | Leyenda trasladada a la esquina superior derecha (X 2960–3780, Y 50–315), zona de pared libre verificada programáticamente: no interseca reloj (X ≤ 2550), cama (Y ≥ 500), armario (X ≥ 3540 con Y ≥ 330; margen de 15 px) ni ningún mueble, colisión, hotspot, zona de aproximación o rótulo. El archivador izquierdo y su rótulo quedan visibles. |
| QA-V2-02 · H12 sobre «RELOJ» | **Corregido** | Marcador H12 reubicado debajo del reloj, centrado en (2470, 370), fuera del círculo del mueble (Y 170–330). Rótulo «RELOJ» intacto dentro del mueble. Verificado en render: sin amarillo sobre el reloj, marcador visible debajo. |
| QA-V2-03 · H14 sobre «MESA BAJA» | **Corregido** | Rótulo dividido en dos líneas («MESA BAJA» / «(WALK-BEHIND)», Y 922/968) dentro de la mesa; marcador H14 movido debajo de la mesa, centro (3165, 1030), radio 26. Ubicación de la mesa sin cambios. Verificado en render. |
| QA-V2-04 · H08 sobre «GRABADORA» | **Corregido** | Rótulo «GRABADORA» subido a Y 645 (parte alta del mueble); marcador H08 se mantiene a la derecha-abajo (1460, 700). Ambos legibles; verificado en render y por cajas estimadas. |
| QA-V2-05 · H15 como marcador fijo | **Corregido** | Marcador fijo retirado del SVG. H15 se documenta como **hotspot contextual** en la leyenda («sin marcador fijo, hotspot por objeto») y en el plano v2 (sección 6 y nota en sección 4). La numeración H01–H16 se conserva: 15 marcadores fijos + H15 contextual. `verificar_svg_v2.py` adaptado para distinguir fijos de contextuales. |
| QA-V2-06 · Coordenada 6690 | **Corregido** | `1620, 6690 → 2180, 790` → `1620, 690 → 2180, 790` en el anexo de colisiones. Coherencia verificada contra implantación, sección 5 y SVG (`y="690"`). Sin otras apariciones de 6690. |
| QA-V2-07 · Filas silla/rack concatenadas | **Corregido** | Separadas en dos filas Markdown independientes con sus datos originales. Chequeo automático de integridad de tablas: todas las filas cierran con pipe y el número de columnas es consistente en todo el documento. |
| §5 · Mesa baja / walk-behind | **Documentado; prueba en Godot PENDIENTE** | El plano v2 ahora distingue explícitamente colisión física / oclusión visual (dependiente de profundidad Y, `y-sort` o capa delantera) / navegación de aproximación, con criterio de decisión para el Art Test. El repositorio **no contiene proyecto Godot ni Art Test** de la Habitación: la prueba con sprite provisional no se realizó y no se declara validado el comportamiento. Registrado como pendiente. |

### Correcciones adicionales detectadas por el verificador extendido

Las nuevas comprobaciones de solapes del `verificar_svg_v2.py` detectaron y corrigieron dos casos del mismo tipo que los hallazgos QA, no reportados en la primera revisión:

- H03 se solapaba con el rótulo «SILLA» → marcador movido a (610, 722).
- H07 se solapaba con los rótulos «RADIO» y «RACK EQUIPOS» → marcador movido a (1310, 495).

Ambos son marcadores de hotspot; ningún mueble cambió de posición.

### Evidencia de validación

- `scripts/validar_plano_v2.py`: **TODO OK** (cajas en lienzo, solapes con excepciones declaradas, 16 puntos de aproximación fuera de colisiones y alcanzables por BFS, despeje de banda ≥ 120 px, frente de interacción ≥ 150 px, encuadres). Se añadió al informe impreso el **alcance real** de la validación (puntos en cuadrícula de 8 px; no modela huella del personaje, oclusión ni cámara).
- `scripts/verificar_svg_v2.py`: **VERIFICADO** (estructura + nuevas comprobaciones de solapes: leyenda vs. mobiliario/marcadores/rótulos, hotspots vs. rótulos, rótulos entre sí, marcadores en lienzo, H15 contextual documentado y sin marcador fijo, 13 coordenadas transcritas, encuadres).
- `scripts/render_y_verificar_v2.py` (nuevo): renderiza el SVG y verifica por muestreo de píxeles las regiones de las 5 correcciones visuales + costura de cámara. **9/9 comprobaciones en verde.** Genera `vista_completa_3840x1080.png`, `encuadre1_1920x1080.png`, `encuadre2_1920x1080.png` y `vista_reducida.png`.

### Archivos modificados en esta iteración

- `AVENTURA GRAFICA/PLANO_DISTRIBUCION_HABITACION_WNL_v2.md` — QA-V2-06, QA-V2-07, nota de H15 en secciones 4 y 6, sección «Mesa baja: los tres sistemas en juego» con pendiente de Godot.
- `AVENTURA GRAFICA/MAPA_VISUAL_HOTSPOTS_COLISIONES_WNL_v2.svg` — QA-V2-01 a QA-V2-05 + H03/H07.
- `AVENTURA GRAFICA/scripts/validar_plano_v2.py` — nota de alcance de la validación.
- `AVENTURA GRAFICA/scripts/verificar_svg_v2.py` — reescrito: hotspots fijos vs. contextual + solapes.
- `AVENTURA GRAFICA/scripts/render_y_verificar_v2.py` — nuevo.
- `AVENTURA GRAFICA/REVISION_QA_PLANO_HABITACION_WNL_V2.md` — esta sección.
- `AVENTURA GRAFICA/INSTRUCCIONES_PARA_Z_AI.md` e `HISTORIAL_CHAT/2026-11-14.md` — estado e historial.

### Estado tras la iteración

- **Corregidos:** QA-V2-01 a QA-V2-07.
- **Pendiente de prueba en Godot:** comportamiento real de la mesa baja (oclusión por profundidad, acceso lateral a la cama, consecución de H14) y navegación con sprite provisional — requiere un Art Test que todavía no existe en el repositorio.
- **No corregido (por diseño):** ninguno de los defectos listados queda sin resolver.
- La v2 **continúa siendo PROPUESTA PENDIENTE DE APROBACIÓN DEL AUTOR**. Con las correcciones publicadas, queda lista para la revisión de distribución del autor.
