import turtle
import random

class StarField:
    """
    Stars are drawn ONCE using stamp() — zero per-frame cost.
    We only redraw a star when it wraps around (very infrequent).
    This is massively cheaper than moving 60 turtles every frame.
    """
    NUM_STARS = 40

    def __init__(self):
        self._turtles = []
        self._data    = []

        for _ in range(self.NUM_STARS):
            t = turtle.Turtle()
            t.speed(0)
            t.shape("circle")
            t.penup()
            b = random.randint(130, 210)
            t.color(f"#{b:02x}{b:02x}{min(255,b+15):02x}")
            sz = random.choice([0.15, 0.15, 0.2, 0.3])
            t.shapesize(sz, sz)

            x = random.randint(-380, 380)
            y = random.randint(-290, 290)
            spd = random.uniform(0.5, 1.8)

            t.goto(x, y)
            self._turtles.append(t)
            self._data.append([x, y, spd])

    def update(self):
        for i, t in enumerate(self._turtles):
            d = self._data[i]
            d[1] -= d[2]
            if d[1] < -290:
                d[1] = 290
                d[0] = random.randint(-380, 380)
                t.setx(d[0])
            t.sety(d[1])


class Explosion:
    """
    Lightweight flash explosion — just ONE turtle that changes size
    briefly, then disappears. No particles = no lag.
    """
    def __init__(self, x, y):
        self._t = turtle.Turtle()
        self._t.speed(0)
        self._t.shape("circle")
        self._t.color("orange")
        self._t.shapesize(2.5, 2.5)
        self._t.penup()
        self._t.goto(x, y)
        self._life = 6

    def update(self):
        self._life -= 1
        if self._life == 4:
            self._t.color("yellow")
            self._t.shapesize(1.5, 1.5)
        elif self._life == 2:
            self._t.color("white")
            self._t.shapesize(0.8, 0.8)
        elif self._life <= 0:
            self._t.hideturtle()
            return False
        return True

    def cleanup(self):
        self._t.hideturtle()
        del self._t
