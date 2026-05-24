import turtle
import random

_POOL_SIZE = 4
_pool: list = []
_shape_registered = False

def _register_shape():
    global _shape_registered
    if _shape_registered:
        return

    heart = (
        ( 0, -9), ( 7,  0), ( 5,  6),
        ( 0,  4), (-5,  6), (-7,  0),
    )
    turtle.Screen().register_shape("heart", heart)
    _shape_registered = True

def init_lifeup_pool():
    _register_shape()
    for _ in range(_POOL_SIZE):
        t = turtle.Turtle()
        t.speed(0)
        t.shape("heart")
        t.color("#ff44aa", "#ff0066")
        t.shapesize(1.3, 1.3)
        t.penup()
        t.hideturtle()
        t.goto(2000, 2000)
        _pool.append(t)


class LifeUp:
    SPEED  = 2.0
    RADIUS = 14

    def __init__(self):
        self.x = random.randint(-300, 300)
        self.y = 290
        self.active = True

        if _pool:
            self._t = _pool.pop()
        else:
            _register_shape()
            self._t = turtle.Turtle()
            self._t.speed(0)
            self._t.shape("heart")
            self._t.color("#ff44aa", "#ff0066")
            self._t.shapesize(1.3, 1.3)
            self._t.penup()

        self._t.goto(self.x, self.y)
        self._t.showturtle()
        self._pulse = 0

    def update(self):
        if not self.active:
            return
        self.y -= self.SPEED
        self._t.goto(self.x, self.y)

        self._pulse = (self._pulse + 1) % 20
        if self._pulse == 0:
            self._t.shapesize(1.5, 1.5)
        elif self._pulse == 10:
            self._t.shapesize(1.1, 1.1)

        if self.y < -310:
            self._deactivate()

    def destroy(self):
        self._deactivate()

    def _deactivate(self):
        if not self.active:
            return
        self.active = False
        self._t.hideturtle()
        self._t.goto(2000, 2000)
        _pool.append(self._t)
