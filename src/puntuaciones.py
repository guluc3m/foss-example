#!/usr/bin/env  python3

# === Puntuaciones ===
# AUTOR : José Antonio Verde Jiménez
# FECHA : 2023-02-25

import os
import sys
import importlib
path = '/'.join(sys.argv[0].split('/')[:-1])
sys.path.append(os.path.join(path, "..", "lib"))
pyxel = importlib.import_module("pyxel")

class Puntuaciones:
    ES_UN_ARCHIVO = -3
    ESPERAR_NOMBRE = -2
    PEDIR_ARCHIVO = -1
    NADA = 0
    MOSTRANDO = 1
    def __init__ (self,
            nombre    : str,
            anchura   : str,
            altura    : str,
            digitos   : int,
            reverso   : bool,
            controles : list[tuple[str]]):
        directorio = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.nombre = os.path.join(directorio, nombre + ".pts")
        self.archivo = None
        self.modo = self.NADA
        self.siguiente = self.NADA
        self.datos = []
        self.anchura = anchura
        self.__color = 0
        self.altura = altura
        self.digitos = digitos
        if reverso:
            self.key = lambda x : -x[1]
        else:
            self.key = lambda x : x[1]
        self.controles = controles
        self.puntos = -1
        self.iniciales = ""
        self.__open()

    def texto (self, x, y, text, centrar):
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

    def __open(self):
        if self.archivo is not None:
            return
        if os.path.exists(self.nombre):
            if os.path.isdir(self.nombre):
                self.modo = self.ES_UN_ARCHIVO
            else:
                self.archivo = open(self.nombre, 'r')
                datos = self.archivo.read().split('\n')
                for dato in filter(bool, datos):
                    dato = dato.split()
                    if len(dato) != 2:
                        print("¡¡ERROR AL LEER EL ARCHIVO DE PUNTUACIONES!!")
                    else:
                        try:
                            int(dato[1])
                        except ValueError:
                            print("¡¡PUNTUACIÓN NO ENTERA!!")
                        else:
                            self.datos.append((dato[0], int(dato[1])))
                self.datos = sorted(self.datos, key=self.key)
                self.archivo.close()
                self.archivo = open(self.nombre, 'w')
                self.__volcar()
                self.modo = self.siguiente
                self.siguiente = self.NADA
        else:
            self.modo = self.PEDIR_ARCHIVO

    def __del__ (self):
        """ Destructor, asegúrate de cerrar el archivo >:3 """
        if self.archivo is not None:
            self.__volcar()
            self.archivo.close()

    def __volcar(self):
        if self.archivo is not None:
            self.archivo.seek(0)
            for n, p in self.datos:
                print(n, p, file=self.archivo)
            self.archivo.flush()

    def mostrar (self):
        self.siguiente = self.MOSTRANDO
        self.__open()
        if self.modo == self.NADA:
            self.siguiente = self.NADA
            self.modo = self.MOSTRANDO

    def añadir (self, puntos : int):
        self.siguiente = self.ESPERAR_NOMBRE
        self.__open()
        self.puntos = puntos
        print(puntos)
        self.iniciales = ""
        if self.modo == self.NADA:
            self.siguiente = self.NADA
            self.modo = self.ESPERAR_NOMBRE
        self.__volcar()

    def actualizar (self):
        if self.modo == self.ES_UN_ARCHIVO:
            pass
        elif self.modo == self.PEDIR_ARCHIVO:
            pass
        elif self.modo == self.ESPERAR_NOMBRE:
            for letter in range(pyxel.KEY_A, pyxel.KEY_Z+1):
                if pyxel.btnp(letter):
                    if len(self.iniciales) < 3:
                        self.iniciales += chr(letter-pyxel.KEY_A+ord('A'))
            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.iniciales = self.iniciales[:-1]
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.datos.append((self.iniciales, self.puntos))
                self.datos = sorted(self.datos, key=self.key)
                self.modo = self.MOSTRANDO
                self.__volcar()
        elif self.modo == self.MOSTRANDO:
            if pyxel.btn(pyxel.KEY_ESCAPE):
                self.modo = self.NADA
                return True
        return False

    def dibujar (self):
        if self.modo == self.ES_UN_ARCHIVO:
            self.texto(self.anchura//2, self.altura//2,
                "Has creado un a carpeta, iborrala!", True)
            self.__open()
        elif self.modo == self.ESPERAR_NOMBRE:
            self.texto(self.anchura//2, self.altura//2,
                f"Escribe tus iniciales ({self.puntos}): {self.iniciales}", True)
            self.__open()
        elif self.modo == self.PEDIR_ARCHIVO:
            self.texto(self.anchura//2, self.altura//2,
                f"Crea un archivo llamado:", True)
            self.texto(self.anchura//2, self.altura//2 + 12,
                self.nombre, True)
            self.__open()
        elif self.modo == self.MOSTRANDO:
            pyxel.cls(0)
            self.__color += 0.25
            if self.__color >= 16:
                self.__color = 2
            color = int(self.__color)
            pyxel.text(4, 0, "___________________________", color)
            pyxel.text(4, 8, "| P U N T U A C I O N E S |", color)
            pyxel.text(4, 11, "___________________________", color)
            i = 0
            fila = 20 + i * 8
            while fila < self.altura - 20 and i < len(self.datos):
                fila = 20 + i * 8
                numero = str(i + 1)
                pyxel.text(16, fila, numero, (color + i) % 14 + 2)
                texto, puntos = self.datos[i]
                texto = (texto + (3 - len(texto))*' ')[:3].upper()
                puntos = '0' * (self.digitos - len(str(puntos))) + str(puntos)
                if i < 3:
                    c = [0xB, 0x9, 0x8][i]
                else:
                    c = 0x7
                pyxel.text(20+len(numero)*4, fila, texto+' '+puntos, c)
                i += 1

            for i in range(len(self.controles)):
                x = pyxel.width // 2 - 24
                y = 24 + 10 * i
                self.texto (x, y, "* %s : %s" % self.controles[i], False)

