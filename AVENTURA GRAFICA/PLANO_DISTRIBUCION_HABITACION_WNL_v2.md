# WNL — Plano de distribución de la Habitación · v2

**Fecha:** 2026-11-14  
**Versión:** 2 (revisión espacial basada en la imagen conceptual)  
**Documento relacionado:** [MAPA_FUNCIONAL_HABITACION_WNL.md](MAPA_FUNCIONAL_HABITACION_WNL.md) · [REVISION_VISUAL_IMAGEN_CONCEPTUAL_HABITACION_WNL.md](REVISION_VISUAL_IMAGEN_CONCEPTUAL_HABITACION_WNL.md)  
**Estado:** PROPUESTA — pendiente de aprobación del autor. Esta versión no reemplaza silenciosamente a la v1; ambas coexisten para comparación.

Este plano aplica la secuencia visual confirmada por la revisión de la imagen conceptual (2048 × 768) sobre el lienzo de juego de 3840 × 1080. La corrección estructural principal respecto de la v1 es que **el grupo de equipos analógicos y la grabadora pasan a la izquierda de la biblioteca**, junto al escritorio, y no a su derecha. Las coordenadas siguen siendo de diseño: organizan arte, navegación y pruebas; no son medidas arquitectónicas narrativas ni píxeles definitivos de cada sprite.

---

## 1. Sistema de coordenadas (sin cambios respecto de v1)

- Lienzo completo: **3840 × 1080 px**.
- Origen `(0,0)`: esquina superior izquierda.
- Eje X: aumenta hacia la derecha.
- Eje Y: aumenta hacia abajo.
- Vista de cámara de referencia: **1920 × 1080 px**.
- Mitad izquierda: X = 0–1919. Mitad derecha: X = 1920–3839.
- Suelo visible de referencia: Y = 760–1079.
- Franja principal de circulación: Y = 850–1015.
- La altura exacta del suelo y la línea de horizonte se ajustarán al arte final, manteniendo la franja transitable continua.

Las cajas indican ocupación aproximada `[X1, Y1, X2, Y2]`. No son rectángulos literales: cada objeto tendrá su silueta artística y una colisión simplificada adaptada.

## 2. Cambios respecto de la v1

| # | Cambio | Motivo |
|---|---|---|
| 1 | Consola → **rack de equipos** en X 1080–1560 (izquierda de la biblioteca) | La revisión visual confirmó que los equipos están junto al escritorio, antes de la biblioteca (discrepancia 3.1) |
| 2 | Grabadora pasa a integrar el rack (X 1360–1560) | En la referencia forma parte del conjunto de equipos, no una pieza aislada tras la biblioteca (discrepancia 3.1) |
| 3 | Radio pasa a módulo superior del rack (X 1150–1390, Y 420–590) | Mismo conjunto de equipos; la v1 la flotaba sobre la consola en X 1810–2070 |
| 4 | **Archivadores altos del extremo izquierdo** (X 60–320) con hotspot H16 | Pieza visible en la referencia que la v1 omitía (discrepancia 3.2) |
| 5 | Biblioteca reubicada al centro exacto: X 1620–2180 | Centro visual de la habitación (discrepancia 3.3); ahora sí es el eje que divide los dos encuadres |
| 6 | **Cajonera derecha** (antes archivador, X 2320–2650) + **reloj sobre ella** (X 2390–2550, Y 170–330) | La referencia sitúa el reloj sobre la cajonera derecha, no sobre la cama (discrepancia 3.5) |
| 7 | Mesa baja delante de la cama, en primer plano (Y 880–990), **walk-behind sin colisión** | En la referencia está delante de la cama; bloquearla cortaría la circulación frontal (discrepancia 3.4) |
| 8 | **Alfombra principal** (X 1500–2400, Y 880–1035) como elemento visual transitable | Presente en la referencia, omitida en v1; no afecta navegación |
| 9 | Torre(s) PC y mueble de consulta de la v1 **no se mueven a esta versión** | Las torres son parte del puesto PC (sin hotspot propio); el mueble de consulta se sustituye por la superficie del rack |
| 10 | Silla con aproximación frontal independiente (610, 905) | Evita que la colisión de la silla tape el acceso a la mesa/escritorio |

## 3. Implantación general

La habitación sigue siendo un único ambiente continuo. Los sectores funcionales de la v1 se conservan como lectura, pero la secuencia espacial es ahora la de la imagen conceptual:

**archivadores → escritorio/PC → rack de equipos (radio + grabadora) → biblioteca → cajonera + reloj → cama + mesa baja → armario**

| Elemento | Caja aproximada (X1, Y1 → X2, Y2) | Ubicación |
|---|---:|---|
| Archivadores altos | 60, 330 → 320, 825 | Extremo izquierdo |
| Escritorio y puesto PC | 380, 490 → 980, 825 | Sector A, pared/fondo |
| Silla de PC | 520, 690 → 700, 880 | Frente al escritorio |
| Rack de equipos | 1080, 500 → 1560, 825 | Entre escritorio y biblioteca |
| Radio / comunicaciones | 1150, 420 → 1390, 590 | Módulo superior del rack |
| Grabadora / reproductor | 1360, 610 → 1560, 790 | Extremo derecho del rack |
| Biblioteca principal | 1620, 300 → 2180, 790 | Centro visual, cruza la costura de cámara |
| Cajonera derecha | 2320, 520 → 2650, 825 | Derecha de la biblioteca |
| Reloj | 2390, 170 → 2550, 330 | Pared, sobre la cajonera |
| Cama | 2800, 500 → 3480, 850 | Sector D, pared/fondo |
| Mesa baja | 2980, 880 → 3300, 990 | Delante de la cama, primer plano (walk-behind) |
| Armario / taquilla | 3540, 330 → 3800, 850 | Extremo derecho |
| Alfombra principal | 1500, 880 → 2400, 1035 | Primer plano central, transitable |
| Objetos personales | Sobre escritorio, rack y estantes (H15, sin caja fija) | Según composición |

**Lectura visual:** los archivadores del extremo izquierdo abren la composición con una masa alta que equilibra el armario del extremo derecho. El puesto informático y el rack de equipos forman un continuo de trabajo en la mitad izquierda; la biblioteca domina el centro como núcleo vertical; la cajonera con reloj hace de bisagra hacia la zona de descanso, que cierra la cama protegida por la mesa baja en primer plano. No se agrega ninguna puerta, ventana ni salida física.

## 4. Recorrido del personaje

### Ruta principal

- Banda de circulación: **Y = 850–1015** (franja continua de suelo por delante de los muebles).
- El personaje se desplaza en X a lo largo de todo el escenario.
- Se permite ajuste de profundidad en Y para acercarse a los objetos y rodear muebles bajos.
- Ningún mueble debe ocupar toda la profundidad de la banda de circulación.
- No forzar al personaje por huecos inferiores a unos 120 px de ancho útil.
- Mantener al menos 150 px de suelo libre frente a los frentes de interacción principales.
- La alfombra es transitable: no genera colisión, solo cambio visual de suelo.

### Puntos de aproximación (16)

Posiciones sugeridas donde el personaje se detiene antes de activar cada hotspot. El motor calcula el acercamiento desde la posición actual, evitando terminar dentro de una colisión.

| Interacción | Punto (X, Y) | Orientación |
|---|---:|---|
| Archivadores izq. | (190, 850) | Hacia los cajones |
| Escritorio | (450, 850) | Hacia la superficie |
| Computadora | (760, 850) | Hacia el monitor |
| Silla | (610, 905) | Hacia el asiento |
| Rack de equipos | (1180, 850) | Hacia controles y medidores |
| Radio | (1320, 850) | Hacia el módulo superior |
| Grabadora | (1460, 850) | Hacia el reproductor |
| Documentos | (1120, 890) | Hacia la superficie del rack |
| Biblioteca | (1740, 850) | Hacia estantes |
| Libros / consulta | (2020, 850) | Hacia los libros seleccionables |
| Cajonera | (2430, 850) | Hacia cajones |
| Reloj | (2540, 875) | Hacia la pared |
| Cama | (2890, 880) | Hacia la cama |
| Mesa baja | (3140, 1000) | Hacia la mesa |
| Armario | (3660, 870) | Hacia el armario |
| Objetos personales * | (870, 850) | Punto de referencia genérico, no ubicación de H15 |

Las coordenadas Y son puntos de suelo, no centros visuales de hotspots. La interacción se activa al llegar al punto de aproximación o al entrar en el área válida, según el sistema de control.

**\* Nota sobre el punto de objetos personales:** (870, 850) es solo un punto de aproximación de referencia junto al escritorio. No define la ubicación del hotspot H15: cada objeto personal tendrá su propio punto de aproximación según la superficie donde esté (escritorio, rack o estantes de la biblioteca). El SVG v2 no dibuja un marcador fijo para H15 por este motivo; su representación es una anotación contextual.

## 5. Colisiones y profundidad

### Colisiones sólidas (8)

Formas simples siguiendo el volumen de cada mueble, no el contorno de cada píxel:

| Mueble | Huella (X1, Y1 → X2, Y2) | Nota |
|---|---:|---|
| Archivadores izq. | 60, 730 → 320, 825 | Volumen inferior |
| Escritorio | 380, 730 → 980, 825 | Cuerpo y laterales; acceso a silla libre |
| Silla | 540, 800 → 680, 875 | Asiento/base; si el personaje se sienta, cambia a estado correspondiente |
| Rack de equipos | 1080, 730 → 1560, 825 | Cuerpo inferior; controles superiores son hotspots |
| Biblioteca | 1620, 690 → 2180, 790 | Base y laterales; estantes altos sin colisión adicional |
| Cajonera | 2320, 730 → 2650, 825 | Volumen inferior; acercamiento frontal |
| Cama | 2800, 740 → 3480, 850 | Estructura y colchón; no atravesable |
| Armario | 3540, 730 → 3800, 850 | Cuerpo; acercamiento frontal |

La silla intruye en la banda de circulación hasta Y = 875, dejando **140 px libres** (≥ 120 px exigidos). Todos los demás muebles terminan en Y ≤ 825, dejando 190–254 px de suelo libre bajo su frente.

### Walk-behinds

- **Mesa baja** delante de la cama: el personaje pasa por detrás; capa delantera con alfa, sin colisión declarada en este plano.
- **Alfombra**: capa de suelo transitable; puede dibujarse bajo el personaje.
- Primer plano de la silla si el personaje puede pasar delante de ella.
- Esquinas o laterales de muebles que deban tapar parcialmente al personaje.
- Elementos bajos del primer plano que no bloqueen el paso.
- Cualquier objeto que cruce visualmente la silueta del personaje durante el recorrido.

Los walk-behinds son máscaras visuales con alfa y orden de dibujo; no son colisiones.

### Mesa baja: los tres sistemas en juego (aclaración)

«Mesa baja walk-behind, sin colisión» no significa que cualquier comportamiento del personaje sea aceptable. Hay que distinguir tres sistemas distintos, y esta propuesta los trata por separado:

1. **Colisión física (navegación):** dónde puede desplazarse el personaje. El plano actual no declara colisión sólida para la mesa; el suelo bajo la caja X 2980–3300 / Y 880–990 es transitable según las colisiones vigentes (comprobado por BFS: H14 en (3140, 1000) y la aproximación a la cama en (2890, 880) son alcanzables).
2. **Oclusión visual (walk-behind):** cuándo la mesa se dibuja por delante del personaje. La máscara de oclusión debe depender de la profundidad (Y) real del personaje: si su base está por encima de Y ≈ 935 (detrás de la mesa), la mesa lo tapa parcialmente; si está por debajo (por delante), no. En Godot esto se resuelve con orden de dibujo por Y (`y-sort`) o capa delantera separada, no con una máscara fija que tape siempre.
3. **Navegación de aproximación:** cómo llega el personaje a H14 y a la cama. Acceso a la cama por el lateral izquierdo de la mesa (tramo X 2800–2980 libre); acceso a H14 desde delante o desde los costados. Si en el Art Test el personaje «camina sobre el tablero» al cruzar la zona, la solución es una colisión baja específica del tablero o un corredor de navegación por detrás (Y < 880), decisión que se tomará con evidencia del motor, no por intuición.

**Pendiente de prueba en Godot (Art Test):** el repositorio todavía no contiene un proyecto Godot de la Habitación ni un Art Test preparado para este escenario. Por tanto, el comportamiento real de oclusión, el acceso por el lateral izquierdo y la consecución de H14 con un sprite provisional **no han sido probados**. El BFS del script valida la alcanzabilidad geométrica con las colisiones declaradas; no es una prueba funcional en el motor. Esta comprobación queda registrada como pendiente y forma parte de la fase de Art Test, no de esta iteración documental.

### Regla de seguridad de navegación

Prioridad: que el personaje llegue a cada punto de aproximación sin quedar atrapado. Si una colisión impide alcanzar un hotspot, se modifica la colisión o el punto; no se obliga al jugador a encontrar un píxel exacto.

## 6. Hotspots ubicados en el plano (16)

| ID | Área de interacción aproximada | Acción principal |
|---|---|---|
| H01 Computadora | X 600–830, Y 475–670 | Usar / examinar |
| H02 Escritorio | X 380–980, Y 650–825 | Examinar |
| H03 Silla | X 490–730, Y 680–890 | Sentarse / examinar |
| H04 Biblioteca | X 1620–2180, Y 300–790 | Examinar |
| H05 Libros seleccionados | X 1700–2100, Y 390–690 | Leer / examinar |
| H06 Rack de equipos | X 1080–1560, Y 500–825 | Usar / examinar |
| H07 Radio | X 1150–1390, Y 420–590 | Usar / escuchar |
| H08 Grabadora | X 1360–1560, Y 610–790 | Usar / reproducir |
| H09 Cajonera | X 2320–2650, Y 520–825 | Abrir / buscar |
| H10 Documentos | X 1080–1350, Y 600–820 | Leer / examinar |
| H11 Cama | X 2800–3480, Y 500–850 | Descansar / dormir / examinar |
| H12 Reloj | X 2390–2550, Y 170–330 | Consultar |
| H13 Armario | X 3540–3800, Y 330–850 | Abrir / almacenamiento |
| H14 Mesa baja | X 2980–3300, Y 880–990 | Examinar |
| H15 Objetos personales * | Sin caja fija: según objeto sobre escritorio, rack o estantes | Examinar / recoger cuando corresponda |
| H16 Archivadores izq. | X 60–320, Y 330–825 | Abrir / buscar / examinar |

**\* H15 es un hotspot contextual, no un área fija.** Identifica el conjunto de objetos personales distribuidos sobre distintas superficies. No representa un objeto único ni tiene ubicación definitiva: cada objeto personal (taza, foto, llave, nota, etc.) recibirá su propio hotspot y su propio punto de aproximación cuando el arte final los concrete. Por eso el SVG v2 no dibuja un marcador fijo para H15 y lo documenta como anotación. La numeración H01–H16 se conserva completa: H15 sigue reservado para esta familia de interacciones.

Las áreas son cajas de referencia iniciales. En el montaje real deben recortarse para que un hotspot no tape a otro ni active interacciones a través de muebles. Los elementos sobre una superficie pueden tener hotspots individuales.

## 7. Composición por encuadres de cámara

### Encuadre 1 — X = 0 a 1920

Debe mostrar:
- Archivadores del extremo izquierdo y escritorio/PC completo, con la computadora claramente reconocible.
- Silla y espacio de aproximación.
- Rack de equipos completo (radio y grabadora).
- **Biblioteca como foco de cierre**: su primer tercio (X 1620–1920) anticipa la continuidad.

Validado: el grupo de trabajo/equipos termina en X = 1560, sin cortes. No se corta el monitor, la silla ni el rack. La biblioteca entra parcialmente por la derecha como anticipación, igual que el inicio de consola en la v1, pero ahora es el mueble dominante del centro el que hace de transición.

### Encuadre 2 — X = 1920 a 3840

Debe mostrar:
- Biblioteca (dos tercios restantes) y cajonera con reloj.
- Cama y mesa baja.
- Armario completo.
- Espacio de aproximación frente a cama y armario.

Validado: el descanso completo (cajonera → armario) queda en X ≥ 2320. La cámara permite descubrir el tramo derecho al caminar, sin que la cama o el armario parezcan una habitación separada.

### Zona de solape de composición

La **biblioteca (X 1620–2180)** es ahora el elemento de transición entre encuadres: 300 px en el encuadre 1 y 260 px en el encuadre 2. Su masa vertical continua evita la división artificial que produciría una costura vacía, y su condición de núcleo visual hace que la revelación de la mitad derecha se sienta como girar la vista dentro de la misma habitación.

## 8. Reglas de cámara derivadas del plano (sin cambios respecto de v1)

- Cámara de referencia: 1920 × 1080.
- Límites horizontales: X mínimo 0; X máximo 1920 (posición de cámara para ventana de 1920 px).
- La cámara no debe moverse antes de que el personaje se acerque a una zona de margen configurable.
- En la mitad inicial, permitir desplazamiento sin seguimiento mientras el personaje esté dentro del encuadre.
- Al superar el margen, seguir suavemente.
- En el extremo derecho, detener el seguimiento cuando el borde de cámara alcance X = 1920.
- Mantener la interfaz en CanvasLayer.
- Probar en móvil horizontal y en pantallas con recortes/áreas seguras.

## 8-bis. Validación programática (nueva en v2)

Esta versión incorpora una comprobación automática ejecutada sobre las coordenadas del documento. El script `scripts/validar_plano_v2.py` verifica: cajas dentro del lienzo, solapes no intencionados, puntos de aproximación fuera de colisiones y alcanzables mediante BFS sobre el suelo transitable, despeje ≥ 120 px en la banda de circulación, frente de interacción ≥ 150 px y encuadres. **Resultado: TODO OK.** Se recomienda que el autor revise el resultado y que el script se ejecute de nuevo si se ajustan coordenadas.

## 9. Riesgos detectados y correcciones preventivas

1. **Muebles demasiado profundos:** pueden cortar el recorrido. Solución: reducir su huella inferior o desplazar el punto de aproximación.
2. **Hotspots superpuestos:** pueden seleccionar el objeto equivocado. Solución: dividir objetos compuestos en áreas específicas y priorizar el objeto bajo el cursor/toque.
3. **Cama y armario juntos:** pueden dejar poco espacio para interactuar. Solución: zona frontal común, con puntos de aproximación separados (2890 y 3660).
4. **Biblioteca demasiado ancha:** puede parecer un muro infranqueable. Solución: base sólida con 560 px de frente libre por delante (Y 790–1079).
5. **Corte entre cámaras:** puede partir objetos o revelar una unión artificial. Solución: la biblioteca cruza la costura como masa continua; revisar en ambos encuadres y en desplazamiento continuo.
6. **Escala del personaje:** si resulta demasiado alto o bajo respecto de los muebles, las coordenadas Y y las colisiones pierden sentido. Solución: fijar escala de prueba del personaje y ajustar línea de suelo antes de exportar sprites finales.
7. **Mesa baja frente a la cama:** al estar en primer plano puede tapar la aproximación a la cama si se dibuja demasiado alta. Solución: mantener su tope en Y ≤ 990 y el punto de aproximación de la cama en (2890, 880), al costado izquierdo de la mesa.

## 9-bis. Prueba de validación previa al arte definitivo

1. Crear un bloque gris del lienzo 3840 × 1080.
2. Dibujar cajas de muebles con estas coordenadas.
3. Añadir rectángulo de prueba que represente al personaje.
4. Marcar la banda transitable y los puntos de aproximación.
5. Simular la cámara 1920 × 1080 desplazándose de extremo a extremo.
6. Comprobar que se llega a los **16 puntos de aproximación** sin atravesar muebles ni quedar bloqueado.
7. Revisar la lectura de cada mitad y la transición entre ambas.
8. Ajustar coordenadas y colisiones antes de crear sprites definitivos.

**Criterio de aprobación:** el plano se aprueba cuando el recorrido es cómodo, todos los objetos importantes son accesibles desde el inicio, ambos encuadres se leen como una sola habitación y no hay hotspots inaccesibles. Solo entonces se pasa al mapa visual definitivo de hotspots/colisiones y al escenario panorámico final.

## 10. Pendientes de revisión del autor

- Confirmar la secuencia izquierda-derecha: **archivadores → escritorio/PC → rack (radio + grabadora) → biblioteca → cajonera + reloj → cama + mesa baja → armario**.
- Confirmar si la biblioteca debe seguir siendo el elemento que cruza la costura de cámara, o preferir que la costura caiga en un tramo de pared limpia.
- Decidir si la alfombra y la mesa baja se mantienen como walk-behinds/elementos decorativos según esta propuesta.
- Decidir qué elementos de ambientación (plantas, pósteres, láminas espaciales, esfera decorativa) se incorporan al inventario visual.
- Aprobar la franja de circulación y el nivel de libertad de movimiento en profundidad.
- Aprobar el plano antes de convertir estas coordenadas en el mapa técnico definitivo.

**Importante:** esta propuesta no modifica el canon narrativo. Tampoco declara aprobada la distribución: fija un segundo plano cuantificado, derivado de la revisión visual, para poder revisarlo con precisión.

---

## Anexo: diferencias numéricas v1 → v2

| Elemento | v1 | v2 |
|---|---|---|
| Archivadores izq. | — | 60, 330 → 320, 825 |
| Escritorio/PC | 180, 490 → 790, 825 | 380, 490 → 980, 825 |
| Silla | 470, 690 → 650, 880 | 520, 690 → 700, 880 |
| Rack (antes consola) | 1650, 500 → 2200, 825 | 1080, 500 → 1560, 825 |
| Radio | 1810, 420 → 2070, 590 | 1150, 420 → 1390, 590 |
| Grabadora | 2110, 610 → 2340, 790 | 1360, 610 → 1560, 790 |
| Biblioteca | 900, 300 → 1430, 790 | 1620, 300 → 2180, 790 |
| Cajonera (antes archivador) | 2390, 520 → 2700, 825 | 2320, 520 → 2650, 825 |
| Reloj | 3220, 170 → 3380, 330 | 2390, 170 → 2550, 330 |
| Cama | 2850, 500 → 3520, 850 | 2800, 500 → 3480, 850 |
| Mesa baja (antes mesa aux.) | 2700, 690 → 2870, 835 | 2980, 880 → 3300, 990 (walk-behind) |
| Armario | 3540, 330 → 3800, 850 | 3540, 330 → 3800, 850 |
| Alfombra | — | 1500, 880 → 2400, 1035 (transitable) |
| Mueble de consulta | 1120, 680 → 1510, 830 | — (eliminado; el rack cumple esa función) |
| Archivador v1 (derecha) | 2390, 520 → 2700, 825 | — (sustituido por cajonera con reloj encima) |

---

## Anexo: diferencias numéricas v1 → v2 (colisiones)

| Elemento | v1 (huella) | v2 (huella) |
|---|---|---|
| Archivadores izq. | — | 60, 730 → 320, 825 |
| Escritorio | 180, 730 → 790, 825 | 380, 730 → 980, 825 |
| Silla | 455, 790 → 645, 875 | 540, 800 → 680, 875 |
| Rack (antes consola) | 1650, 730 → 2200, 825 | 1080, 730 → 1560, 825 |
| Biblioteca | 900, 690 → 1430, 790 | 1620, 690 → 2180, 790 |
| Cajonera (antes archivador) | 2390, 730 → 2700, 825 | 2320, 730 → 2650, 825 |
| Cama | 2850, 740 → 3520, 850 | 2800, 740 → 3480, 850 |
| Armario | 3540, 730 → 3800, 850 | 3540, 730 → 3800, 850 |

*(El anexo de colisiones repite la tabla de implantación y huellas para consulta rápida del autor; los valores coinciden con las secciones 3 y 5.)*
