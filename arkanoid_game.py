"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:


    if not self.level_path.exists() or not self.level_path.is_file():
        raise FileNotFoundError(f"La carpeta no existe o no contiene ningún archivo.")

    texto = self.level_path.read_text(encoding='utf-8')

    filas = []
    for linea in texto.splitlines():
        if not len(linea) == 0:
            filas.append(linea)

    if len(filas) == 0:
        raise ValueError("No existe")

    ancho = len(filas[0])
    for i, fila in enumerate(filas):
        if len(fila) != ancho:
            raise ValueError(f"Error en la fila {i+1}")

    self.layout = filas
    return self.layout


@arkanoid_method
def preparar_entidades(self) -> None:

    self.paddle.size = self.PADDLE_SIZE
    self.paddle.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PADDLE_OFFSET,)

    self.score = 0
    self.lives = 3
    self.end_message = ""

    self.reiniciar_bola()

@arkanoid_method
def crear_bloques(self) -> None:
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()

    for fila, linea in enumerate(self.layout):
        for columna, simbolo in enumerate(linea):
            if simbolo in self.BLOCK_COLORS:
                self.blocks.append(self.calcular_posicion_bloque(fila, columna))
                self.block_colors.append(self.BLOCK_COLORS[simbolo])
                self.block_symbols.append(simbolo)


@arkanoid_method
def procesar_input(self) -> None:
    teclas = self.obtener_estado_teclas()
    izquierda = teclas[self.KEY_LEFT] or teclas[self.KEY_A]
    derecha = teclas[self.KEY_RIGHT] or teclas[self.KEY_D]

    if izquierda and not derecha:
        self.paddle.x -= int(self.PADDLE_SPEED)
    elif derecha and not izquierda:
        self.paddle.x += int(self.PADDLE_SPEED)

    if self.paddle.left < 0:
        self.paddle.left = 0
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH


@arkanoid_method
def actualizar_bola(self) -> None:

    radio = self.BALL_RADIUS

    self.ball_pos += self.ball_velocity

    if self.ball_pos.x - radio <= 0:
        self.ball_pos.x = radio
        self.ball_velocity.x = abs(self.ball_velocity.x)
    elif self.ball_pos.x + radio >= self.SCREEN_WIDTH:
        self.ball_pos.x = self.SCREEN_WIDTH - radio
        self.ball_velocity.x = -abs(self.ball_velocity.x)
    if self.ball_pos.y - radio <= 0:
        self.ball_pos.y = radio
        self.ball_velocity.y = abs(self.ball_velocity.y)

    if self.ball_pos.y - radio > self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives <= 0:
            self.end_message = "¡Derrota!"
            self.running = False
        else:
            self.reiniciar_bola()
        return

    ball_rect = self.obtener_rect_bola()

    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        desplazamiento = (self.ball_pos.x - self.paddle.centerx) / (self.paddle.width / 2)
        desplazamiento = max(-1.0, min(1.0, desplazamiento))
        self.ball_velocity = Vector2(desplazamiento, -1).normalize() * self.BALL_SPEED
        self.ball_pos.y = self.paddle.top - radio
        ball_rect = self.obtener_rect_bola()

    for i, bloque in enumerate(self.blocks):
        if ball_rect.colliderect(bloque):
            self.score += self.BLOCK_POINTS[self.block_symbols[i]]

            solape_x = min(ball_rect.right, bloque.right) - max(ball_rect.left, bloque.left)
            solape_y = min(ball_rect.bottom, bloque.bottom) - max(ball_rect.top, bloque.top)
            if solape_x < solape_y:
                self.ball_velocity.x = -self.ball_velocity.x
            else:
                self.ball_velocity.y = -self.ball_velocity.y


            del self.blocks[i]
            del self.block_colors[i]
            del self.block_symbols[i]
            break

    if not self.blocks:
        self.end_message = "¡Victoria!"
        self.running = False


@arkanoid_method
def dibujar_escena(self) -> None:
    if not self.screen:
        return

    self.screen.fill(self.BACKGROUND_COLOR)

    for bloque, color in zip(self.blocks, self.block_colors):
        self.dibujar_rectangulo(bloque, color)

    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    centro = (int(self.ball_pos.x), int(self.ball_pos.y))
    self.dibujar_circulo(centro, self.BALL_RADIUS, self.BALL_COLOR)

    self.dibujar_texto(f"Puntos: {self.score}", (10, 10))
    self.dibujar_texto(f"Vidas: {self.lives}", (self.SCREEN_WIDTH - 110, 10))

    if self.end_message:
        self.dibujar_texto(
            self.end_message,
            (self.SCREEN_WIDTH // 2 - 90, self.SCREEN_HEIGHT // 2),
            grande=True,
        )


@arkanoid_method
def run(self) -> None:
    try:
        self.inicializar_pygame()
        self.cargar_nivel()
        self.preparar_entidades()
        self.crear_bloques()
        self.running = True

        while self.running:
            for evento in self.iterar_eventos():
                if evento.type == self.EVENT_QUIT:
                    self.running = False
                elif evento.type == self.EVENT_KEYDOWN and evento.key == self.KEY_ESCAPE:
                    self.running = False

            self.procesar_input()
            self.actualizar_bola()
            self.dibujar_escena()
            self.actualizar_pantalla()
            self.clock.tick(self.FPS)

        if self.end_message:
            self.esperar(2000)
    finally:
        self.finalizar_pygame()

def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
