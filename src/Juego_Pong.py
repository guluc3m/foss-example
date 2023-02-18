#!/usr/bin/env  python3
# *-* encoding=utf8 *-*

# === Pong ===
# Clásico juego de ping pong multijugador
# Las teclas "w" y "s" (arriba y abajo) controlan la pala de la izquierda 
# Las flechas del teclado controlan el movimiento de la pala de la derecha 
#
# AUTOR : Daniel Gómez Schwartz
# FECHA : 2023-02-18

# === CONSTANTES ==========================================================#
ALTURA_PANTALLA = 300
ANCHURA_PANTALLA = 400
FPS = 30
VELOCIDAD_JUGADOR = 2
VELOCIDAD_PELOTA = 3
RADIO_PELOTA = 10
TAMAÑO_JUGADORES = 45

# === Código ==============================================================#
import math 
import random
import sys
import os
import importlib
path = '/'.join(sys.argv[0].split('/')[:-1])
sys.path.append(os.path.join(path, "..", "lib"))
pyxel = importlib.import_module("pyxel")
import pyxel

class Vect:
    def __init__(self, x : int, y : int) -> None:
        self.x = float(x)
        self.y = float(y)

class Velocidad:
    def __init__(self, x : int, y : int) -> None:
        self.m = math.sqrt(x*x + y*y)
        self.x = x / self.m * VELOCIDAD_PELOTA
        self.y = y / self.m * VELOCIDAD_PELOTA

class Pelota:
    def __init__(self, px : int, py : int):
        self.pos = Vect(px, py)
        self.vel = Velocidad(random.choice([-2,2]), random.choice([-2,2]))
    def tic(self)-> None:
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        #Choque contra las paredes
        if self.pos.y >= ALTURA_PANTALLA - RADIO_PELOTA or self.pos.y <= RADIO_PELOTA:
            self.vel.y = -self.vel.y



class Pala:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        self.punt: int = 0

class Juego():
    def __init__(self) -> None:
        pyxel.init(ANCHURA_PANTALLA, ALTURA_PANTALLA, fps=FPS)
        self.Pelota = Pelota(ANCHURA_PANTALLA/2, ALTURA_PANTALLA/2)
        self.Jugador_a = Pala(
            ANCHURA_PANTALLA - ANCHURA_PANTALLA,
            ALTURA_PANTALLA// 2
        )
        self.Jugador_b = Pala(
            ANCHURA_PANTALLA - 20,
            ALTURA_PANTALLA // 2
        )
        
        pyxel.run(self.actualizar, self.dibujar)

    def actualizar(self):
        self.Pelota.tic()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        #Movimiento Palas
        if pyxel.btn(pyxel.KEY_W):
            if self.Jugador_a.y > ALTURA_PANTALLA - ALTURA_PANTALLA:
                self.Jugador_a.y -= VELOCIDAD_JUGADOR
        if pyxel.btn(pyxel.KEY_S) :
            if self.Jugador_a.y < ALTURA_PANTALLA - TAMAÑO_JUGADORES:
                self.Jugador_a.y += VELOCIDAD_JUGADOR
        if pyxel.btn(pyxel.KEY_UP) :
            if self.Jugador_b.y > ALTURA_PANTALLA - ALTURA_PANTALLA:
                self.Jugador_b.y -= VELOCIDAD_JUGADOR
        if pyxel.btn(pyxel.KEY_DOWN) :
            if self.Jugador_b.y < ALTURA_PANTALLA - TAMAÑO_JUGADORES:
                self.Jugador_b.y += VELOCIDAD_JUGADOR

        #Colisión con palas
        if self.Pelota.pos.x - RADIO_PELOTA <= self.Jugador_a.x + 20 and self.Pelota.pos.y <= self.Jugador_a.y + TAMAÑO_JUGADORES and self.Pelota.pos.y >= self.Jugador_a.y:
            self.Pelota.vel.x = -self.Pelota.vel.x 

        if self.Pelota.pos.x + RADIO_PELOTA >= self.Jugador_b.x and self.Pelota.pos.y <= self.Jugador_b.y + TAMAÑO_JUGADORES and self.Pelota.pos.y >= self.Jugador_b.y:
            self.Pelota.vel.x = -self.Pelota.vel.x 

        #Puntos
        if self.Pelota.pos.x >= ANCHURA_PANTALLA - RADIO_PELOTA:
            self.Pelota = Pelota(ANCHURA_PANTALLA / 2, ALTURA_PANTALLA /2)
            self.Jugador_a.punt += 1
        if self.Pelota.pos.x <= RADIO_PELOTA:
            self.Pelota = Pelota(ANCHURA_PANTALLA / 2, ALTURA_PANTALLA /2)
            self.Jugador_b.punt += 1
        
    def dibujar (self) -> None:
        pyxel.cls(0)
        #Pelota
        pyxel.circ(int(self.Pelota.pos.x), int(self.Pelota.pos.y), RADIO_PELOTA, 7)
        #Palas
        pyxel.rect(self.Jugador_a.x + 10, self.Jugador_a.y, TAMAÑO_JUGADORES/ 4.5, TAMAÑO_JUGADORES, 7)
        pyxel.rect(self.Jugador_b.x - (TAMAÑO_JUGADORES / 4.5)+10, self.Jugador_b.y, TAMAÑO_JUGADORES / 4.5, TAMAÑO_JUGADORES, 7)

        #Puntuaciones
        pyxel.text(ANCHURA_PANTALLA / 2 - 7, ALTURA_PANTALLA / 2, str(self.Jugador_b.punt), 7)
        pyxel.text(ANCHURA_PANTALLA / 2 + 7, ALTURA_PANTALLA / 2, str(self.Jugador_a.punt), 7)
        


if __name__ == "__main__":
    Juego ()

# === Fin del archivo ================================================================================#