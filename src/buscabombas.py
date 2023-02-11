# ==== Constantes =========================================================== #

FILAS = 8
COLUMNAS = 8
BOMBAS = 16
FPS = 30

# 8x8  : 10 minas
# 16x16: 40 minas
# 30x16: 99 minas


NO_CAMBIAR_EL_VALOR_DE_ESTA_VARIABLE_SI_QUIERES_SOBREVIVIR = False

# ==== Código =============================================================== #

import random
import math
import time
import sys
import os
import importlib
path = '/'.join(sys.argv[0].split('/')[:-1])
sys.path.append(os.path.join(path, "..", "lib"))
pyxel = importlib.import_module("pyxel")

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
        self.cantidad = bombas
        posiciones = []
        for i in range(self.filas):
            for j in range(self.columnas):
                posiciones.append((i, j))
        # Generar matriz
        self.bombas = [[(False, 0) for _ in range(columnas)] for _ in range(filas)]
        self.marcadas = 0
        for _ in range(bombas):
            (i, j) = posiciones.pop(random.randrange(len(posiciones)))
            self.bombas[i][j] = (False, -1)

    def inundar (self):
        pass

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
        print(x, y)

    def marcar (self, encabezado : int, borde : int):
        r = self.__raton(encabezado, borde)
        if r is None:
            return
        x, y = r
        print(x, y)

    def dibujar (self, encabezado : int, borde : int):
        for y in range(self.filas):
            py = encabezado + y * 16
            for x in range(self.columnas):
                px = borde + x * 16
                (v, n) = self.bombas[y][x]
                if v is None:
                    pyxel.blt(px, py, 0, 0, 16, 16, 16, 0xF)
                elif v is False:
                    pyxel.blt(px, py, 0, 0, 0, 16, 16, 0xF)

class Juego:
    def __init__ (self):
        # Iniciar pyxel
        self.campo = CampoDeMinas(FILAS, COLUMNAS, BOMBAS)
        BORDE = 16
        MENU_ANCHURA = 32 + 8 + 8 + 16 * 3 + 16 * 3 + BORDE * 2
        MENU_ALTURA = 32 + BORDE * 2
        ANCHURA_PANTALLA = max(MENU_ANCHURA, BORDE*2+self.campo.anchura_total())
        ALTURA_PANTALLA = MENU_ALTURA + BORDE + self.campo.altura_total()
        self.borde = (ANCHURA_PANTALLA - self.campo.anchura_total()) // 2
        self.arriba = MENU_ALTURA
        self.anchura = ANCHURA_PANTALLA
        self.status = 0
        self.tiempo = 0
        pyxel.init(ANCHURA_PANTALLA, ALTURA_PANTALLA, fps=FPS)
        pyxel.load(os.path.join("..", "resources", "buscabombas.pyxres"),
            True, True, True, True)
        pyxel.mouse(True)
        pyxel.run(self.actualizar, self.dibujar)

    def actualizar (self):
        dt = 1 / FPS
        self.tiempo += dt
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.campo.actualizar(dt, self.arriba, self.borde)
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.campo.marcar(self.arriba, self.borde)

    def dibujar (self):
        pyxel.cls(0xD)
        self.dibujar_menu()
        self.campo.dibujar(self.arriba, self.borde)

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
        pyxel.blt(self.anchura // 2 - 16, 16, 0, self.status*32, 32, 32, 32, 0xF)
        # Números
        self.numero(int(self.tiempo), 16, 16)
        self.numero(int(self.tiempo), self.anchura - 16 - 48, 16)

if __name__ == "__main__":
    Juego ()

# ==== Fin del Archivo ====================================================== #
