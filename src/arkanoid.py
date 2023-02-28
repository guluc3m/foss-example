#!/usr/bin/env  python3
# *-* encoding=utf8 *-*

# AVISO: éste juego está rotísimo y a medio hacer...
# ¡Oh, las bondades del FOSS!

# Controles: sí

# AUTORES : José Antonio Verde Jiménez y Luis Daniel Casais Mezquida
# FECHA     : 2023-02-27

import math
import sys
import os
import importlib
path = '/'.join(sys.argv[0].split('/')[:-1])
sys.path.append(os.path.join(path, "..", "lib"))
pyxel = importlib.import_module("pyxel")

FPS = 60
SCREEN_HEIGHT = 200
SCREEN_WIDTH = 200
PAD_SPEED = FPS
H_BORDER = 8
V_BORDER = 8
BRICK_WIDTH = 16
BRICK_HEIGHT = 8
PAD_WIDTH = 24
PAD_HEIGHT = 6

class Entity:
    def __init__ (self, kind : str, x : int, y : int,
            w : int = 0, h : int = 0, r : int = 0):
        self.__kind = kind
        self.r = r
        self.width = w
        self.height = h
        self.x = x
        self.y = y

    def __rect_rect_collide (self, other : "Entity") -> bool:
        return (
            self.x + self.width  >= other.x and
            self.x <= other.x + other.width and
            self.y + self.height >= other.y and
            self.y <= other.y + other.height)

    def __circle_circle_collide (self, other : "Entity") -> bool:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 <=
                (self.r + other.r) ** 2)

    def __rect_circle_collide (r, c : "Entity") -> bool:
        if ((c.x >= r.x and c.x <= r.x + r.width) or
            (c.y >= r.y and c.y <= r.y + r.height)):
            return ((c.x + c.r >= r.x and c.x - c.r <= r.x + r.width) and
                    (c.y + c.r >= r.y and c.y - c.r <= r.y + r.height))
        else:
            corners = [
                (r.x, r.y),
                (r.x+r.width, r.y),
                (r.x, r.y+r.height),
                (r.x+r.width, r.y+r.height)]
            r2 = c.r ** 2
            for (x, y) in corners:
                if (c.x - x)**2 + (c.y - y)**2 < r2:
                    return True
            return False

    @property
    def kind (self) -> str:
        return self.__kind

    def collide (self, other : "Entity") -> bool:
        if self.kind == "rect" == other.kind:
            return self.__rect_rect_collide (other)
        elif self.kind == "circle" == other.kind:
            return self.__circle_circle_collide (other)
        else:
            if self.kind == "rect":
                return self.__rect_circle_collide (other)
            else:
                return other.__rect_circle_collide (self)

    def update (self, dt : float):
        pass

    def draw (self, dx : int, dy : int):
        pass

class Rectangle (Entity):
    def __init__ (self, x : int, y : int, w : int, h : int, colour : int):
        super().__init__("rect", x, y, w=w, h=h)
        self.colour = colour

    # overriding
    def update (self, dt : float):
        super().update(dt)

    # overriding
    def draw (self, dx : int, dy : int):
        super().draw(dx, dy)
        pyxel.rect(self.x+dx, self.y+dy, self.width, self.height, self.colour)
        pyxel.rectb(self.x+dx, self.y+dy, self.width, self.height, 0x0)

class Circle (Entity):
    def __init__ (self, x : int, y : int, r : int, colour : int):
        super().__init__("circle", x, y, r=r)
        self.colour = colour

    # overriding
    def update (self, dt : float):
        super().update(dt)

    # overriding
    def draw (self, dx : int, dy : int):
        super().draw(dx, dy)
        pyxel.circ(self.x+dx, self.y+dy, self.r, self.colour)
        pyxel.circb(self.x+dx, self.y+dy, self.r, 0x0)

class Ball (Circle):
    def __init__ (self, x : int, y : int, r : int, colour : int):
        super().__init__(x, y, r, colour)
        self.angle = math.pi / 2
        self.speed = FPS * 4

    def __bounce (self, dir : int):
        if dir == 0:
            pass
        elif dir == 1:
            self.angle = math.pi * 2 - 2 * self.angle
        elif dir == 2:
            self.angle = math.pi * 2 - self.angle
        elif dir == 3:
            self.angle = math.pi * 2 - self.angle

    def update (self, dt : float):
        super().update(dt)
        x = self.x + self.speed * dt * math.cos(self.angle)
        y = self.y + self.speed * dt * math.sin(self.angle)
        r = self.r / 2
        b = 0
        if x <= H_BORDER + r:
            x = H_BORDER + r
            b = 1
        if x >= SCREEN_WIDTH - r - H_BORDER:
            x = SCREEN_WIDTH - r - H_BORDER
            b = 1
        if y <= V_BORDER + r:
            y = V_BORDER + r
            b = 2
        if y >= SCREEN_HEIGHT - r - V_BORDER:
            y = SCREEN_HEIGHT - V_BORDER - r
            b = 2
        if b:
            self.__bounce(b)
            # self.update(dt)
        else:
            self.x = x
            self.y = y

    def collide (self, other):
        c = self
        r = other
        # Check which part it collides:
        if (c.x >= r.x and c.y <= r.x + r.width):
            if ((c.x + c.r >= r.x and c.x - c.r <= r.x + r.width) and
                (c.y + c.r >= r.y and c.y - c.r <= r.y + r.height)):
                self.__bounce(1)
            else:
                return False
        if (c.y >= r.y and c.y <= r.y + r.height):
            if ((c.x + c.r >= r.x and c.x - c.r <= r.x + r.width) and
                (c.y + c.r >= r.y and c.y - c.r <= r.y + r.height)):
                self.__bounce(2)
            else:
                return False
        else:
            # Top-Left
            r2 = c.r ** 2
            f = lambda x, y : (c.x - x) ** 2 + (c.y - y) ** 2 <= r2
            if f(r.x, r.y):
                # Top-Left
                self.__bounce(3)
            elif f(r.x+r.width, r.y):
                # Top-Right
                self.__bounce(3)
            elif f(r.x, r.y+r.height):
                # Bottom-Left
                self.__bounce(3)
            elif f(r.x+r.width, r.y+r.height):
                # Bottom-Right
                self.__bounce(3)
            else:
                return False
        return True

class Pad (Rectangle):
    def update (self, dt : float):
        super().update(dt)
        d = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            d -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            d += 1
        x = self.x + d * PAD_SPEED * dt
        if x <= H_BORDER:
            x = H_BORDER
        if x >= SCREEN_WIDTH - self.width - H_BORDER:
            x = SCREEN_WIDTH - self.width - H_BORDER
        self.x = x

class Brick (Rectangle):
    def __init__ (self, x : int, y : int, colour : int):
        super().__init__(x, y, BRICK_WIDTH, BRICK_HEIGHT, colour)

class Game:
    def __init__ (self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS)
        # pyxel.load(os.path.join("..", "resources", "arkanoid.pyxres"),
        #     True, True, True, True)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 3, 0x4)
        w = PAD_WIDTH; h = PAD_HEIGHT
        self.pad = Pad(SCREEN_WIDTH//2 - w//2, SCREEN_HEIGHT - 20, w, 6, 0x6)
        self.dt = 1 / FPS
        count = (SCREEN_WIDTH - 2 * H_BORDER) // BRICK_WIDTH
        padborder = (SCREEN_WIDTH - count * BRICK_WIDTH) // 2
        ycount = int((SCREEN_HEIGHT - 2 * V_BORDER) // BRICK_HEIGHT * .6)
        self.items = []
        for y in range(ycount):
            for x in range(count):
                self.items.append(Brick(
                    x      = padborder + x * BRICK_WIDTH,
                    y      = V_BORDER + y * BRICK_HEIGHT,
                    colour = (x + y) % 16))
        pyxel.run(self.update, self.draw)
        self.count = 0

    def update (self):
        self.ball.update (self.dt)
        self.pad.update (self.dt)
        self.ball.collide(self.pad)
        todelete = []
        for i in range(len(self.items)):
            if self.ball.collide(self.items[i]):
                todelete.append(i)
        for i in range(len(todelete)-1,-1,-1):
            del self.items[todelete[i]]
        self.count = len(todelete)

    def draw (self):
        pyxel.cls(0x7)
        self.ball.draw (self.count, self.count)
        self.pad.draw (self.count, self.count)
        for item in self.items:
            item.draw (self.count, self.count)

if __name__ == "__main__":
    Game()
