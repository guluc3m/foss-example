#!/usr/bin/env  python3
# *-* encoding=utf8 *-*

class Juego:
    def __init__ (self):
        pyxel.init(ANCHURA_PANTALLA, ALTURA_PANTALLA, fps=FPS)
        pyxel.load(os.path.join("..", "resources", "arkanoid.pyxres"),
            True, True, True, True)
