import turtle
import random

_POOL_SIZE = 20
_pool: list = []

def _register_shapes(screen):
    """Register custom enemy silhouettes once."""

    saucer = (
        ( 0,  10), ( 6,   8), (14,  3), (16,  0),
        (14, -4),  ( 6, -8),  ( 0, -11),
        (-6, -8),  (-14, -4), (-16,  0),
        (-14,  3), (-6,   8),
    )
    screen.register_shape("saucer", saucer)

    bomber = (
        ( 0,  8),   ( 4,  4),   (18,  0),  (12, -6),
        ( 6, -5),   ( 4, -12),  ( 0, -10),
        (-4, -12),  (-6, -5),   (-12, -6), (-18,  0),
        (-4,  4),
    )
    screen.register_shape("bomber", bomber)

    dart = (
        ( 0,  14), ( 3,   6), (10,  -2), ( 7,  -8),
        ( 2,  -6), ( 0, -12),
        (-2,  -6), (-7,  -8), (-10, -2), (-3,   6),
    )
    screen.register_shape("dart", dart)

_shapes_registered = False

def init_enemy_pool():
    global _shapes_registered
    screen = turtle.Screen()
    if not _shapes_registered:
        _register_shapes(screen)
        _shapes_registered = True
    for _ in range(_POOL_SIZE):
        _pool.append(_make_enemy_turtle(screen))

DESIGNS = [
    ("saucer", "#ff4444", "#660000"),
    ("saucer", "#ff6600", "#662200"),
    ("bomber", "#cc44ff", "#440066"),
    ("bomber", "#ff44aa", "#660033"),
    ("dart",   "#00ddff", "#004466"),
    ("dart",   "#ffcc00", "#664400"),
]

def _make_enemy_turtle(screen=None):
    t = turtle.Turtle()
    t.speed(0)
    t.shape("saucer")
    t.color("#ff4444", "#660000")
    t.shapesize(1.4, 1.4)
    t.penup()
    t.setheading(270)
    t.hideturtle()
    t.goto(2000, 2000)
    return t


class Enemy:
    RADIUS  = 16
    SPAWN_Y = 290

    def __init__(self, level=1):
        self.x      = random.randint(-330, 330)
        self.y      = self.SPAWN_Y
        self.speed  = min(2.0 + (level - 1) * 0.6, 10.0)
        self.drift  = random.uniform(-1.4, 1.4)
        self._zt    = 0
        self._ztmax = random.randint(20, 55)
        self.active = True

        shape, outline, fill = random.choice(DESIGNS)

        if _pool:
            self._t = _pool.pop()
        else:
            self._t = _make_enemy_turtle()

        self._t.shape(shape)
        self._t.color(outline, fill)
        self._t.shapesize(1.4, 1.4)
        self._t.setheading(270)
        self._t.goto(self.x, self.y)
        self._t.showturtle()

    def update(self):
        if not self.active:
            return
        self.y -= self.speed
        self.x += self.drift

        if self.x >  355: self.drift = -abs(self.drift)
        if self.x < -355: self.drift =  abs(self.drift)

        self._zt += 1
        if self._zt >= self._ztmax:
            self.drift  *= -1
            self._zt     = 0
            self._ztmax  = random.randint(20, 55)

        self._t.goto(self.x, self.y)

        if self.y < -310:
            self._deactivate()

    def escaped(self):
        return self.y < -310

    def destroy(self):
        self._deactivate()

    def _deactivate(self):
        if not self.active:
            return
        self.active = False
        self._t.hideturtle()
        self._t.goto(2000, 2000)
        _pool.append(self._t)
