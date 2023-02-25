#!/usr/bin/env  python3

# === Puntuaciones ===
# AUTORES : José Antonio Verde Jiménez y Luis Daniel Casais Mezquida
# FECHA   : 2023-02-25

import os

class Puntuaciones:
    def __init__ (self, nombre : str):
        directorio = os.path.dirname(os.path.realpath(__file__))
        self.nombre = os.path.join(directorio, nombre + ".pts")
        self.archivo = None

    def __del__ (self):
        """ Destructor, asegúrate de cerrar el archivo >:3 """
        if self.archivo is not None:
            self.archivo.close()

    def actualizar (self):
        pass

    def dibujar (self):
        pass

