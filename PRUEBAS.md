# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- nivel válido y nivel inexistente;
- nivel con filas de distinta longitud;
- paleta en ambos límites de la pantalla;
- rebote contra pared, paleta y cada tipo de bloque;
- pérdida de una vida y reinicio de la bola;
- victoria al eliminar el último bloque y derrota al agotar vidas;
- salida limpia con Escape y al cerrar la ventana.

Una mejora opcional no debe romper ninguno de estos casos.

Trabajo hecho por Roman Libertad Tiburcio Racero, UVUS: KFJ0894

El uso de la IA ha sido para exclusivamente el entendimiento de las funciones con parámetros self y el contenido de la libreria pygame, pero no para generar código.

- nivel válido y nivel inexistente

Al ejecutar el juego llamando a niveles/demo.txt, el juego se ejecuta correctamente. Me ha dado problemas al ejecutarlo en la terminal, pero ninguno desde powershell. 

Al ejecutar un archivo inexistente, salta el error FileNotFoundError: La carpeta no existe o no contiene ningún archivo. 

- nivel con filas de distinta longitud

Al crear malo.txt, con filas desiguales, salta el error ValueError: Error en la fila 2. Variando el archivo malo.txt, salta el error indicando la primera linea donde se encuentra el error.

- paleta en ambos límites de la pantalla

Al intentar atravesar el borde de la ventana por ambos lados, la paleta se frena contra estos sin sobrepasarlos.

- rebote contra pared, paleta y cada tipo de bloque

Al intentar rebotar con las paredes y el techo, la pelota rebota sin atravesar la ventana.  
Al golpear la paleta sube, y el ángulo cambia según el punto de impacto.
Al romper un bloque '#' se suman 50 puntos, con un '@' 75 y con un '%' 120. 
Al tocar una esquina de un bloque la bola no se queda atascada.

- pérdida de una vida y reinicio de la bola

Cuando la bola toca la parte baja de la ventana, se descuenta una vida y la bola reaparece sobre la paleta en movimiento.

- victoria al eliminar el último bloque y derrota al agotar vidas

Al perder las 3 vidas aparece "¡Derrota!" y el juego se cierra sin errores. 
Al eliminar el último bloque y conseguir los 3860 puntos aparece "¡Victoria!" y también se cierra sin errores.

- salida limpia con Escape y al cerrar la ventana

Al pulsar Escape o la X de la ventana, el juego se cierra sin errores.