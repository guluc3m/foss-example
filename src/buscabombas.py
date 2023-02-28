#!/usr/bin/env  python3
# *-* encoding=utf8 *-*

# === Buscabombas ===
# Un clon del buscaminas. Trata de liberar todos los huecos que no tienen
# minas. El número que aparece en pantalla indica cuántas minas contiguas
# (incluidas las diagonales) hay.
#
# CONTROLES: 
# Click Izquierdo --- Descubrir espacio
# Click Derecho ----- Marcar espacio
# Escape ------------ Volver
#
# ¡¡Pásatelo bien!!
#
# AUTORES : José Antonio Verde Jiménez y Luis Daniel Casais Mezquida
# FECHA   : 2023-02-27

# ==== Constantes =========================================================== #

FILAS = 8
COLUMNAS = 8
BOMBAS = 10
FPS = 30
global ANCHURA_PANTALLA
global ALTURA_PANTALLA

# FILAS = 20
# COLUMNAS = 20

# 8x8  : 10 minas
# 16x16: 40 minas
# 30x16: 99 minas

# No poner a True, vuelve el juego muy muy difícil  :)
NO_CAMBIES_EL_VALOR_DE_ESTA_VARIABLE_SI_QUIERES_SEGUIR_VIVIENDO = False # :3

# ==== Código =============================================================== #

import random
import sys
import os
from puntuaciones import Puntuaciones
import importlib
path = '/'.join(sys.argv[0].split('/')[:-1])
sys.path.append(os.path.join(path, "..", "lib"))
pyxel = importlib.import_module("pyxel")
sys.setrecursionlimit(100000000)

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
    def __init__ (self):
        pass

    def actualizar (self, dt):
        pass

    def dibujar (self):
        pass

class CampoDeMinas (Entidad):
    def __init__ (self, filas : int, columnas : int, bombas : int):
        MAX = 50
        if filas > MAX:
            filas = MAX
        elif filas <= 0:
            filas = 1
        if columnas > MAX:
            columnas = MAX
        elif columnas <= 0:
            columnas = 0
        self.filas = filas
        self.columnas = columnas
        # Valores para posiciones
        # (True, n)     Liberado con n := (si es bomba -1, si no vecinos)
        # (False, n)    No liberado n := (si es bomba -1, si no vecinos)
        # (None, n)     Marcado n := (si es bomba -1, si no vecinos)
        # Configuración inicial, si el usuario toca una bomba se cambiaría.
        if bombas > self.filas * self.columnas - 1:
            bombas = self.filas * self.columnas - 1
        elif bombas <= 0:
            bombas = 1
        if NO_CAMBIES_EL_VALOR_DE_ESTA_VARIABLE_SI_QUIERES_SEGUIR_VIVIENDO:
            bombas = int(0.8 * self.filas * self.columnas)
        self.cantidad = bombas
        posiciones = []
        for i in range(self.filas):
            for j in range(self.columnas):
                posiciones.append((i, j))
        # Generar matriz
        self.bombas = [[(False, 0) for _ in range(columnas)] for _ in range(filas)]
        self.marcadas = 0
        self.descubiertas = 0
        self.nuevo = True
        self.lose = False
        for _ in range(bombas):
            (i, j) = posiciones.pop(random.randrange(len(posiciones)))
            self.bombas[i][j] = (False, -1)

    def __inundar (self):
        DIRS = [-1, -1, 0, -1, 1, 0, 1, 1, -1]
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.bombas[f][c][1] != -1:
                    cont = 0
                    for i in range(8):
                        x = c + DIRS[i]
                        y = f + DIRS[i + 1]
                        if 0 <= y < self.filas and 0 <= x < self.columnas:
                            if self.bombas[y][x][1] == -1:
                                cont += 1
                    self.bombas[f][c] = (self.bombas[f][c][0], cont)

    def __descubrir (self, x, y) -> bool:
        DIRS = [0, 1, 0, -1, 0]
        if 0 <= x < self.columnas and 0 <= y < self.filas:
            (v, n) = self.bombas[y][x]
            if v is not True and n != -1:
                self.bombas[y][x] = (True, n)
                self.descubiertas += 1
                if v is None:
                    self.marcadas -= 1
                if n == 0:
                    for i in range(4):
                        self.__descubrir(x + DIRS[i], y + DIRS[i + 1])

    def altura_total (self) -> int:
        return self.filas * 16

    def anchura_total (self) -> int:
        return self.columnas * 16

    def __raton (self, encabezado : int, borde : int) -> (int, int):
        x = pyxel.mouse_x - borde
        y = pyxel.mouse_y - encabezado
        if 0 <= x < self.anchura_total() and 0 <= y < self.altura_total():
            return (x // 16, y // 16)
        else:
            return None

    def actualizar (self, dt, encabezado : int, borde : int):
        r = self.__raton(encabezado, borde)
        if r is None:
            return
        x, y = r
        if self.nuevo:
            if self.bombas[y][x][1] == -1:
                self.bombas[y][x] = (False, 0)
                # Buscar otro
                while True:
                    i = random.randrange(self.filas)
                    j = random.randrange(self.columnas)
                    if i != x or j != y:
                        self.bombas[i][j] = (False, -1)
                        break
            self.__inundar()
            self.nuevo = False
        if self.bombas[y][x][0] is not True:
            if self.bombas[y][x][1] == -1:
                self.lose = True
                self.bombas[y][x] = (True, -1)
            else:
                self.__descubrir(x, y)

    def marcar (self, encabezado : int, borde : int):
        r = self.__raton(encabezado, borde)
        if r is None:
            return
        x, y = r
        (v, n) = self.bombas[y][x]
        if v is False:
            self.bombas[y][x] = (None, n)
            self.marcadas += 1
        elif v is None:
            self.bombas[y][x] = (False, n)
            self.marcadas -= 1

    def dibujar (self, encabezado : int, borde : int):
        for y in range(self.filas):
            py = encabezado + y * 16
            for x in range(self.columnas):
                px = borde + x * 16
                (v, n) = self.bombas[y][x]
                if v is None:
                    pyxel.blt(px, py, 0, 16, 0, 16, 16, 0xF)
                elif v is False:
                    pyxel.blt(px, py, 0, 0, 0, 16, 16, 0xF)
                else:
                    if n != -1:
                        pyxel.blt(px, py, 0, 16*n, 16, 16, 16, 0xF)
                    else:
                        if self.lose:
                            pyxel.blt(px, py, 0, 48, 0, 16, 16, 0xF)
                        else:
                            pyxel.blt(px, py, 0, 32, 0, 16, 16, 0xF)

    def __descubrir_todo (self):
       # Descubrir el resto
       for i in range(self.filas):
           for j in range(self.columnas):
               (v, n) = self.bombas[i][j]
               # if v is False:
               #     self.marcadas += 1
               self.descubiertas += 1
               self.bombas[i][j] = (True, n)

    def fin (self) -> bool:
        if self.lose:
            self.__descubrir_todo()
            return False
        elif self.filas * self.columnas - self.descubiertas <= self.cantidad:
            self.__descubrir_todo()
            return True
        else:
            return None

class Sonido:
    def __init__(self) -> None:
        self.tick = 0
        self.fin = False
    
    def actualizar(self, tiempo = 0, fin = False):
        game_tick = int(tiempo)

        if fin:
            if not self.fin:
                self.fin = True
                pyxel.play(0, 4, loop = False)

            return

        if game_tick == self.tick:
            return

        # tic
        if game_tick % 2:
            pyxel.play(0, 0, loop = False)
            self.tick = game_tick

        # toc
        else:
            self.tick = game_tick
            pyxel.play(0, 1, loop = False)


class Juego:
    PORTADA = 0
    JUGANDO = 1
    PUNTUACIONES = 2
    MAX_TIMEOUT = FPS * 4
    def __init__ (self):
        global ANCHURA_PANTALLA
        global ALTURA_PANTALLA
        # Iniciar pyxel
        self.reset()
        BORDE = 16
        MENU_ANCHURA = 32 + 8 + 8 + 16 * 3 + 16 * 3 + BORDE * 2
        MENU_ALTURA = 32 + BORDE * 2
        ANCHURA_PANTALLA = max(MENU_ANCHURA, BORDE*2+self.campo.anchura_total())
        ALTURA_PANTALLA = MENU_ALTURA + BORDE + self.campo.altura_total()
        ANCHURA_PANTALLA = max(256, ANCHURA_PANTALLA)
        ALTURA_PANTALLA = max(256, ALTURA_PANTALLA)
        self.borde = (ANCHURA_PANTALLA - self.campo.anchura_total()) // 2
        self.arriba = MENU_ALTURA
        self.anchura = ANCHURA_PANTALLA
        pyxel.init(ANCHURA_PANTALLA, ALTURA_PANTALLA, fps=FPS, quit_key=pyxel.KEY_NONE)
        pyxel.load(os.path.join("..", "resources", "buscabombas.pyxres"),
            True, True, True, True)
        self.puntuaciones = Puntuaciones("buscabombas", ANCHURA_PANTALLA,
            ALTURA_PANTALLA, digitos=3, reverso=False, controles = [
            ("Click Izquierdo", "Descubrir espacio"),
            ("Click Derecho",   "Marcar espacio"),
            ("Escape",          "Volver")])
        pyxel.run(self.actualizar, self.dibujar)

    def reset (self):
        self.campo = CampoDeMinas(FILAS, COLUMNAS, BOMBAS)
        self.estado = 0
        self.tiempo = 0
        self.timeout = 0
        self.cursor = 0
        self.modo = self.PORTADA
        self.sonido = Sonido()

    def actualizar (self):
        if self.modo == self.JUGANDO:
            pyxel.mouse(True)
            estado = self.campo.fin()
            if estado is True:
                self.estado = 1
                self.timeout += 1
                if self.timeout >= self.MAX_TIMEOUT and pyxel.btnp(pyxel.KEY_RETURN):
                    self.puntuaciones.añadir(int(self.tiempo))
                    self.modo = self.PUNTUACIONES
            elif estado is False:
                self.estado = 3
                self.sonido.actualizar(fin = True)
                self.timeout += 1
                if self.timeout >= self.MAX_TIMEOUT and pyxel.btnp(pyxel.KEY_RETURN):
                    self.modo = self.PORTADA
            else:
                dt = 1 / FPS
                self.tiempo += dt
                self.sonido.actualizar(tiempo = self.tiempo)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.campo.actualizar(dt, self.arriba, self.borde)
                elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                    self.campo.marcar(self.arriba, self.borde)
        elif self.modo == self.PORTADA:
            pyxel.mouse(False)
            if pyxel.btnp (pyxel.KEY_DOWN):
                self.cursor += 1
            if pyxel.btnp (pyxel.KEY_UP):
                self.cursor -= 1
            self.cursor = self.cursor % 3
            if pyxel.btnp (pyxel.KEY_RETURN):
                if self.cursor == 0:
                    self.reset()
                    self.modo = self.JUGANDO
                elif self.cursor == 1:
                    self.puntuaciones.mostrar()
                    self.modo = self.PUNTUACIONES
                elif self.cursor == 2:
                    del self.puntuaciones
                    pyxel.quit()
        elif self.modo == self.PUNTUACIONES:
            pyxel.mouse(False)
            if self.puntuaciones.actualizar ():
                self.modo = self.PORTADA

    def dibujar (self):
        global ANCHURA_PANTALLA
        global ALTURA_PANTALLA
        pyxel.cls(0x0)
        if self.modo == self.JUGANDO:
            pyxel.cls(0xD)
            self.dibujar_menu()
            self.campo.dibujar(self.arriba, self.borde)
            if self.timeout >= self.MAX_TIMEOUT:
                texto(ANCHURA_PANTALLA//2, ALTURA_PANTALLA//2,
                    "Pulsa Enter para continuar...", True)
        elif self.modo == self.PORTADA:
            pyxel.cls(0x9)
            offx = max(0, (ANCHURA_PANTALLA - 256) // 2)
            offy = max(0, (ALTURA_PANTALLA - 256) // 2)
            pyxel.blt(offx, offy, 1, 0, 0, 256, 256)
            pyxel.blt(offx + 108, offy + 196 + self.cursor * 16, 0, 0, 96, 8, 8, 0x0);
        elif self.modo == self.PUNTUACIONES:
            self.puntuaciones.dibujar()

    def numero (self, n, x, y):
        g = [(n // 100) % 10, (n // 10) % 10, n % 10]
        if g[0] == 0:
            g[0] = None
            if g[1] == 0:
                g[1] = None
        for i in range(3):
            if g[i] is None:
                pyxel.blt(x + i*16, y, 0, 0, 64, 16, 32, 0xF)
            else:
                pyxel.blt(x + i*16, y, 0, g[i]*16+16, 64, 16, 32, 0xF)

    def dibujar_menu (self):
        # Bordes
        alt = self.arriba + self.campo.altura_total()
        pyxel.blt(0, 0, 0, 112, 0, 16, 16, 0xF)
        pyxel.blt(self.anchura-16, 0, 0, 80, 0, 16, 16, 0xF)
        pyxel.blt(0, alt, 0, 144, 0, 16, 16, 0xF)
        pyxel.blt(self.anchura-16, alt, 0, 128, 0, 16, 16, 0xF)
        pyxel.blt(0, 48, 0, 176, 0, 16, 16, 0xF)
        pyxel.blt(self.anchura-16, 48, 0, 160, 0, 16, 16, 0xF)
        for x in range(16, self.anchura - 16, 16):
            pyxel.blt(x, 0, 0, 64, 0, 16, 16, 0xF)
            pyxel.blt(x, 48, 0, 64, 0, 16, 16, 0xF)
            pyxel.blt(x, alt, 0, 64, 0, 16, 16, 0xF)
        for y in range(16, 48, 16):
            pyxel.blt(0, y, 0, 96, 0, 16, 16, 0xF)
            pyxel.blt(self.anchura-16, y, 0, 96, 0, 16, 16, 0xF)
        for y in range(64, alt, 16):
            pyxel.blt(0, y, 0, 96, 0, 16, 16, 0xF)
            pyxel.blt(self.anchura-16, y, 0, 96, 0, 16, 16, 0xF)
        # Carita en el medio
        pyxel.blt(self.anchura // 2 - 16, 16, 0, self.estado*32, 32, 32, 32, 0xF)
        # Números
        self.numero(int(self.tiempo), 16, 16)
        self.numero(int(self.campo.cantidad - self.campo.marcadas), self.anchura - 16 - 48, 16)

if __name__ == "__main__":
    Juego ()

# ==== Fin del Archivo ====================================================== #
