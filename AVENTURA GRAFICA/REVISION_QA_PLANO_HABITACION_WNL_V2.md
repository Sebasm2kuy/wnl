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
