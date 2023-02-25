#!/usr/bin/env  python3
# *-* encoding=utf8 *-*

import pyxel
import math

FPS = 60
SCREEN_HEIGHT = 200
SCREEN_WIDTH = 200
PAD_SPEED = FPS
H_BORDER = 8
V_BORDER = 8

class Entity:
    def __init__ (self, kind : str, x : int, y : int,
            w : int = 0, h : int = 0, r : int = 0):
        self.__kind = kind
        self.r = r
        self.width = w
        self.height = h
        self.x = x
        self.y = y

    @property
    def kind (self) -> str:
        return self.__kind

    def collide (self, other : "Entity") -> bool:
        if self.kind == "rect" == other.kind:
            return (
                self.x + self.width  >= other.x and
                self.x <= other.x + other.width and
                self.y + self.height >= other.y and
                self.y <= other.y + other.height)
        elif self.kind == "circle" == other.kind:
            return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 <=
                (self.r + other.r) ** 2)
        else:
            if self.kind == "rect":
                r = self
                c = other
            else:
                r = other
                c = self
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
        self.speed = FPS

    def __bounce (self, dir : int):
        if dir == 1:
            self.angle = math.pi * 2 - self.angle
        else:
            self.angle = self.angle

    def update (self, dt : float):
        super().update(dt)
        x = self.x + self.speed * dt * math.cos(self.angle)
        y = self.y + self.speed * dt * math.sin(self.angle)
        r = self.r / 2
        if x <= H_BORDER + r:
            x = H_BORDER + r
        if x >= SCREEN_WIDTH - r - H_BORDER:
            x = SCREEN_WIDTH - r - H_BORDER
        if y <= V_BORDER + r:
            y = V_BORDER + r
        if y >= SCREEN_HEIGHT - r - V_BORDER:
            y = SCREEN_HEIGHT - V_BORDER - r
        self.x = x
        self.y = y

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

class Game:
    def __init__ (self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS)
        # pyxel.load(os.path.join("..", "resources", "arkanoid.pyxres"),
        #     True, True, True, True)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 3, 0x4)
        w = 24; h = w * .3
        self.pad = Pad(SCREEN_WIDTH//2 - w//2, SCREEN_HEIGHT - 20, w, 6, 0x6)
        self.dt = 1 / FPS
        pyxel.run(self.update, self.draw)

    def update (self):
        self.ball.update (self.dt)
        self.pad.update (self.dt)

    def draw (self):
        pyxel.cls(0x7)
        self.ball.draw (0, 0)
        self.pad.draw (0, 0)

if __name__ == "__main__":
    Game()
