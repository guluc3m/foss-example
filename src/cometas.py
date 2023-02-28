#!/usr/bin/env  python3
# *-* encoding=utf8 *-*

# === Lluvia de Cometas ===
# Un pequeño juego que consiste en evitar los cometas con la nave. Puedes
# modificar las constantes que aparecen a continuación en mayúscula para ver
# cómo cambia el juego.
#
# CONTROLES: 
# W/Arriba ------ Arriba
# S/Abajo ------- Abajo
# A/Izquierda --- Izquierda
# D/Derecha ----- Derecha
# Escape -------- Volver
#
# ¡¡Pásatelo bien!!
#
# AUTORES : José Antonio Verde Jiménez y Luis Daniel Casais Mezquida
# FECHA   : 2023-02-27

# ==== Constantes =========================================================== #

ANCHURA_PANTALLA = 256
ALTURA_PANTALLA = 256
FPS = 60

ANCHURA_JUGADOR = 10
ALTURA_JUGADOR = 10
VELOCIDAD_JUGADOR = 80

COMETAS_MÁXIMOS = 100
VELOCIDAD_COMETA = 90

VELOCIDAD_ESTRELLA = 800
CANTIDAD_ESTRELLAS = 200

# ==== Código =============================================================== #

import random
import math
import sys
import os
from puntuaciones import Puntuaciones
import importlib
path = '/'.join(sys.argv[0].split('/')[:-1])
sys.path.append(os.path.join(path, "..", "lib"))
pyxel = importlib.import_module("pyxel")

def texto (x, y, text, centrar):
    """
    Esta función dibuja una caja texto centrada (o no) en la posición (x, y).
    """
    b = 4
    w = len(text) * 4 + b - 1
    h = 7 + b
    c1 = 2
    c2 = 7
    if not centrar:
        pyxel.rect(x, y, w, h, c1)
        pyxel.rectb(x, y, w, h, c2)
        pyxel.text(x + b//2, y + b//2, text, c1)
        pyxel.text(x + b//2, y + b//2 + 1, text, c2)
    else:
        pyxel.rect(x - w//2, y - h//2, w, h, c1)
        pyxel.rectb(x - w//2, y - h//2, w, h, c2)
        pyxel.text(x - w//2 + b//2, y - h//2 + b//2, text, c1)
        pyxel.text(x - w//2 + b//2, y - h//2 + b//2 + 1, text, c2)

class Entidad:
    def __init__ (self,
            x       : int,
            y       : int,
            anchura : int,
            altura  : int):
        self.x = x
        self.y = y
        self.anchura = anchura
        self.altura = altura

    def actualizar (self, dt):
        pass

    def dibujar (self):
        pyxel.rect(int(self.x), int(self.y), self.anchura, self.altura, 7)

    def colisiona (self, otro):
        return (self.x + self.anchura >= otro.x and
                self.x <= otro.x + otro.anchura and
                self.y <= otro.y + otro.altura  and
                self.y + self.altura >= otro.y)

    def __repr__ (self):
        return f"Objeto ({self.x}, {self.y}, {self.anchura}, {self.altura})"

class Jugador (Entidad):
    def __init__ (self, x : int, y : int):
        super().__init__(x, y, ANCHURA_JUGADOR, ALTURA_JUGADOR)
        self.velocidad = VELOCIDAD_JUGADOR

    def actualizar (self, dt):
        # Recibir tecla
        vertical = 0
        horizontal = 0
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            vertical -= 1
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            vertical += 1
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            horizontal -= 1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            horizontal += 1
        # Mover
        self.x += self.velocidad * dt * horizontal
        self.y += self.velocidad * dt * vertical
        if self.x > ANCHURA_PANTALLA - self.anchura:
            self.x = ANCHURA_PANTALLA - self.anchura
        elif self.x < 0:
            self.x = 0
        if self.y > ALTURA_PANTALLA - self.altura:
            self.y = ALTURA_PANTALLA - self.altura
        elif self.y < 0:
            self.y = 0

    def dibujar (self):
        x = self.x - (16 - self.anchura) / 2
        y = self.y - (16 - self.altura) / 2
        pyxel.blt(x, y, 0, 0, 0, 16, 16, 0)

class Cometa (Entidad):
    def __init__ (self):
        # El cometa empieza desde fuera de la pantalla.
        anchura = altura = random.choice([4, 8, 16, 32])
        if random.randint(0, 2) == 0:
            x = random.randint(0, ANCHURA_PANTALLA)
            y = random.choice([-altura, ALTURA_PANTALLA+altura])
        else:
            x = random.choice([-anchura, ANCHURA_PANTALLA+anchura])
            y = random.randint(0, ALTURA_PANTALLA)
        # El ángulo inicial es de forma que vaya al centro de la pantalla.
        dx = ANCHURA_PANTALLA // 2 - x
        dy = ALTURA_PANTALLA // 2 - y
        self.ángulo = math.atan2(dy, dx)
        self.velocidad = VELOCIDAD_COMETA
        if anchura == 4:
            self.u = 0
            self.v = 16
        elif anchura == 8:
            self.u = 0
            self.v = 24
        elif anchura == 16:
            self.u = 8
            self.v = 16
        else:
            self.u = 0
            self.v = 32
        super().__init__(x, y, anchura, altura)

    def actualizar (self, dt):
        x, y = self.x, self.y
        self.x += math.cos(self.ángulo) * self.velocidad * dt
        self.y += math.sin(self.ángulo) * self.velocidad * dt
        pi2 = math.pi * 2
        if self.x > ANCHURA_PANTALLA:
            self.x = x
            self.ángulo = pi2 - 2 * self.ángulo
        elif self.x < -self.anchura:
            self.x = x
            self.ángulo = pi2 - 2 * self.ángulo
        if self.y > ALTURA_PANTALLA:
            self.y = y
            self.ángulo = pi2 - self.ángulo
        elif self.y < -self.altura:
            self.y = y
            self.ángulo = pi2 - self.ángulo
        self.ángulo = self.ángulo % pi2

    def dibujar (self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.anchura, self.altura, 0)

class Estrella (Entidad):
    def __init__ (self):
        super().__init__(0, 0, 0, 0)
        self.rz = 0
        self.actualizar(0)

    def actualizar (self, dt):
        self.rz -= dt * VELOCIDAD_ESTRELLA
        self.px = self.x
        self.py = self.y
        anc = ANCHURA_PANTALLA
        alt = ALTURA_PANTALLA
        if self.rz < 10:
            self.rz = random.randint(1, ANCHURA_PANTALLA)
            self.rx = random.randint(-ANCHURA_PANTALLA, ANCHURA_PANTALLA)
            self.ry = random.randint(-ALTURA_PANTALLA, ALTURA_PANTALLA)
            self.px = anc * (self.rx / self.rz + 1.0) / 2.0
            self.py = alt * (self.ry / self.rz + 1.0) / 2.0
        self.anchura = 2 * (ANCHURA_PANTALLA - self.rz) / ANCHURA_PANTALLA
        self.altura = self.anchura
        self.x = anc * (self.rx / self.rz + 1.0) / 2.0
        self.y = alt * (self.ry / self.rz + 1.0) / 2.0

    def dibujar (self):
        pyxel.line(self.x, self.y, self.px, self.py, 13)
        pyxel.rect(self.x, self.y, self.anchura, self.altura, 7)


class Música:
    def __init__(self) -> None:
        self.state = 0
        
        # Menú principal
        pyxel.playm(1, loop=True)
    
    def actualizar(self, game_state):
        # No tienes que actualizar nada
        if game_state == self.state:
            return

        # Música del juego
        if game_state == 1:  # game
            pyxel.stop()
            pyxel.playm(0, loop=True)
            self.state = 1

        elif game_state == 2:  # loss
            pyxel.stop()
            pyxel.playm(2, loop=False)
            self.state = 2
        
        elif game_state == 3 and self.state != 0:  # points
            pyxel.stop()
            pyxel.playm(1, loop=True)
            self.state = 3


class Juego:
    def __init__ (self):
        pyxel.init(ANCHURA_PANTALLA, ALTURA_PANTALLA, fps=FPS,
            quit_key=pyxel.KEY_NONE)
        pyxel.load(os.path.join("..", "resources", "cometas.pyxres"),
            True, True, True, True)
        # state:
        #   0 : Portada
        #   1 : Jugando
        #   2 : Perdiste :(
        #   3 : Puntuaciones
        self.state = 0
        self.reset()
        self.puntuaciones = Puntuaciones("cometas", ANCHURA_PANTALLA,
            ALTURA_PANTALLA, digitos=8, reverso=True, controles = [
            ("W/Arriba",        "Arriba"),
            ("S/Abajo",         "Abajo"),
            ("A/Izquierda",     "Izquierda"),
            ("D/Derecha",       "Derecha"),
            ("Escape",          "Volver")])
        pyxel.run(self.actualizar, self.dibujar)

    def reset (self):
        self.fin = False
        self.puntuación = 0
        self.jugador = Jugador(ANCHURA_PANTALLA // 2, ALTURA_PANTALLA // 2)
        self.cursor = 0
        self.objetos = []
        self.estrellas = []
        for _ in range(CANTIDAD_ESTRELLAS):
            self.estrellas.append(Estrella())
        self.musica = Música()

    def actualizar (self):
        if self.state == 0:
            if pyxel.btnp (pyxel.KEY_UP):
                self.cursor -= 1
            if pyxel.btnp (pyxel.KEY_DOWN):
                self.cursor += 1
            self.cursor = self.cursor % 3
            if pyxel.btnp (pyxel.KEY_RETURN):
                if self.cursor == 0:
                    self.state = 1
                elif self.cursor == 1:
                    self.state = 3
                    self.puntuaciones.mostrar()
                elif self.cursor == 2:
                    del self.puntuaciones
                    pyxel.quit()
        elif self.state == 1:
            dt = 1 / FPS
            colisiones = []
            for objeto in self.objetos:
                objeto.actualizar(dt)
                if objeto.colisiona(self.jugador):
                    colisiones.append(objeto)
            for estrella in self.estrellas:
                estrella.actualizar(dt)
            self.jugador.actualizar(dt)
            # Creamos un nuevo cometa cada cierto tiempo
            if len(self.objetos) < COMETAS_MÁXIMOS:
                if random.randint(0, FPS*2) == 0:
                    self.objetos.append(Cometa())
            self.puntuación += 100 / FPS
            # Si se choca pierde.
            if len(colisiones) != 0:
                self.state = 2
        elif self.state == 2:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.puntuaciones.añadir(int(self.puntuación))
                self.state = 3
                self.reset()
        elif self.state == 3:
            if self.puntuaciones.actualizar():
                self.state = 0

        self.musica.actualizar(self.state)

    def dibujar (self):
        pyxel.cls(0)
        if self.state == 0:
            pyxel.blt(0, 0, 1, 0, 0, 256, 256, 0)
            pyxel.blt(88, 172 + 3 + self.cursor * 16, 0, 0, 64, 8, 8, 0)
        elif self.state == 1 or self.state == 2:
            for estrella in self.estrellas:
                estrella.dibujar()
            for objeto in self.objetos:
                objeto.dibujar()
            self.jugador.dibujar()
            s = str(int(self.puntuación))
            s = "0" * (8 - len(s)) + s
            texto(0, 0, s, False)
            if self.state == 2:
                texto(ANCHURA_PANTALLA // 2, ALTURA_PANTALLA // 2,
                    "Perdiste..., Pulsa ENTER para continuar.", True)
        elif self.state == 3:
            self.puntuaciones.dibujar()

if __name__ == "__main__":
    try:
        j = Juego ()
    except KeyboardInterrupt:
        del j.puntuaciones
    else:
        del j.puntuaciones

# ==== Fin del Archivo ====================================================== #
